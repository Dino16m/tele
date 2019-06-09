#api_id = 872129
#api_hash = '1390959115b339a8e20294e3591a8b41'
#app_title = Telchat
#short_name = Telchat1

#mine below, peters'above

#api_id = 764531
#api_hash = a41f8549c7dd1341613de3569f9796cb
#app_title = telchannel
#app_name = telchan2020
#test_channel= 'webtrading4'
#my channel = 'UdaraTV'

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

from telethon.tl.functions.channels import InviteToChannelRequest

test_channel= 'webtrading4'
my_channel = 'UdaraTV'
#api_id = 764531
#api_hash = 'a41f8549c7dd1341613de3569f9796cb'

#peters'
api_id = 872129
api_hash = '1390959115b339a8e20294e3591a8b41'
#to_hack = ['binanceexchange', 'LitecoinDiamonD', 'VietnamBitcoinWorld_2' ]

def login(name, api_id, api_hash):
    client = TelegramClient(name, api_id, api_hash)
    # if not client.is_user_authorized():
    #     client.send_code_request(phone)
    #     client.sign_in(phone, input('Enter the code: '))
    return client
    
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
    
def addUsersToCsv(users, filename):
    file = open(filename, "a")
    for user in users:
        if user.username == None:
            continue
        file.write(user.username)
        file.write('\n')
    file.close()
    return True
    
def addUsersToChannel(client, users, channel):
    channelEntity = InputPeerChannel(channel.id, channel.access_hash)
    count = 0
    error = False
    for user in users:
        if type(user)==str:
            userToAdd = client.get_input_entity(user)
        else:
            userToAdd = client.get_input_entity(user.id)
        try:
           client(InviteToChannelRequest(channelEntity,[userToAdd]))
        except Exception as e:
            print(e.args)
	    error = True
        finally:
	    if not error == True:
            	print('adding users to channel  ')
	    error = False
        if count >= 50 :
            sleep(random.randint(10,61)*2)
            count = 0
        count = count + 1
    return True
    
def getUsersFromCsv(filePath):
    file = open(filePath, "r")
    if file.mode == "r":
        lines = file.readlines()
        users = []
        for line in lines:
            users.append(line)
            
    return users

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
    for channel in channels:
        if channel == None:
            continue
        users = getChannelParticipants(client, channel)
        addUsersToCsv(users, 'users.txt')
    return True
        
def add(peters):
    #peters = people
    for peter in peters:
        with TelegramClient(peter, api_id, api_hash) as client:
            client.send_message('me', 'Hello, myself!')
            channels = getChannels(client)
            users = getUsersFromCsv('users.txt')
            #users = getChannelParticipants(client, channels['dualminecom'])
            #addUsersToCsv(users, 'users.txt')
            addUsersToChannel(client, users, channels['killindem'])
            print('peter '+peter+' done and dusted adding')
    
def work(people):
    #peters = people
    for peter in peters:
        with TelegramClient(peter, api_id, api_hash) as client:
            client.send_message('me', 'Hello, myself!')
            channels = getChannels(client)
            printChannels(channels)
            #users = getUsersFromCsv('users.txt')
            getAllChannelUsers(client, channels)
            #users = getChannelParticipants(client, channels['dualminecom'])
            #addUsersToCsv(users, 'users.txt')
            #addUsersToChannel(client, users, channels['webtrading4'])
            print('peter '+peter+' done and dusted writing')
    
peters = ['akira','benjamin', 'chukwu', 'ibe', 'james', 'john', 'kwame', 'mary', 'melik', 'mike', 'mike4', 'mike9','suo','sampson' ]
#work(peters)
add(peters)







