import os
import shutil

def readFromFile(basename, basedir):
    #it is expected that any method that calls this function must have implemented os.path.isfile(filepath)
    file = open(filename, "r")
    list = []
    if file.mode == "r":
        lines = file.readlines()
        for line in lines:
            list.append(line)
        file.close()
    return list
    
def writeToFile(items, basename, basedir):
    filename = basedir + basename
    file = open(filename, "a")
    for item in items:
        if type(item) == str:
            file.write(item)
        if not type(item) == str and not type(item) == None:
            file.write(item.username)
    file.close()
    return True
    
def singlify(listItems):
    single = []
    for listItem in listItems:
        if not listItem in single:
            single.append(listItem)
    return single
    
def makeSingle(param):
    return singlify(param)
    
def writeSingle(filepath, list=[]):
    basename = os.path.basename(filepath)
    basedir = os.path.dirname(filepath)
    if not os.path.isfile(filepath):
        return False
    repeated = readFromFile(basename, basedir)
    repeated.extend(lsit)
    singles = singlify(repeated)
    if writeToFile(singles, basename, basedir):
        return len(singles)

def backupUsers(filepath):
    if not os.path.isfile(filepath):
        return False
    basename = os.path.basename(filepath)
    basedir = os.path.basedir(filepath)
    bak = basename + '.bak'
    if os.path.isfile(basedir+bak):
        readOld = readFromFile(bak, basedir)
        readNew = readFromFile(basename, basedir)
        readNew.extend(readOld)
        singles = singlify(readNew)
        try:
            os.remove(basedir+bak)
        except Exception as e:
            False
        if writeToFile(singles, bak, basedir):
            return basedir + bak
    try:
        shutil.copystat(basedir+basename, basedir+bak)
    except Exception as e:
        return False 
    return basedir+bak

def commitSuccess(success, filepath):
    if not os.path.isfile(filepath):
        return False
    basename = os.path.basename(filepath)
    basedir = os.path.basedir(filepath)
    try:
        os.remove(filepath)
    except Exception as e:
        return False
    if writeToFile(success, basename, basedir):
        return True

            
