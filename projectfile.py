from smtplib import *
import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import string
import os
import datetime


class loginPage(object):

    def __init__(self, master, info='Invoice Management'):
        self.master = master
        self.mainlabel = tk.Label(master, text=info, justify=tk.CENTER)
        self.mainlabel.grid(row=0, columnspan=3)

        self.user = tk.Label(master, text='username', borderwidth=2)
        self.user.grid(row=1, sticky=tk.W)

        self.pwd = tk.Label(master, text='password', borderwidth=2)
        self.pwd.grid(row=2, sticky=tk.W)


        attn = ['user1', 'user2']
        self.userEntry = ttk.Combobox(master)
        self.userEntry['values'] = tuple(attn)
        self.userEntry.grid(row=1, column=1, columnspan=2)
        self.userEntry.focus_set()

        self.pwdEntry = tk.Entry(master, show='*')
        self.pwdEntry.bind('<Return>',self.loginit)
        self.pwdEntry.grid(row=2, column=1, columnspan=2)

        self.loginButton = tk.Button(master, text='Login', borderwidth=2, command=self.login)
        self.loginButton.grid(row=3, column=1)

        self.clearButton = tk.Button(master, text='Clear', borderwidth=2, command=self.clear)
        self.clearButton.grid(row=3, column=2)

    def loginit(self,event):
        print(self.pwdEntry.get())
        self.login()
        self.clear()

    def clear(self):
        self.userEntry.delete(0, tk.END)
        self.pwdEntry.delete(0, tk.END)

    def login(self):
        self.username = self.userEntry.get().strip()
        self.passwd = self.pwdEntry.get().strip()
        self.clear()

        attn=['user1', 'user2']                                                                                        #username/usernames
        if len(self.username) == 0 or len(self.passwd) == 0 or not self.username in attn:
            tkMessageBox.showinfo('Notice','please check your username')
            self.clear()
            self.userEntry.focus_set()
            return
        else:
            p='1234'                                                                                                   #password/passwords
            if not self.passwd == p:
                tkMessageBox.showinfo('Notice','please check your password')
                self.clear()
                self.userEntry.focus_set()
                return
                
        self.connect()

    def connect(self):
        self.username = (self.userEntry.get().strip()).upper()
        self.invoice = invoice(self.master,self.username)
        #self.stock = stocks(self.master, self.username)

class stocks(object):
    def __init__(self, master, user=''):
        self.user = user
        self.mas = tk.Toplevel(master)


        
        #-----------------------------------treeview----------------------------
        invoice_list=['Code','Name','Quantity left','MRP','Price']
        listbar=tk.Frame(self.mas)

        bary3=tk.Scrollbar(listbar)
        bary3.pack(side=tk.RIGHT,fill=tk.Y)
        barx3=tk.Scrollbar(listbar,orient=tk.HORIZONTAL)
        barx3.pack(side=tk.BOTTOM,fill=tk.X)

        self.invoiceList=ttk.Treeview(listbar,columns=invoice_list)
        self.invoiceList.column(column='#0',width=0,stretch=False)
        for i in range(len(invoice_list)):
            self.invoiceList.heading(i,text=invoice_list[i])
            self.invoiceList.column(i,width=100)
        self.invoiceList.column(1,width=100)
        self.invoiceList['height']=20
        #self.invoiceList.bind('<<TreeviewSelect>>',self.getInvoiceItem)
        self.invoiceList.pack(side=tk.LEFT,fill=tk.BOTH)

        barx3.config(command=self.invoiceList.xview)
        bary3.config(command=self.invoiceList.yview)
        
        self.invoiceList.config(xscrollcommand=barx3.set,yscrollcommand=bary3.set)

        listbar.pack(fill=tk.X)

    def add_stock(self):
        '''
        a new dialog box will open to enter all the details
        and then youll press okay button or cancel button if you dont want to.
        this will update the the table in the database file
        '''
        pass

    def edit_stock(self):
        '''
        a new dialog box will open to enter code or name and then 
        this will open a new dialog box with labels and entries with the details 
        inserted already and you get to edit the values
        and then youll press okay button or cancel button if you dont want to.
        this will update the the table in the database file 
        '''
        pass

    
    def delete_stock(self):
        '''
        a new dialog box will open to enter code or name and then 
        and then youll press okay button or cancel button if you dont want to.
        this will update the the table in the database file
        '''

        pass





