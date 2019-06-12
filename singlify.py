import os

def readFromFile(filename):
    file = open(filename, "r")
    if file.mode == "r":
        lines = file.readlines()
        list = []
        for line in lines:
            list.append(line)
        file.close()
        os.rename(filename, 'old_'+filename)
        return list
    
def writeToFile(items, filename):
    file = open(filename, "a")
    for item in items:
        if type(item) == str:
            file.write(item)
            #file.write('\n')
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
def work():
    repeated = readFromFile('users.txt')
    singles = singlify(repeated)
    if writeToFile(singles, 'users.txt'):
        print('You now have unique files')

work()