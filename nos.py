from telethon.sync import TelegramClient
api_id = 872129
api_hash = '1390959115b339a8e20294e3591a8b41'
peters = ['1','2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12','13' ,'14', '15', '16', '17', '18', '19', '20' ]
for peter in peters:
	with TelegramClient(peter, api_id, api_hash) as client:
		client.send_message('me', 'Hello, maker!')