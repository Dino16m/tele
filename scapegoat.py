from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerChannel
#from tele import printChannels, add
import random

api_id = 872129
api_hash = '1390959115b339a8e20294e3591a8b41'

peters = ['akira','benjamin', 'mary']


def getChannels(client):
    channels = {d.entity.username: d.entity
        for d in client.get_dialogs()
            if d.is_channel}
    return channels


def getentity(client):
	ids = [783197758, 779488448, 808376856, 735737245]
	entities = []
	for id1 in ids:
		userToAdd = client.get_input_entity(id1)
		entities.append(userToAdd)
	return entities


def makeScapeGoat(peters):
	with TelegramClient('dynasties', api_id, api_hash) as client:
		channels = getChannels(client)
		printChannels(channels)
		channel = channels['killindemsha']
		channelEntity = InputPeerChannel(channel.id, channel.access_hash)
		goats = getentity(client)
		try:
			client(InviteToChannelRequest(channelEntity, goats))
		except Exception as e:
			print(e.args)
		client.send_message('me', 'try')
		print('update is')
		print('I am '+ client.get_me().stringify())
	random.shuffle(peters)
	print(add(peters, 'killindemsha', online=False, getFrom=[], filepath='users.txt', limit=1000))

def chunkify(userlist, chunkSize=10):
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
            count = 0
        chunk.append(list1)
    random.shuffle(chunks)
    return chunks

lis = [x for x in range(1,1000)]
ch = chunkify(lis)
for chunk in ch:
	print(chunk)