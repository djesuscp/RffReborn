import tkinter
from tkinter import ttk
from gui.stylesUI import keepStyles
from gui.oneDirectoryUI import oneDirectory
from gui.twoDirectoriesUI import twoDirectories

# GUI.
# Main screen configuration.
class Gui():
    def __init__(self):        
        self.mainScreen = tkinter.Tk()
        self.mainScreen.title("RffReborn")
        self.mainScreen.geometry("1600x800")
        self.mainScreen.configure(bg="#000000")

        keepStyles(self.mainScreen)

        self.container = tkinter.Frame(self.mainScreen, bg="#000000")
        self.container.pack(expand=True, fill="both")

        self.screens = {}

        self.createScreens()

        self.showScreen('menu')
    
    def createScreens(self):
        # ----- Menu Screen -----
        menu = tkinter.Frame(self.container, bg="#000000")
        tkinter.Label(menu, text="RFF Reborn",
                      fg="white", bg="#000000", font=("Arial", 20)).pack(pady=30)

        ttk.Button(menu, text="Examine On Directory",
                       command=lambda: self.showScreen("one")).pack(pady=10)

        ttk.Button(menu, text="Compare Two Directories",
                       command=lambda: self.showScreen("two")).pack(pady=10)

        self.screens["menu"] = menu
        menu.grid(row=0, column=0, sticky="nsew")

        # ----- OneDirectory Screen -----
        one = oneDirectory(self.container, self.showScreen)
        self.screens["one"] = one
        one.grid(row=0, column=0, sticky="nsew")

        # ----- TwoDirectories Screen -----
        two = twoDirectories(self.container, self.showScreen)
        self.screens["two"] = two
        two.grid(row=0, column=0, sticky="nsew")

    def showScreen(self, name: str):
        frame = self.screens[name]
        frame.tkraise()
    

    def run(self):
        self.mainScreen.mainloop()