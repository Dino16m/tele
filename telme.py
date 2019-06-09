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
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser

from telethon.tl.functions.channels import InviteToChannelRequest

test_channel= 'webtrading4'
my_channel = 'UdaraTV'
#api_id = 764531
#api_hash = 'a41f8549c7dd1341613de3569f9796cb'

#peters'
api_id = 872129
api_hash = '1390959115b339a8e20294e3591a8b41'
to_hack = ['binanceexchange', 'LitecoinDiamonD', 'VietnamBitcoinWorld_2' ]

def getChannel(mine, channels):
    for channel in channels:
        if channel == mine:
            return channel
            
with TelegramClient('peters', api_id, api_hash) as client:
    client.send_message('me', 'Hello, myself!')
    channels = {d.entity.username: d.entity
        for d in client.get_dialogs()
        if d.is_channel}

        # choose the one that I want list users from
        
        
    channel = channels[test_channel]
    channel_entity = InputPeerChannel(channel.id, channel.access_hash)
        # get all the users and print them
    for channel in channels:
        if channel in to_hack:
            
            channel = channel
            for u in client.get_participants(channel):
            
                user_to_add = client.get_input_entity(u.id)
                client(InviteToChannelRequest(channel_entity,[user_to_add]))
                sleep(60)
            #print(u.id, u.first_name, u.last_name, u.username)
                
    