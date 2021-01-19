import datetime
import tkinter as tk
import tkinter.font as font
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
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

        # retriving username password from database
        self.managers_usernamepasswd, self.cashiers_usernamepasswd, self.no_of_users = self.get_login_details()
        self.manager_usernames, self.cashier_usernames, self.attn = self.get_attn()  # usernames
        self.username = ttk.Combobox(master)
        self.username['values'] = tuple(self.attn)
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
        # print(self.password.get())
        self.login()
        self.clear()

    def clear(self):
        self.username.delete(0, tk.END)
        self.password.delete(0, tk.END)

    def password_focus(self, event):
        self.password.focus_set()

    def login(self):
        self.usernm = self.username.get().strip()
        self.passwd = self.password.get().strip()
        self.clear()

        if len(self.usernm) == 0 or len(self.passwd) == 0 or not self.usernm in self.attn:
            tkMessageBox.showinfo('Notice', 'please check your username')
            self.clear()
            self.usernm.focus_set()
            return
        else:
            if self.usernm in self.manager_usernames:
                for i in self.managers_usernamepasswd:
                    if i[0] == self.usernm:
                        if i[1] != self.passwd:
                            tkMessageBox.showinfo(
                                'Notice', 'please check your password')
                            self.clear()
                            self.username.focus_set()
                            return
                        else:
                            self.connect_manager(self.usernm)

            elif self.usernm in self.cashier_usernames:
                for i in self.cashiers_usernamepasswd:
                    if i[0] == self.usernm:
                        if i[1] != self.passwd:
                            tkMessageBox.showinfo(
                                'Notice', 'please check your password')
                            self.clear()
                            self.username.focus_set()
                            return
                        else:
                            self.connect_cashier(self.usernm)

    def connect_cashier(self, usernm):
        self.invoice = cashier_window.invoice(self.master, user=self.usernm)

    def connect_manager(self, usernm):
        self.stock = manager_window.manager_win(self.master)

    def get_login_details(self):
        login_infos = {'manager': [], 'cashier': []}
        x = "select * from users;"
        c.execute(x)
        no_of_users = 0
        for i in c.fetchall():
            username, password, desgn = i
            for j in login_infos:
                if j == desgn:
                    login_infos[j] = login_infos[j] + [(username, password)]
                    no_of_users += 1
        return login_infos['manager'], login_infos['cashier'], no_of_users

    def get_attn(self):
        attn = []  # username/usernames
        manager_usernames = []
        cashier_usernames = []
        # print(self.managers_usernamepasswd, len(self.managers_usernamepasswd))
        for i in range(len(self.managers_usernamepasswd)):
            manager_usernames += [self.managers_usernamepasswd[i][0]]
            attn += [self.managers_usernamepasswd[i][0]]
        for i in range(len(self.cashiers_usernamepasswd)):
            cashier_usernames += [self.cashiers_usernamepasswd[i][0]]
            attn += [self.cashiers_usernamepasswd[i][0]]
        # print(manager_usernames, cashier_usernames, attn)
        return manager_usernames, cashier_usernames, attn


if __name__ == '__main__':
    db = sqlite3.connect("database.db")
    c = db.cursor()

    root = tk.Tk()
    root.title('')

    myLogin = loginPage(root)

    tk.mainloop()
