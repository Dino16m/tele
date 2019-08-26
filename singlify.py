import os
import shutil
import pickle
import fcntl


def storeUsers(channelDict, filename="store.pkl"):
    with open(filename, "wb") as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        pickle.dump(channelDict, file)
        fcntl.flock(file, fcntl.LOCK_UN)

def getUsersFromStore(filename="store.pkl"):
    if not os.path.isfile(filename):
        return {}
    with open(filename, "rb") as file:
        channelDict = pickle.load(file)
    return channelDict
    


            
