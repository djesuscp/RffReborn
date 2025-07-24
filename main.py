import os

directories = []
coincidences = []

def retrieveDirectories():
    i = 0
    while i < 2:
        path = input(f'Specify path: ')
        if path == 0:
            break
        else:
            directories.append(path)
        i += 1

def checkIfDirectory(directory):
    if os.path.isdir(directory):
        print('Directory confirmed.')
        return True
    else:
        print('NOT a directory.')
        return False

def countValidDirectories():
    counter = 0
    for x in directories:
        if checkIfDirectory(x):
            counter += 1
            print(f'Directory counter> {counter}')
    if counter <= 2:
        return True
    else:
        print(f'There are not enough directories to compare. Please, provide at least 2 valid directories.')
        return False

def getFileList(path):
    list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            list.append(os.path.join(root, file))
    return list

def compareLists(list1, list2):
    coincidences = []
    for x in range(len(list1)):
        fileName1 = os.path.basename(list1[x])
        fileSize1 = os.path.getsize(list1[x])
        for i in range(len(list2)):
            fileName2 = os.path.basename(list2[i])
            fileSize2 = os.path.getsize(list2[i])
            if fileName1 == fileName2 and fileSize1 == fileSize2:
                coincidences.append(fileName2)
    print('COINCIDENCES: ', coincidences)


if __name__ == "__main__":
    retrieveDirectories()
    compareLists(getFileList(directories[0]), getFileList(directories[1]))
