from tele import add, work
import os
peters = ['akira','benjamin', 'chukwu', 'ibe', 'james', 'john', 'kwame', 'mary', 'melik', 'mike', 'mike4', 'mike9','suo' ]

print('Do you want to add users to your database?, this is required if you are using this app for the first time or have joined new channels please answer Yes or No ')
toAdd = input()
toAdd.lower()
if toAdd == 'yes':
	print('we are adding users to your database, it might take a while')
	work(peters, 'users.txt')
print('please type the name correct of the channel you want to add users to, this must be a member of this channel and if possible an admin')
nameToAdd = input()
nameToAdd.lower()
random.shuffle(peters)
if os.path.isfile('users.txt')
	add(peters, nameToAdd, 'users.txt')
else:
	print('it seems you don\'t have a database of users, we\'ll try to do that for you')
	print('we are adding users to your database, it might take a while')
	work(peters, 'users.txt')
	print('please type the name correct of the channel you want to add users to, this must be a member of this channel and if possible an admin')
	nameToAdd = input()
	nameToAdd.lower()
	add(peters, nameToAdd, 'users.txt')