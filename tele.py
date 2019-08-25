import os
import random
from time import sleep
from myexceptions import OutOfUserException
from singlify import backupUsers, readFromFile, writeSingle, writeToFile
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import InputPeerChannel
from vomitonegro import do


#api_id = 872129
#api_hash = '1390959115b339a8e20294e3591a8b41'

api_id = 764531
api_hash = 'a41f8549c7dd1341613de3569f9796cb'


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
                if u.username is not None:
                    users.append(u.username)
    except Exception as e:
        print(e.args)
    return users


def addUsersToCsv(users, filepath, singlify=False):
    basename = os.path.basename(filepath)
    basedir = os.path.dirname(filepath)
    if singlify:
        return writeSingle(filepath, users)
    else:
        return writeToFile(users, basename, basedir)


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


def getUserEntities(client, users):
    list = []
    for user in users:
        if type(user) == str:
            try:
                userToAdd = client.get_input_entity(user)
                list.append(userToAdd)
            except Exception:
                continue
        else:
            userToAdd = client.get_input_entity(user.id)
            list.append(userToAdd)
    return chunkify(list)


def convertEntity(client, entities):
    returnable = []
    for entity in entities:
        user = client.get_entity(entity)
        if user.username is not None:
            returnable.append(user.username)
    return returnable


def getSuccessFromUpdate(update):
    if len(update) < 1:
        return []
    users = []
    for u in update:
        if u.username is not None:
            users.append(u.username)
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
    usersToAdd = getUserEntities(client, users)
    for usersToAdd1 in usersToAdd:
        try:
            update = client(InviteToChannelRequest(channelEntity, usersToAdd1))

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


def getUsersFromCsv(filepath):
    basename = os.path.basename(filepath)
    basedir = os.path.dirname(filepath)
    if not os.path.isfile(basedir + basename):
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
        if i >= range:
            break
        list.append(user)
        i = i + 1
    return list


def getAllChannelUsers(client, channels):
    list = []
    for channel in channels:
        if channel is None:
            continue
        users = getChannelParticipants(client, channel)
        list.extend(users)
    return list


def removeSuccess(success, users):
    setWithoutSuccess = set(users) - set(success)
    listWithoutSuccess = list(setWithoutSuccess)
    return listWithoutSuccess


def numberOfUsers(filepath):
    if not os.path.isfile(filepath):
        return 0
    basename = os.path.basename(filepath)
    basedir = os.path.dirname(filepath)
    return len(readFromFile(basename, basedir))


def backup(filepath):
    return backupUsers(filepath)


def finalResolve(error, count=0, limit=0):
    if __name__ == '__main__':
        exit(error)
    else:
        return {'status': False, 'error': error}


def removeUsersAlreadyInChannel(channelUsers, users):
    channelUsersList = []
    for channelUser in channelUsers:
        if channelUser is None:
            continue
        if type(channelUser) == str:
            channelUsersList.append(channelUser)
        if not type(channelUser) == str and channelUser.username is not None:
            channelUsersList.append(channelUser.username)
    unique = set(users) - set(channelUsersList)
    return list(unique)


def getUsers(source, channels={}, online=True, getFrom=[], usedChannels=[]):
    users = []
    if online and not channels:
        return users
    sourceChannels = []
    if online and getFrom:
        for getFrom1 in getFrom:
            if getFrom1 in channels.keys():
                sourceChannels.append(channels[getFrom1])
                getFrom.remove(getFrom1)
    if online and not getFrom:
        sourceChannelsSet = set(channels) - set(usedChannels)
        sourceChannels = list(sourceChannelsSet)
        usedChannels.extend(sourceChannels)
    if online and sourceChannels:
        users = getAllChannelUsers(source, sourceChannels)
    if not online:
        if not os.path.isfile(source):
            return users
        users = getUsersFromCsv(source)
    return users


def untappedAddingPotential(peterLnt, count, limit, userLnt):
    if count < limit:
        return True
    weight = 10
    if count < limit:
        weight += 1
    else:
        weight -= 1
    if (peterLnt * 150) < count:
        weight += 1
    else:
        weight -= 1
    if (userLnt-count) > 50:
        weight += 1
    if weight >= 10:
        return True
    return False


def add(peters, channelInto, online=True, getFrom=[], filepath='users.txt', limit=1000):
    # do()
    count = 0
    print('adding has started')  # delete in production
    # (lambda: getUsers(filepath, online=False), lambda: [])[online is True]()
    users = []
    removedUsersInChannel = False
    usedChannels = []
    trials = True
    while trials:
        for peter in peters:
            print('using peter ' + peter)
            with TelegramClient(peter, api_id, api_hash) as client:
                #client.send_message('me', 'Hello, myself!')
                channels = getChannels(client)
                printChannels(channels)  # delete in production
                tmpUsers = (lambda: users, lambda: getUsers(
                    client, channels, online, getFrom, usedChannels))[online is True]()
                users = list(set(users + tmpUsers))
                print('for peter '+peter +
                      ' the users before are: ' + str(len(users)))
                if not users and count <= limit:
                    continue
                if channelInto not in channels.keys():
                    continue
                if channelInto not in channels.keys() and peters[len(peters)-1] == peter:
                    return finalResolve('invalid channel name')
                if not removedUsersInChannel:
                    channelUsers = getChannelParticipants(
                        client, channels[channelInto])
                    users = removeUsersAlreadyInChannel(channelUsers, users)
                    print(
                        'after removing users from the channel, they are now: '+str(len(users)))
                    removedUsersInChannel = True
                if count < limit:
                    success = addUsersToChannel(
                        client, users, channels[channelInto])
                    count = count + len(success)
                else:
                    return finalResolve('you have exhausted your quota and adding has ended.')
                if not users and (peters[len(peters)-1] == peter and count < limit):
                    raise OutOfUserException(count, limit)
                users = removeSuccess(success, users)
                random.shuffle(users)
                print('successes are '+str(len(success)))
                print('users after accounting for successes are ' + str(len(users)))
                print('peter '+peter+' done and dusted adding.')
            removedUsersInChannel = False
            trials = False
        if untappedAddingPotential(len(peters), count, limit, len(users)):
            trials = True
            random.shuffle(peters)
            continue
    print('adding has ended.')
    report = {'status': True, 'data': {
        'usersAdded': count, 'channelAddedTo': channelInto}}
    return report


def work(peters, getFrom=[], filepath='users.txt'):
    """The method stores users from channels channels specified by the getFrom param avove to a given file."""
    # do()
    print('storing users started')
    allUsers = []
    number = 0
    usedChannels = []
    for peter in peters:
        with TelegramClient(peter, api_id, api_hash) as client:
            client.send_message('me', 'Hello, maker!')
            channels = getChannels(client)
            printChannels(channels)
            users = getUsers(client, channels, True, getFrom, usedChannels)
            allUsers.extend(users)
            if allUsers:
                number = number + addUsersToCsv(allUsers, filepath, True)
            print('peter '+peter+' done and dusted writing')
    print('storing users ended')
    return number


def joinChannel(peters, channelName):
    for peter in peters:
        with TelegramClient(peter, api_id, api_hash) as client:
            channelEntity = client.get_entity('t.me/'+channelName)
            client(JoinChannelRequest(channelEntity))
            print('peter ' + peter + 'joined channel' + channelName)


if __name__ == '__main__':
    peters = ['dynasties', '12', '13', '5', '7']
    #joinChannel(peters, 'successvisa')  
    #'james', 'john', 'mary', 'mike', 'mike10', 'mike20', 'mike4'
    add(peters, 'successvisa', getFrom=[])
