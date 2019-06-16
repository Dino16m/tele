import random
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetAdminLogRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from time import sleep
from telethon.tl.types import ChannelParticipantsRecent
from telethon.tl.types import InputChannel
from telethon.tl.types import ChannelAdminLogEventsFilter
from telethon.tl.types import InputUserSelf
from telethon.tl.types import InputUser
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, PeerUser
from singlify import makeSingle, readFromFile, writeToFile, writeSingle, backupUsers, commitSuccess
import os
from vomitonegro import do
from telethon.tl.functions.channels import InviteToChannelRequest


api_id = 872129
api_hash = '1390959115b339a8e20294e3591a8b41'

def getChannels(client):
    channels = {d.entity.username: d.entity
        for d in client.get_dialogs()
            if d.is_channel}
    return channels
    
def getChannelParticipants(client, channel):
    users = []
    try:
        for u in client.get_participants(channel):
            if not u.bot and not u.scam and not u.restricted:
                users.append(u)
    except Exception as e:
        print(e.args)
    return users
    
def addUsersToCsv(users, filepath, singlify = False):
    basename = os.path.basename(filepath)
    basedir = os.path.dirname(filepath)
    if singlify:
        return writeSingle(filepath, users) 
    else:
        return writeToFile(users, basename, basedir)
        
def addUsersToChannel(client, users, channel):
    channelEntity = InputPeerChannel(channel.id, channel.access_hash)
    count = 0
    error = False
    success = []
    for user in users:
        if type(user)==str:
            try:
                userToAdd = client.get_input_entity(user)
            except Exception:
                continue
        else:
            userToAdd = client.get_input_entity(user.id)
        try:
           client(InviteToChannelRequest(channelEntity,[userToAdd]))
        except Exception as e:
            print(e.args)
            error = True
        finally:
            if not error == True:
                print('adding users to channel')
                success.append(user)
            error = False
        if count >= 50 :
            sleep(random.randint(10,61)*2)
            count = 0
            continue
        count = count + 1
    return success
    
def getUsersFromCsv(filepath):
    basename = os.path.basename(filepath)
    basedir = os.path.dirname(filepath)
    if not os.path.isfile(basedir+basename):
        return []
    return readFromFile(basename, basedir)

def printChannels(channels):
    for channel in channels:
        print(channel)
    return

def getSomeUsers(range, users):
    list = []
    i = 0
    for user in users:
        if i>=range:
            break
        list.append(user)
        i = i + 1
    return list
                
def getAllChannelUsers(client, channels):
    list = []
    for channel in channels:
        if channel == None:
            continue
        users = getChannelParticipants(client, channel)
        list.extend(users)
    return list

def removeSuccess(success, users):
    for user in users:
        if user in success:
            users.remove(user)
    return users
    
def numberOfUsers(filepath):
    if not os.path.isfile(filepath): 
        return 0
    basename = os.path.basename(filepath)
    basedir = os.path.dirname(filepath)
    return len(readFromFile(basename, basedir))

def backup(filepath):
    return backupUsers(filepath)

def removeUsersAlreadyInChannel(channelUsers, users):
    usersInChannel = channelUsers
    for channelUser in channelUsers:
        if channelUser.username in users:
            users.remove(channelUser.username)
    return users

def add(peters, channelInto, filepath='users.txt', limit=1000):
    do()
    count = 0
    if not os.path.isfile(filepath):
        return 0
    print('adding has started')
    users = getUsersFromCsv(filepath)
    removedUsersInChannel = False
    for peter in peters:
        with TelegramClient(peter, api_id, api_hash) as client:
            client.send_message('me', 'Hello, myself!')
            channels = getChannels(client)
            random.shuffle(users)
            users.reverse()
            if not removedUsersInChannel:
                channelUsers = getChannelParticipants(client, channels[channelInto])
                users = removeUsersAlreadyInChannel(channelUsers, users)
                removedUsersInChannel = True
            if count < limit:
                success = addUsersToChannel(client, users, channels[channelInto])
                count = count + len(success)
            else:
                print('you have exhausted your quota \n and adding has ended')
                break
            users = removeSuccess(success, users)
            print('peter '+peter+' done and dusted adding')
    commitSuccess(users, filepath)
    print('adding has ended')
    return True

def work(peters, filepath='users.txt'):
    do()
    print('storing users started')
    allUsers = []
    for peter in peters:
        with TelegramClient(peter, api_id, api_hash) as client:
            client.send_message('me', 'Hello, myself!')
            channels = getChannels(client)
            printChannels(channels)
            users = getAllChannelUsers(client, channels)
            allUsers.extend(users)
            print('peter '+peter+' done and dusted writing') 
    number = addUsersToCsv(users, filepath, True)
    print('storing users ended')
    return number








