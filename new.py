

li = ["a", "b", "c", "d", "e", "f", "g"]

channels = {"a": "b", "c": "d", "e": "f"}

storey = {"a": "b", "c": "d", "e": "f", "g": "h", "i": "j", "k": "l"}
li = ["a", "b", "c"]
store = ''

new = {key: value for key, value in channels.items() if key in li}

s = set(value for key, value in storey.items() if key in li)


def setStore(val):
	global store 
	store = val

setStore('lol')
print(store)

def getStore():
	return store

print(getStore())