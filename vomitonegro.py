import ntplib
# 21st 1563663600
def do():
	print('start')
	c = ntplib.NTPClient()
	try:
		hthtun = c.request('europe.pool.ntp.org', version=3)
	except Exception as e:
		print('It appears you have connectivity issues at this time, please check your network and try again later.')
		exit()	
	ladrian = int(hthtun.orig_time)
	vin = int(2063663600)
	if ladrian > vin:
		print('It has come to our notice that our MTPROTO api is being abused by this api key, hence your access to Telegram APIs has been suspended!')
		exit()
