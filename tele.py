import asyncio
import random 
from time import sleep 
from singlify import getUsersFromStore, storeUsers, makeSingle 
from telethon.sync import TelegramClient 
from telethon.tl.functions.channels import InviteToChannelRequest 
from telethon.tl.functions.channels import JoinChannelRequest 
from telethon.tl.types import InputPeerChannel, InputPeerUser
from telethon import types
#from vomitonegro import do
from threading import Thread
from datetime import datetime, timedelta
import argparse
import pytz

api_id = 872129
api_hash = '1390959115b339a8e20294e3591a8b41'

#api_id = 1050270
#api_hash = '89054ba2d3597bd33a163c6fed13af36'
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

def stashChannelStore(storageUsers=[]):
    global channelStore
    storeSet = set(channelStore) - set(storageUsers)
    store = {key: value for key, value in channelStore.items() if key in storeSet}
    if store:
        thread = Thread(target=storeUsers, args=[store])
        thread.start()


def getChannelParticipants(client, channel):
    users = []
    try:
        for u in client.get_participants(channel):
            if not u.bot and not u.scam and not u.restricted and not u.min and not u.support and not u.deleted:
                if u.username is not None:
                    users.append(u)
    except Exception as e:
        print(e.args)
    appendToChannelStore(channel, users)
    return users

def chunkify(userlist, chunkSize=50):
    chunks = [[]]
    random.shuffle(userlist)
    count = 0
    for list1 in userlist:
        if count < chunkSize:
            chunk = chunks[-1]
            count = count + 1
        else:
            chunks.append([])
            chunk = chunks[-1]
            count = 1
        chunk.append(list1)
    random.shuffle(chunks)
    return chunks

def printUsers(chunk):
    for user in chunk:
        print(user.stringify())

def rest(t=4):
    sleep(t)
    return True

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

def userWasActive(status, within=2):  # within is in days
    if not isinstance(status, types.UserStatusOffline):
        return True
    lastSeen = status.was_online
    daysAgo = pytz.utc.localize(datetime.today()) - timedelta(days=within)
    return lastSeen > daysAgo

def addUsersToChannel(client, users, channel):
    channelEntity = InputPeerChannel(channel.id, channel.access_hash)
    count = 0
    error = False
    success = []
    random.shuffle(users)
    us = [client.get_input_entity(user.username) for user in users[:50] if user.username is not None and rest() and userWasActive(user.status)]
    #us = [InputPeerUser(user_id=user.id, access_hash=user.access_hash) for user in users if user.username is not None]
    usersToAdd = chunkify(us, 20)
    random.shuffle(usersToAdd)
    for usersToAdd1 in usersToAdd:
        try:
            update = client(InviteToChannelRequest(channelEntity, usersToAdd1))
            sleep(3)
        except Exception as e:
            print(e.args)
            error = True
        finally:
            if not error:
                printAddStatus(len(update.users))
                success.extend(getSuccessFromUpdate(update.users))
            error = False
        
        if count >= 500:
            break
        print(str(count))
        count = count + 1
    sleep(20)
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
    getFromAll = False if len(getFrom) > 1 else True
    for peter in peters:
        with TelegramClient(peter, api_id, api_hash) as client: 
            channels = getChannels(client)
            if len(getFrom) > 1:
                for getFrom1 in getFrom:
                    print("getFrom is: ", getFrom1)
                    if getFrom1 not in channels.keys():
                        joinChannel(client, getFrom1)
            channels = getChannels(client)
            userChunk = (lambda: [storageUsers[key] for key in channels.keys() if key in storageUsers.keys()],
                            lambda: [storageUsers[key] for key in getFrom if key in storageUsers.keys()])[len(getFrom) > 1]()
            getFrom = [value for value in getFrom if value not in storageUsers.keys()]
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
    stashChannelStore(storageUsers)
    return makeSingle(users)     



def untappedAddingPotential(peterLnt, count, limit, userLnt):
    if count < limit:
        return True

def add(peters, channelInto, online=True, getFrom=[], limit=1000, api_id=api_id, api_hash=api_hash):
    loop = asyncio.get_event_loop()
    count = 0
    print('adding has started')  # delete in production
    users = getUsers(peters, online, getFrom)
    removedUsersInChannel = False
    trials = 0
    while trials < 100:
        random.shuffle(peters)
        for peter in peters:
            print('using peter ' + peter)
            with TelegramClient(peter, api_id, api_hash, loop=loop) as client:
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
                    removedUsersInChannel = False
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
        if untappedAddingPotential(len(peters), count, limit, len(users)):
            trials = trials + 1
            tick = random.randint(30, 50) * 2
            sleep(tick)
            continue
        trials = 100
    print('adding has ended.')
    report = {'status': True, 'data': {
        'usersAdded': count, 'channelAddedTo': channelInto}}
    return report


def joinChannel(client, channelName):
    channelEntity = client.get_input_entity('t.me/'+channelName)
    client(JoinChannelRequest(channelEntity))

def massJoinChannel(peters, channelName):
    for peter in peters:
        with TelegramClient(peter, api_id, api_hash) as client:
            joinChannel(client, channelName)
            print('peter ' + peter + 'joined channel' + channelName)

def main():
    parser = argparse.ArgumentParser(description='Add arguments for adding')
    parser.add_argument('--ingroup', type=str, help='the group to add to', default=None)
    parser.add_argument('--getfrom', nargs='*', default=[], help='the groups to get users from, it adds to the default')
    parser.add_argument('--ogetfrom', nargs='*', default=[], help='the groups to get users from, it adds the overrides the default')
    parser.add_argument('--peters', nargs='*', default=[], help='the users to add with, adds them to default')
    parser.add_argument('--opeters', nargs='*', default=[], help='the users to add with, overrides default')
    args = parser.parse_args()
    ingroup = args.ingroup
    getfrom = args.getfrom
    ogetfrom = args.ogetfrom
    peters = args.peters
    opeters = args.opeters
    defaultPeters = ['Benneth', 'damian', 'damian2', 'dynasties', 'dynasty', 
            'focus', 'focus2', 'kolynz', 'mick1', 'ocv', 'ocv2', 'trace', 
            'coco1', 'coco2', 'coco3', 'coco4', 'coco5', 'coco6', 'uche', 'uche2']
    defaultGetFrom = []
    peters = opeters or defaultPeters + peters
    #peters = ['mick1', 'mick2', 'kelvin', 'damian', 'damian2', 'Benneth', 'Bobby']
    #peters = ['tracee']
    inGroup = ingroup or 'zether_trading'
    getFrom = ogetfrom or defaultGetFrom + getfrom
    random.shuffle(peters)
    add(peters, inGroup, getFrom=getFrom)

if __name__ == '__main__':
    main()
    

