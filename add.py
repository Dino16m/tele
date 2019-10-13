from tele import add, chunkify
import random
from threading import Thread

apis = [
	{"key": "764531", "hash": "a41f8549c7dd1341613de3569f9796cb"},
	{"key": "1124248", "hash": "d08aa4a2326763e69767881e67944fc6"},
	{"key": "1050270", "hash": "89054ba2d3597bd33a163c6fed13af36"},
	{"key": "1069414", "hash": "e8a0cec143c3426236a52d0e86fe68fa"},
	{"key": "872129", "hash": "1390959115b339a8e20294e3591a8b41"}
]
standByPeters = ['dynasties', 'dynasty', 'focus', 'focus2', 'prosper', 'prosper2', 'uche', 'uche2', 'uche3', 'uche4']

def init(channelInto, getFrom=[], limit=1000, peters=[]):
	peters = (lambda: peters, lambda: standByPeters)[len(peters) < 20]()
	peterChunks = chunkify(peters, int(len(peters)/5))
	random.shuffle(peterChunks)
	params = []
	count = 0
	for peterChunk in peterChunks:
		state = {}
		api = apis[count % 4]
		count = count + 1
		state['peters'] = peterChunk
		state["channelInto"] = channelInto
		state["api_key"] = api['key']
		state["api_hash"] = api['hash']
		state["getFrom"] = getFrom
		state["limit"] = limit
		params.append(state)
	dispatch(params)


def dispatch(params):
	for param in params:
		print(param)
		exit()
	threads = []
	for x in range(len(params)):
		threads.append(Thread(target=add, args=params[x]))
	for thread in threads:	
		thread.start()

def main():
	init('sucessvisa')

if __name__ == '__main__':
	main()