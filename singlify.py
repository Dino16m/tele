import os
import shutil

def readFromFile(basename, basedir):
    #it is expected that any method that calls this function must have implemented os.path.isfile(filepath)
    filename = basedir+basename
    file = open(filename, "r")
    list = []
    if file.mode == "r":
        lines = file.readlines()
        for line in lines:
            if line is not None and not line == "":
                list.append(line.strip())
        file.close()
    return list
    
def writeToFile(items, basename, basedir):
    filename = basedir + basename
    file = open(filename, "a")
    items.sort()
    for item in items:
        if type(item) == str:
            file.write(item)
            file.write('\n')
        if not type(item) == str and type(item) is not None and type(item.username) is not None:
            if item.username is None:
                continue
            file.write(item.username)
            file.write('\n')
    file.close()
    return True
    
def singlify(listItems):
    singleSet = set(listItems)
    singleList = list(singleSet)
    return singleList
    
def makeSingle(param):
    return singlify(param)

def createFile(filepath):
    if os.path.isfile(filepath):
        return
    file = open(filepath, "w+")
    file.close()
    
def writeSingle(filepath, list=[]):
    basename = os.path.basename(filepath)
    basedir = os.path.dirname(filepath)
    if not os.path.isfile(filepath):
        createFile(filepath)
    repeated = readFromFile(basename, basedir)
    repeated.extend(list)
    singles = singlify(repeated)
    if writeToFile(singles, basename, basedir):
        return len(singles)

def backupUsers(filepath):
    if not os.path.isfile(filepath):
        return False
    basename = os.path.basename(filepath)
    basedir = os.path.dirname(filepath)
    bak = basename + '.bak'
    if os.path.isfile(basedir+bak):
        readOld = readFromFile(bak, basedir)
        readNew = readFromFile(basename, basedir)
        readNew.extend(readOld)
        singles = singlify(readNew)
        try:
            os.remove(basedir+bak)
        except Exception:
            False
        if writeToFile(singles, bak, basedir):
            return basedir + bak
    try:
        shutil.copystat(basedir+basename, basedir+bak)
    except Exception:
        return False 
    return basedir+bak

def commitSuccess(success, filepath):
    if not os.path.isfile(filepath):
        return False
    basename = os.path.basename(filepath)
    basedir = os.path.dirname(filepath)
    try:
        os.remove(filepath)
    except Exception:
        return False
    if writeToFile(success, basename, basedir):
        return True

            
