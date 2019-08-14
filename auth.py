"""This is the modeul for the addition proper."""

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


#api_id = 872129
#api_hash = '1390959115b339a8e20294e3591a8b41'

api_id = 764531
api_hash = 'a41f8549c7dd1341613de3569f9796cb'
master = 'micky'
code = ''

class GetCode(object):
	"""docstring for ClassName."""
	def __init__(self, code):
		self.code = code

	def __call__(self):
		return self.code
		
		
def sendCodeRequest(phone, session='dynasties'):
	with TelegramClient(session, api_id, api_hash) as client:
		status = client.send_code_request(phone)
		if type(status.phone_code_hash) == str:
			return status.phone_code_hash
		return False

def signIn(phone, code, session, phone_code_hash=None):
	getCode = GetCode(code)	
	client = TelegramClient(session, api_id, api_hash).start(phone=phone, code_callback=getCode)
	client.send_message('me', 'master, I made it')

phone = '+234 812 246 3202'
session = 'dynasties'
hash = sendCodeRequest(phone)
if hash:
	code = input('what is the code you received: ')
	signIn(phone, code, session, phone_code_hash=hash)