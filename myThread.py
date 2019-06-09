from tele import work
import asyncio
import threading
import time

class myThread(threading.Thread):
    
    def __init__(self, peter, loop):
        threading.Thread.__init__(self)
        asyncio.set_event_loop(loop)
        self.peter = []
        self.peter.append(peter)
    
    def run(self):
        work(self.peter)

        