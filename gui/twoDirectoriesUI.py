import tkinter
from tkinter import ttk

class twoDirectories(tkinter.Frame):
    def __init__(self, master, showScreen):
        super().__init__(master, bg="#000000")
        tkinter.Label(self, text="Compare 2 directories window.", fg="white", bg="#000000", font=("Arial", 16)).pack(pady=10)

        self.text = tkinter.Text(self, font=("courier new", 14), bg="#FFFFFF", fg="#000000")
        self.text.pack(expand=True, fill="both", padx=10, pady=10)

        ttk.Button(self, text="Main Menu",
                  command=lambda: showScreen("menu")).pack(pady=5)