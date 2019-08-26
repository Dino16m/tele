import os
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
        fcntl.flock(file, fcntl.LOCK_EX)
        channelDict = pickle.load(file)
        fcntl.flock(file, fcntl.LOCK_UN)
    return channelDict
    
def makeSingle(users):
    usernameSet = set(user.username for user in users if user is not None and user.username is not None)
    usersList = [users for user in users if user.username in usernameSet]
    return usersList


            
