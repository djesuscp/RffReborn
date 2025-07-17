import tkinter
from tkinter import *
from tkinter.ttk import *

# Main screen configuration.
mainScreen = tkinter.Tk()
mainScreen.title("RffReborn")
mainScreen.geometry("800x800")
mainScreen.configure(bg="#000000")

# Labels.
title = tkinter.Label(mainScreen, text="RffReborn", font=("Arial", 20), bg="#000000", fg="#FFFFFF")
title.grid(row=0, column=0, columnspan=7)

# Text Fields.
field1 = tkinter.Entry(mainScreen, width=60)
field2 = tkinter.Entry(mainScreen, width=60)
field3 = tkinter.Entry(mainScreen, width=60)
field4 = tkinter.Entry(mainScreen, width=60)
field1.grid(row=1, column=0)
field2.grid(row=2, column=0)
field3.grid(row=3, column=0)
field4.grid(row=4, column=0)

# Text Area.
console = tkinter.Text(mainScreen, font=("courier new", 14), bg="#FFFFFF", fg="#000000", width=75)
console.grid(row=5, column=0, columnspan=7)

# Buttons.
button1 = Button(mainScreen, text="Browse...")
button1.grid(row=1, column=1)
button2 = Button(mainScreen, text="Browse...")
button2.grid(row=2, column=1)
button3 = Button(mainScreen, text="Browse...")
button3.grid(row=3, column=1)
button4 = Button(mainScreen, text="Browse...")
button4.grid(row=4, column=1)
# Button styles.
style = Style()
style.theme_use('clam')
style.configure('TButton', font=("Arial", 14), background="darkred", foreground="white", borderwidth=0)
style.map('TButton',
    foreground=[('pressed', 'white'), ('active', 'white')],
    background=[('pressed', 'pink'), ('active', 'red')],
)

# Main method to launch the app.
if __name__ == "__main__":
    mainScreen.mainloop()