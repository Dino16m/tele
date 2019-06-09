from threading import Thread
import asyncio
from tele import work

peters = ['akira','benjamin', 'chukwu', 'ibe', 'james', 'john', 'kwame', 'mary', 'melik', 'mike', 'mike4', 'mike9','suo','sampson' ]
threads = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,25]
i = 0

async def callTele(peter):
    await work([peter])
    
def workhere(loop, peter):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(callTele(peter))
    

    
for peter in peters:
    loop = asyncio.new_event_loop()
    thread = Thread( args=(loop, peter), target=workhere)
    threads[i]=thread
    thread.start()
    
    
    



