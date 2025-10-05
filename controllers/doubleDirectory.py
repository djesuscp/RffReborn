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
    showTextConsole('\n---------------\nLIST OF REPEATED FILES BETWEEN DIR1 and DIR2:')
    showTextConsole(showCoincidences(coincidenceList1))
    showTextConsole('\nEND OF DIR1 LIST.')
    showTextConsole('\n---------------\nLIST OF REPEATED FILES BETWEEN DIR2 and DIR1:')
    showTextConsole(showCoincidences(coincidenceList2))
    showTextConsole('\nEND OF DIR2 LIST.')