import tkinter
from tkinter import filedialog
import os

directories = []
ownCoincidenceList1 = []
ownCoincidenceList2 = []
coincidenceList1 = []
coincidenceList2 = []

def browseDirectory(textField):
    selectedDirectory = filedialog.askdirectory()
    retrieveDirectory(selectedDirectory)
    textField.insert(0, selectedDirectory)

def retrieveDirectory(path):
    directories.append(path)

def showCoincidences(list):
    result = ''
    for x in range(len(list)):
        result += f'\n{list[x]}'
    return result

def checkIfDirectory(directory):
    if os.path.isdir(directory):
        print('Directory confirmed.')
        return True
    else:
        print('NOT a directory.')
        return False

def countValidDirectories(button, option):
    counter = 0
    for x in directories:
        if checkIfDirectory(x):
            counter += 1
            print(f'Directory counter> {counter}')
    if option == "two":
        if counter == 2:
            button.config(state=tkinter.NORMAL)
        else:
            print(f'There are not enough directories to compare. Please, provide at least 2 valid directories.')
    else:
        if counter == 1:
            button.config(state=tkinter.NORMAL)
        else:
            print(f'There is no directory to look into. Please, provide 1 valid directory.')


def getFileList(path):
    list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            list.append(os.path.join(root, file))
    return list

def removeDuplicates(list):
    x = 0
    while x < len(list):
        i = x + 1
        while i < len(list):
            if list[x] == list[i]:
                list.pop(i)
            else:
                i += 1
        x += 1

def debugListByFileName(list):
    x = 0
    while x < len(list):
        i = x + 1
        while i < len(list):
            if os.path.basename(list[x]) == os.path.basename(list[i]):
                list.pop(i)
            else:
                i += 1
        x += 1

def deleteFiles(list):
    for x in range(len(list)):
        if os.path.exists(list[x]):
            os.remove(list[x])
            showTextConsole(f'\nThe following file has been successfully DELETED: {list[x]}')
        else:
            showTextConsole(f'\nThe following file does NOT exist: {list[x]}')

def deleteEmptyDirectories(list):
    dirList = []
    for x in range(len(list)):
        dirList.append(os.path.dirname(list[x]))
    for x in range(len(dirList)):
        if os.path.exists(dirList[x]) and len(os.listdir(dirList[x])) == 0:
            os.rmdir(dirList[x])
            showTextConsole(f'\nThe following directory has been successfully DELETED: {dirList[x]}')

# Functions.
def cleanDir(list):
    showTextConsole('\nCLEANING...')
    deleteFiles(list)
    deleteEmptyDirectories(list)

def smc(path):
    if checkIfDirectory(path):
        if len(ownCoincidenceList1) > 0:
            True
    else:
        return False
    
def showTextConsole(console, text):
    currentText = console.get("1.0", "end").strip()
    if currentText == "":
        console.insert(tkinter.END, text)
    else:
        console.insert(tkinter.END, "\n" + text)

def cleanList(list):
    list.clear()

def clearConsole(console):
    console.delete("1.0", "end")