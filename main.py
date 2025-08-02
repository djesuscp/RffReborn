import tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import filedialog
import os
import time

directories = []
coincidenceList1 = []
coincidenceList2 = []

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

def countValidDirectories():
    counter = 0
    for x in directories:
        if checkIfDirectory(x):
            counter += 1
            print(f'Directory counter> {counter}')
    if counter == 2:
        startButton.config(state=tkinter.NORMAL)
    else:
        print(f'There are not enough directories to compare. Please, provide at least 2 valid directories.')

def getFileList(path):
    list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            list.append(os.path.join(root, file))
    return list

def compareLists():
    list1 = getFileList(directories[0])
    list2 = getFileList(directories[1])
    for x in range(len(list1)):
        fileName1 = os.path.basename(list1[x])
        fileSize1 = os.path.getsize(list1[x])
        for i in range(len(list2)):
            fileName2 = os.path.basename(list2[i])
            fileSize2 = os.path.getsize(list2[i])
            if fileName1 == fileName2 and fileSize1 == fileSize2:
                coincidenceList1.append(list1[x])
                coincidenceList2.append(list2[i])

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
def browseDirectory(field, fieldRef, operation):
    selectedDirectory = filedialog.askdirectory()
    if operation == 0:
        retrieveDirectory(selectedDirectory)
        field.insert(0, selectedDirectory)
        showTextConsole(f'{fieldRef} selected directory is: ' + selectedDirectory)
        countValidDirectories()
    else:
        field.insert(0, selectedDirectory)
        showTextConsole(f'{fieldRef} selected directory is: ' + selectedDirectory)
        sortMixButton.config(state=tkinter.NORMAL)

def showTextConsole(text):
    currentText = console.get("1.0", "end").strip()
    if currentText == "":
        console.insert(tkinter.END, text)
    else:
        console.insert(tkinter.END, "\n" + text)

def showSearchResults():
    compareLists()
    showTextConsole('\n---------------\nLIST OF REPEATED FILES IN DIR1:')
    showTextConsole(showCoincidences(coincidenceList1))
    showTextConsole('\nEND OF DIR1 LIST.')
    showTextConsole('\n---------------\nLIST OF REPEATED FILES IN DIR2:')
    showTextConsole(showCoincidences(coincidenceList2))
    showTextConsole('\nEND OF DIR2 LIST.')
    deleteButton1.config(state=tkinter.NORMAL)
    deleteButton2.config(state=tkinter.NORMAL)

def cleanDir(num):
    showTextConsole('\nCLEANING...')
    if num == 1:
        deleteFiles(coincidenceList1)
        deleteEmptyDirectories(coincidenceList1)
    else:
        deleteFiles(coincidenceList2)
        deleteEmptyDirectories(coincidenceList2)

# GUI.
# Main screen configuration.
mainScreen = tkinter.Tk()
mainScreen.title("RffReborn")
mainScreen.geometry("1600x800")
mainScreen.configure(bg="#000000")

# Frames.
# frame1 = tkinter.Frame(mainScreen, borderwidth=2, relief='solid')
# frame1.grid(row=0, column=0, padx=10, pady=10)

# Labels.
title = tkinter.Label(mainScreen, text="RffReborn", font=("Arial", 20), bg="#000000", fg="#FFFFFF")
title.grid(row=0, column=0, columnspan=7)
subtitle1 = tkinter.Label(mainScreen, text="---- Compare directories section ----", font=("Arial", 16), bg="#000000", fg="#FFFFFF")
subtitle1.grid(row=1, column=0, columnspan=3)
text1 = tkinter.Label(mainScreen, text="In this section, you will find 2 fields in which you should browse\nthe directories you want to compare. This program will find out\nthe repeated files and let the user decide wether to\ndelete them from one or both of the directories.", font=("Arial", 10), bg="#000000", fg="#FFFFFF")
text1.grid(row=2, column=0, columnspan=3)
subtitle2 = tkinter.Label(mainScreen, text="---- Sort and Mix section ----", font=("Arial", 16), bg="#000000", fg="#FFFFFF")
subtitle2.grid(row=1, column=3, columnspan=3)
text2 = tkinter.Label(mainScreen, text="In this section, there is a field in which you must specify\nthe new directory path. Once the button \"SMC\" (sort, mix and clean)\n is pressed, the program will make a security copy in the selected path,\nsaving all the files properly without repeating any of them.\nFinally, the program will clean the original directories to save espace for the user.", font=("Arial", 10), bg="#000000", fg="#FFFFFF")
text2.grid(row=2, column=3, columnspan=3)

# Text Fields.
field1 = tkinter.Entry(mainScreen, width=60)
field2 = tkinter.Entry(mainScreen, width=60)
field3 = tkinter.Entry(mainScreen, width=60)
field1.grid(row=3, column=0)
field2.grid(row=4, column=0)
field3.grid(row=3, column=3)

# Text Area.
console = tkinter.Text(mainScreen, font=("courier new", 14), bg="#FFFFFF", fg="#000000")
console.grid(row=7, column=0, columnspan=6)

# Buttons.
browseButton1 = Button(mainScreen, text="Browse...", command = lambda: browseDirectory(field1, 'First', 0))
browseButton1.grid(row=3, column=1)
browseButton2 = Button(mainScreen, text="Browse...", command = lambda: browseDirectory(field2, 'Second', 0))
browseButton2.grid(row=4, column=1)
browseButton3 = Button(mainScreen, text="Browse...", command = lambda: browseDirectory(field3, 'New', 1))
browseButton3.grid(row=3, column=4)
startButton = Button(mainScreen, text="Start Search", command = showSearchResults)
startButton.grid(row=5, column=0, columnspan=3)
startButton.config(state=tkinter.DISABLED)
deleteButton1 = Button(mainScreen, text="Clean Dir1", command = lambda: cleanDir(1))
deleteButton1.grid(row=6, column=0)
deleteButton1.config(state=tkinter.DISABLED)
deleteButton2 = Button(mainScreen, text="Clean Dir2", command = lambda: cleanDir(2))
deleteButton2.grid(row=6, column=1)
deleteButton2.config(state=tkinter.DISABLED)
sortMixButton = Button(mainScreen, text="SMC", command = lambda: cleanDir(2))
sortMixButton.grid(row=5, column=3, columnspan=3)
sortMixButton.config(state=tkinter.DISABLED)

# Button styles.
style = Style()
style.theme_use('clam')
style.configure('TButton', font=("Arial", 14), background="darkred", foreground="white", borderwidth=0)
style.map('TButton',
    foreground=[('pressed', 'white'), ('active', 'white'), ('disabled', 'black')],
    background=[('pressed', 'pink'), ('active', 'red'), ('disabled', 'grey')],
)

# Main method to launch the app.
if __name__ == "__main__":
    mainScreen.mainloop()