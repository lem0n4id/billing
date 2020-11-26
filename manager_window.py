import datetime
import tkinter as tk
from tkinter import Toplevel
import tkinter.font as font
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
from smtplib import *


class manager_win(object):
    """
    docstring
    """
    def __init__(self, master):
        self.master = master
        self.mas = master

        #buttons
        tk.Button(self.mas,text='stocks').grid(row=0,column=0,sticky=tk.N+tk.W, padx=10, pady=10, ipadx=36, ipady=5)
        tk.Button(self.mas,text='sales').grid(row=0,column=1,sticky=tk.N+tk.W, padx=10, pady=10, ipadx=36, ipady=5)
        tk.Button(self.mas,text='Employyee details').grid(row=1,column=0,sticky=tk.N+tk.W, padx=10, pady=10, ipadx=5, ipady=5)






if __name__ == "__main__":
    root = tk.Tk()
    manager = manager_win(root)
    tk.mainloop()