class invoice(object):
    def __init__(self, master, user=''):
        self.user = user
        self.DATALIST={}

        self.mas = tk.Toplevel(master)
        #--------------------------------------menubar-------------------------------
        menubar=tk.Menu(self.mas)
        filemenu=tk.Menu(menubar,tearoff=0)
        filemenu.add_command(label='Add Invoice')
        filemenu.add_command(label='Delete Invoice')
        filemenu.add_separator()
        filemenu.add_command(label='Exit',command=master.quit)
        menubar.add_cascade(label='File',menu=filemenu)

        projmenu=tk.Menu(menubar,tearoff=0)
        projmenu.add_command(label='Update Project List')
        menubar.add_cascade(label='Project',menu=projmenu)

        aboutmenu=tk.Menu(menubar,tearoff=0)
        aboutmenu.add_command(label='About Me')
        menubar.add_cascade(label='About',menu=aboutmenu)

        self.mas['menu']=menubar

        self.sp=tk.LabelFrame(self.mas, text="invoice")
        self.sp.pack(side=tk.TOP,fill=tk.X)


        #----------------------------------labels--------------------------------

        #tk.Label(self.sp,text='USER').grid(row=0,column=0,sticky=tk.W+tk.N)
        tk.Label(self.sp,text='DATE').grid(row=1,column=0,sticky=tk.W+tk.N)
        tk.Label(self.sp,text='PHONE NO').grid(row=1,column=3,sticky=tk.W+tk.N)
        tk.Label(self.sp,text='ADDRESS').grid(row=3,column=3,sticky=tk.W+tk.N)#CN AMOUNT
        tk.Label(self.sp,text='CUSTOMER NAME').grid(row=2,column=3,sticky=tk.W+tk.N)#INVOICE AMOUNT
        tk.Label(self.sp,text='BARCODE').grid(row=5,column=0,sticky=tk.W+tk.N)

        #=====USER NAME=====
        #self.username=StringVar()
        #self.username.set(self.user)
        #tk.Label(self.sp,text=self.user).grid(row=0,column=1,sticky=W+N)
        

        #ADD ENTRY FOR DATE WITH DATE AS OS.DATE
        
        #-------------------------------------entry---------------------------------
        
        '''
        important note. we have to bind
        before you pack or use grid to place the widgit
        '''
        
        #===============Date=======================
        self.date=tk.StringVar()
        #today's date
        formatted_date = datetime.date.strftime(datetime.date.today(), "%m/%d/%Y")
        
        self.Date=tk.Entry(self.sp,textvariable=self.date)
        self.Date.bind("<Return>", self.Print1)
        self.date.set(formatted_date)
        self.Date.grid(row=1,column=2,sticky=tk.W+tk.N)

        #==============PHONE NO===================
        self.phone_no=tk.StringVar()

        self.PhoneNo=tk.Entry(self.sp,textvariable=self.phone_no)
        self.phone_no.set('')
        self.PhoneNo.grid(row=1,column=4,sticky=tk.W+tk.N)
        

        #===============ADDRESS====================
        f1=tk.Frame(self.sp)
        bary1=tk.Scrollbar(f1)
        bary1.pack(side=tk.RIGHT,fill=tk.Y)
        self.address=tk.Text(f1,width=27,height=1)

        self.address.pack(side=tk.LEFT,fill=tk.BOTH)
        bary1.config(command=self.address.yview)
        self.address.config(yscrollcommand=bary1.set)
        f1.grid(row=4,column=3,rowspan=2,columnspan=3,sticky=tk.W+tk.N)

        
        #=====CUSTOMER NAME==============================
        self.customer_name=tk.StringVar()

        self.CustomerName=tk.Entry(self.sp,textvariable=self.customer_name)
        self.customer_name.set('')
        self.CustomerName.grid(row=2,column=4,sticky=tk.W+tk.N)
        #-----------------------------------treeview----------------------------
        invoice_list=['Code','Name','MRP','Price','Quantity','Total']
        listbar=tk.Frame(self.mas)

        bary3=tk.Scrollbar(listbar)
        bary3.pack(side=tk.RIGHT,fill=tk.Y)
        barx3=tk.Scrollbar(listbar,orient=tk.HORIZONTAL)
        barx3.pack(side=tk.BOTTOM,fill=tk.X)

        self.invoiceList=ttk.Treeview(listbar,columns=invoice_list)
        self.invoiceList.column(column='#0',width=0,stretch=False)
        for i in range(len(invoice_list)):
            self.invoiceList.heading(i,text=invoice_list[i])
            self.invoiceList.column(i,width=100)
        self.invoiceList.column(1,width=100)
        self.invoiceList['height']=20
        #self.invoiceList.bind('<<TreeviewSelect>>',self.getInvoiceItem)
        self.invoiceList.pack(side=tk.LEFT,fill=tk.BOTH)

        barx3.config(command=self.invoiceList.xview)
        bary3.config(command=self.invoiceList.yview)
        
        self.invoiceList.config(xscrollcommand=barx3.set,yscrollcommand=bary3.set)

        listbar.pack(fill=tk.X)
    def Print1(self, *args):
        print('date:',self.Date.get())
        self.Date.delete(0, tk.END)


if __name__ == '__main__':



    root = tk.Tk()
    root.title('')


    #myLogin = loginPage(root)

    stock=stocks(root)

    #root.wait_window(myLogin.mySendMail.sp)
    tk.mainloop()
