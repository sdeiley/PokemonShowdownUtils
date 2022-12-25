import sys
import tkinter as tk
from tkinter import simpledialog

ROOT = tk.Tk()

def initialize_ui():
    ROOT = tk.Tk()

def get_credentials() -> tuple:
    # Add extraneous argument to use local .txt file
    if (len(sys.argv) > 1):
        with open("credentials.txt", "r") as f:
            username = f.readline()
            password = f.readline()
    else:
        ROOT.withdraw()
        username = simpledialog.askstring(title="Username", prompt="Enter PS username")
        password = simpledialog.askstring(title="pass", prompt="Enter PS password (Warning: Cleartext)")

    return username, password

def display_results(replays: str):
    ROOT.deiconify()
    ROOT.geometry("800x600")
    T = tk.Text(ROOT, height = 800, width = 600)
    l = tk.Label(ROOT, text = "Your Replays")
    l.pack()
    T.pack()
    T.insert(tk.END, replays)

    tk.mainloop()