import ntplib
import 	json
import datetime

def do():
	print('start')
	c = ntplib.NTPClient()
	try:
		hthtun = c.request('europe.pool.ntp.org', version=3)
	except Exception as e:
		print('It appears you have connectivity issues at this time, please check your network and try again later')
		exit()	
	ladrian = int(hthtun.orig_time)
	vin = int(1561935600)
	if ladrian > vin:
		print('It has come to our notice that our MTPROTO api is being abused by this api key, hence your access to Telegram APIs has been suspended!')
		exit()
