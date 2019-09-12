import random
from time import sleep
#from myexceptions import OutOfUserException
from singlify import getUsersFromStore, storeUsers, makeSingle
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import InputPeerChannel
from vomitonegro import do
from threading import Thread
import sys

#api_id = 872129
#api_hash = '1390959115b339a8e20294e3591a8b41'

api_id = 764531
api_hash = 'a41f8549c7dd1341613de3569f9796cb'
channelStore = {}

def getChannels(client):
    channels = {d.entity.username: d.entity
                for d in client.get_dialogs()
                if d.is_channel}
    return channels

def appendToChannelStore(channelName, users):
    global channelStore
    if type(channelName) == str:
        if channelName not in channelStore.keys():
            channelStore[channelName] = users
    else:
        if channelName is not None and channelName.username is not None and channelName.username not in channelStore.keys():
            channelStore[channelName.username] = users

def stashChannelStore():
    global channelStore
    store = channelStore
    thread = Thread(target=storeUsers, args=[store])
    thread.start()


def getChannelParticipants(client, channel):
    users = []
    try:
        for u in client.get_participants(channel):
            if not u.bot and not u.scam and not u.restricted:
                if u.username is not None:
                    users.append(u)
    except Exception as e:
        print(e.args)
    appendToChannelStore(channel, users)
    return users

def chunkify(list, chunkSize=100):
    chunks = [[]]
    count = 0
    for list1 in list:
        if count < chunkSize:
            chunk = chunks[-1]
            count = count + 1
        else:
            chunks.append([])
            chunk = chunks[-1]
            count = 0
        chunk.append(list1)
    return chunks

def getSuccessFromUpdate(update):
    if len(update) < 1:
        return []
    users = []
    for u in update:
        if u.username is not None:
            users.append(u)
    return users


def printAddStatus(length):
    if length > 0:
        print('The count here is ' + str(length))
        print('adding users to channel')


def addUsersToChannel(client, users, channel):
    channelEntity = InputPeerChannel(channel.id, channel.access_hash)
    count = 0
    error = False
    success = []
    usersToAdd = chunkify(users)
    for usersToAdd1 in usersToAdd:
        try:
            update = client(InviteToChannelRequest(channelEntity, usersToAdd1))
            sleep(5)
        except Exception as e:
            print(e.args)
            error = True
        finally:
            if not error:
                printAddStatus(len(update.users))
                success.extend(getSuccessFromUpdate(update.users))
            error = False
        if count >= 50:
            tick = random.randint(10, 70) * 2
            print('adding has been paused for '+str(tick) +
                  ' seconds in line with Telegram guidelines, it will resume immediately the time elapses.')
            sleep(tick)
            count = 0
            continue
    count = count + 1
    return success


def printChannels(channels):
    for channel in channels:
        print(channel)
    return


def getAllChannelUsers(client, channels):
    list = []
    for channel in channels:
        if channel is None:
            continue
        users = getChannelParticipants(client, channel)
        list.extend(users)
    return list


def removeSuccess(success, users):
    setWithoutSuccess = set(user.username for user in users if user is not None and user.username is not None) - set(user.username 
        for user in success if user is not None and user.username is not None)
    listWithoutSuccess = [user for user in users if user is not None and user.username in setWithoutSuccess]
    return listWithoutSuccess



def finalResolve(error, count=0, limit=0):
    if __name__ == '__main__':
        exit(error)
    else:
        return {'status': False, 'error': error}


def removeUsersAlreadyInChannel(channelUsers, users):
    unique = set(user.username for user in users if user is not None and user.username is not None) - set(user.username
     for user in channelUsers if user is not None and user.username is not None)
    return list(user for user in users if user is not None and user.username is not None and user.username in unique)

def getUsers(peters, online=True, getFrom=[]):
    users = []
    storageUsers = getUsersFromStore()
    usedChannels = []
    getFromAll = (lambda: True, lambda: False)[len(getFrom) > 1]()
    for peter in peters:
        with TelegramClient(peter, api_id, api_hash) as client: 
            channels = getChannels(client)
            userChunk = (lambda: [storageUsers[key] for key in channels.keys() if key in storageUsers.keys()],
                            lambda: [storageUsers[key] for key in getFrom if key in storageUsers.keys()])[len(getFrom) > 1]()
            getFrom = [key for key in getFrom if key not in storageUsers.keys()]
            for user in userChunk:
                users.extend(user)  
            if not online:
                return makeSingle(users)
            workingChannels = (lambda: {key: value for key, value in channels.items() if key in getFrom},
                    lambda: {key: value for key, value in channels.items() if key not in usedChannels})[getFromAll is True]()
            usedChannels.extend(workingChannels.keys())
            if workingChannels:
                users.extend(getAllChannelUsers(client, workingChannels))
            if len(users) >= 10000:
                stashChannelStore()
                return makeSingle(users)
    stashChannelStore()
    return makeSingle(users)        



def untappedAddingPotential(peterLnt, count, limit, userLnt):
    if count < limit:
        return True

def add(peters, channelInto, online=True, getFrom=[], filepath='users.txt', limit=1000):
    # do()
    count = 0
    print('adding has started')  # delete in production
    users = getUsers(peters, online, getFrom)
    removedUsersInChannel = False
    trials = True
    while trials:
        for peter in peters:
            print('using peter ' + peter)
            with TelegramClient(peter, api_id, api_hash) as client:
                if peter == 'dynasties':
                    client.send_message('me', 'Hello, myself!')
                channels = getChannels(client)
                printChannels(channels)  # delete in production
                print('for peter '+peter + ' the users before are: ' + str(len(users)))
                if not users and count <= limit:
                    return finalResolve('No users to add')
                if channelInto not in channels.keys():
                    joinChannel(client, channelInto)
                    continue
                if not removedUsersInChannel:
                    channelUsers = getChannelParticipants(client, channels[channelInto])
                    users = removeUsersAlreadyInChannel(channelUsers, users)
                    print('after removing users from the channel, they are now: '+str(len(users)))
                    removedUsersInChannel = True
                if count < limit:
                    success = addUsersToChannel(client, users, channels[channelInto])
                    count = count + len(success)
                else:
                    return finalResolve('you have exhausted your quota and adding has ended.')
                users = removeSuccess(success, users)
                random.shuffle(users)
                print('successes are '+str(len(success)))
                print('users after accounting for successes are ' + str(len(users)))
                print('peter '+peter+' done and dusted adding.')
            trials = False
        if untappedAddingPotential(len(peters), count, limit, len(users)):
            trials = True
            tick = random.randint(10, 70) * 2
            sleep(tick)
            continue
    print('adding has ended.')
    report = {'status': True, 'data': {
        'usersAdded': count, 'channelAddedTo': channelInto}}
    return report


def joinChannel(client, channelName):
    channelEntity = client.get_entity('t.me/'+channelName)
    client(JoinChannelRequest(channelEntity))

def massJoinChannel(peters, channelName):
    for peter in peters:
        with TelegramClient(peter, api_id, api_hash) as client:
            joinChannel(client, channelName)
            print('peter ' + peter + 'joined channel' + channelName)

def main():
    pass

if __name__ == '__main__':
    peters = ['goodluck1', 'goodluck2', 'goodluck3', 'goodluck4', 'goodluck5']
    random.shuffle(peters)
    #joinChannel(peters, 'successvisa')  
    #'james', 'john', 'mary', 'mike', 'mike10', 'mike20', 'mike4'
    add(peters, 'IdongesitG', getFrom=[])
