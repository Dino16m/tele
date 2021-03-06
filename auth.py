"""This is the module for the addition proper."""

from telethon.sync import TelegramClient
import argparse


api_id = 872129
api_hash = '1390959115b339a8e20294e3591a8b41'

api_id = '764531'
api_hash = 'a41f8549c7dd1341613de3569f9796cb'    

class getCode(object):
	"""docstring for getCode"""
	def __init__(self, code):
		super(ClassName, self).__init__()
		self.code = code
	def __call__(self):
		return self.code
		
def sendCodeRequest(phone, session='dynasties'):
	with TelegramClient(session, api_id, api_hash) as client:
		print('logged in ' + session)
		status = client.send_code_request(phone)
		client.disconnect()
		if type(status.phone_code_hash) == str:
			return True
	return False

def signIn(code, phone, session):
	code_callback = getCode(code)
	client = TelegramClient(session, api_id, api_hash).start(phone=phone, code_callback=code_callback)
	client.send_message('me', 'signed in, you are ' + session)

def auth(number, session):
	hash = sendCodeRequest(number)
	if hash:
		code = input('what is the code you received for user ' + session + ': ')
		signIn(code, number, session)
		print('done')
	else:
		print('no code was sent for user ' + session + ': ')

def main():
	#'Benneth','damian', 'damian2', 'dynasties', 'dynasty', 'focus', 'focus2', 'kolynz', 'mick1', 'ocv', 'ocv2', 'prosper2', 'trace', 'uche', 'uche2',
	parser = argparse.ArgumentParser(description='Add arguments for auth')
	parser.add_argument('--users', nargs='*', help='the group to add to', default=[])
	args = parser.parse_args()
	sessions = args.users
	success = 0
	for session in sessions:
		with TelegramClient(session, api_id, api_hash) as client:
			print('signed in, you are ' + session)
			success += 1
			client.send_message('me', 'signed in, you are ' + session)
	print('succcess is ', str(success))

if __name__ == '__main__':
	main()
	#auth('+2348162539708', 'hizanon') +2348115716657
	#print(getCode())
	
