import controllers.fileManager as fm
import tkinter
import os
import shutil

def browse(textField, fieldRef, console, button):
    fm.cleanList(fm.directories)
    fm.browseDirectory(textField)
    fm.showTextConsole(console, f'{fieldRef} selected directory is: ' + textField.get())
    fm.countValidDirectories(button, "one")

def searchInsideDirectory(dirName, console, button):
    list = fm.getFileList(fm.directories[0])
    for x in range(len(list)):
        fileName1 = os.path.basename(list[x])
        fileSize1 = os.path.getsize(list[x])
        for i in range(x+1, len(list)):
            fileName2 = os.path.basename(list[i])
            fileSize2 = os.path.getsize(list[i])
            if fileName1 == fileName2 and fileSize1 == fileSize2:
                fm.ownCoincidenceList1.append(list[x])
                fm.ownCoincidenceList1.append(list[i])
    fm.removeDuplicates(fm.ownCoincidenceList1)
    fm.showTextConsole(console, f'\n---------------\nLIST OF REPEATED FILES INSIDE {dirName}:')
    fm.showTextConsole(console, fm.showCoincidences(fm.ownCoincidenceList1))
    print(fm.ownCoincidenceList1)
    button.config(state=tkinter.NORMAL)

def clean(root, console):
    destinationFolder = f'{root}' + '/securityCopy'
    os.mkdir(f'{destinationFolder}')
    list = fm.ownCoincidenceList1
    shutil.copy2(list[0], destinationFolder)
    list2 = fm.getFileList(destinationFolder)
    for x in range(len(list)):
        fileName1 = os.path.basename(list[x])
        fileSize1 = os.path.getsize(list[x])
        for i in range(len(list2)):
            fileName2 = os.path.basename(list2[i])
            fileSize2 = os.path.getsize(list2[i])
            if fileName1 == fileName2 and fileSize1 == fileSize2:
                fm.showTextConsole(console, f'File named {fileName1} already exists in {destinationFolder}')
            else:
                shutil.copy2(list[x], destinationFolder)
                fm.showTextConsole(console, f'File named {fileName1} has been successfully copied to {destinationFolder}')
    for x in range(len(list)):
        os.remove(list[x])
