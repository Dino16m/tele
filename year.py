WEEKDAYS = ("Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun")

EPOCH = 1970

given_year = 2004
given_month = 1
given_date = 10

days = 3
for i in range(given_year - 1970):
	days += math.floor(((1970 + i) % 4) / 4) + 365
if 

print(WEEKDAYS[days % 6])