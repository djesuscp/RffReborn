from tkinter import ttk

def keepStyles(root):
# Button styles.
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('TButton', font=("Arial", 14), background="darkred", foreground="white", borderwidth=0)
    style.map('TButton',
        foreground=[('pressed', 'white'), ('active', 'white'), ('disabled', 'black')],
        background=[('pressed', 'pink'), ('active', 'red'), ('disabled', 'grey')],
    )