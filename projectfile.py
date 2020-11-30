import datetime
import tkinter as tk
import tkinter.font as font
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
from smtplib import *
import sqlite3
import manager_window
import cashier_window

'''
there will be a common login window where both a manager and a cashier can log in.
cashier does the billing at the counter.
manager managers the stock and has the control over the customer data and analysing the sales data to
 see which products do good sale, at what time the customers usually come, etc etc,basically customer data
 also sets the sales price of goods
'''


class loginPage(object):

    def __init__(self, master):
        self.master = master
        self.master.title('Login')
        self._label = tk.Label(master, text='Welcome!', justify=tk.CENTER)
        self._label.grid(row=0, columnspan=3)

        self.user = tk.Label(master, text='username', borderwidth=2)
        self.user.grid(row=1, sticky=tk.W)

        self._password = tk.Label(master, text='password', borderwidth=2)
        self._password.grid(row=2, sticky=tk.W)

        attn = ['user1', 'user2']
        self.username = ttk.Combobox(master)
        self.username['values'] = tuple(attn)
        self.username.bind('<Return>', self.password_focus)
        self.username.grid(row=1, column=1, columnspan=2)
        self.username.focus_set()

        self.password = tk.Entry(master, show='*')
        self.password.bind('<Return>', self.loginit)
        self.password.grid(row=2, column=1, columnspan=2)

        self.loginButton = tk.Button(
            master, text='Login', borderwidth=2, command=self.login)
        self.loginButton.grid(row=3, column=1)

        self.clearButton = tk.Button(
            master, text='Clear', borderwidth=2, command=self.clear)
        self.clearButton.grid(row=3, column=2)

    def loginit(self, event):
        print(self.password.get())
        self.login()
        self.clear()

    def clear(self):
        self.username.delete(0, tk.END)
        self.password.delete(0, tk.END)

    def password_focus(self, event):
        self.password.focus_set()

    def login(self):
        self.username = self.username.get().strip()
        self.passwd = self.password.get().strip()
        self.clear()

        attn = ['user1', 'user2']  # username/usernames
        managers = ['user1']
        cashiers = ['user2']
        if len(self.username) == 0 or len(self.passwd) == 0 or not self.username in attn:
            tkMessageBox.showinfo('Notice', 'please check your username')
            self.clear()
            self.username.focus_set()
            return
        else:
            p = '1234'  # password/passwords
            if not self.passwd == p:
                tkMessageBox.showinfo('Notice', 'please check your password')
                self.clear()
                self.username.focus_set()
                return
            else:
                if self.username in managers:
                    self.connect_manager(self.username)
                elif self.username in cashiers:
                    self.connect_cashier(self.username)

    def connect_cashier(self, username):
        self.invoice = cashier_window.invoice(self.master, user=self.username)

    def connect_manager(self, username):
        self.stock = manager_window.manager_win(self.master)



if __name__ == '__main__':
    db=sqlite3.connect("database.db")

    root = tk.Tk()
    root.title('')

    myLogin = loginPage(root)

    tk.mainloop()
