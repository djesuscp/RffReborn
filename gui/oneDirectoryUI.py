import tkinter
from tkinter import ttk
import controllers.singleDirectory as sd

class oneDirectory(tkinter.Frame):
    def __init__(self, master, showScreen):
        super().__init__(master, bg="#000000")
        info = 'Please, take into consideration that when clicking on the \"Clean\" button,\nthe program will create a security copy of the listed files into a new folder\nwithin the root directory selected.'
        windowTitle = tkinter.Label(self, text="Examine 1 directory window.", fg="white", bg="#000000", font=("Arial", 18))
        windowTitle.pack(pady=10)
        infoLabel = tkinter.Label(self, text=f'{info}', fg="white", bg="#000000", font=("Arial", 14))
        infoLabel.pack(pady=10)
        uniqueTextField = tkinter.Entry(self, width=60)
        uniqueTextField.pack(pady=10)
        browseButton = ttk.Button(self, text="Browse...", command=lambda: sd.browse(uniqueTextField, "Your", console, startSearchButton))
        browseButton.pack(pady=5)
        console = tkinter.Text(self, font=("courier new", 14), bg="#FFFFFF", fg="#000000")
        console.pack(expand=True, fill="both", padx=10, pady=10)
        startSearchButton = ttk.Button(self, text="Start Search", command=lambda: sd.searchInsideDirectory(f'{uniqueTextField.get()}', console, cleanButton))
        startSearchButton.pack(pady=5)
        startSearchButton.config(state=tkinter.DISABLED)
        cleanButton = ttk.Button(self, text="Clean", command=lambda: sd.clean(f'{uniqueTextField.get()}', console))
        cleanButton.pack(pady=5)
        cleanButton.config(state=tkinter.DISABLED)
        clearConsoleButton = ttk.Button(self, text="Clear console", command=lambda: sd.fm.clearConsole(console))
        clearConsoleButton.pack(pady=5)
        mainMenuButton = ttk.Button(self, text="Go back to Main Menu", command=lambda: showScreen("menu"))
        mainMenuButton.pack(pady=5)
