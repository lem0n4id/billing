import datetime
import tkinter as tk
import tkinter.font as font
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
from smtplib import *


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
        self.pwdEntry.bind('<Return>', self.loginit)
        self.pwdEntry.grid(row=2, column=1, columnspan=2)

        self.loginButton = tk.Button(
            master, text='Login', borderwidth=2, command=self.login)
        self.loginButton.grid(row=3, column=1)

        self.clearButton = tk.Button(
            master, text='Clear', borderwidth=2, command=self.clear)
        self.clearButton.grid(row=3, column=2)

    def loginit(self, event):
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

        attn = ['user1', 'user2']  # username/usernames
        if len(self.username) == 0 or len(self.passwd) == 0 or not self.username in attn:
            tkMessageBox.showinfo('Notice', 'please check your username')
            self.clear()
            self.userEntry.focus_set()
            return
        else:
            p = '1234'  # password/passwords
            if not self.passwd == p:
                tkMessageBox.showinfo('Notice', 'please check your password')
                self.clear()
                self.userEntry.focus_set()
                return

        self.connect()

    def connect(self):
        self.username = (self.userEntry.get().strip()).upper()
        self.invoice = invoice(self.master, self.username)
        #self.stock = stocks(self.master, self.username)


class stocks(object):
    def __init__(self, master, user=''):
        self.user = user
        self.mas = tk.Toplevel(master)
        tabcontrol = ttk.Notebook(self.mas)
        Inventory = ttk.Frame(tabcontrol)
        # ----------------------------------labelframes(invoice)
        self.labelframe2 = tk.LabelFrame(Inventory, text="Update Stocks")
        self.labelframe2.pack(side=tk.TOP, fill=tk.X)

        # ----------------------------------buttons(Add, Remove)
        tk.Button(self.labelframe2, text='Update', command=self.update_button).grid(
            row=3, column=1, sticky=tk.W+tk.N)

        # ----------------------------------labels(BARCODE, PRODUCT NAME, QUANTITY LEFT, MRP, RETAIL PRICE)
        tk.Label(self.labelframe2, text='BARCODE').grid(
            row=1, column=0, sticky=tk.W+tk.N)
        tk.Label(self.labelframe2, text='PRODUCT NAME').grid(
            row=1, column=2, sticky=tk.W+tk.N)
        tk.Label(self.labelframe2, text='QUANTITY LEFT').grid(
            row=1, column=4, sticky=tk.W+tk.N)
        tk.Label(self.labelframe2, text='MRP').grid(
            row=2, column=0, sticky=tk.W+tk.N)
        tk.Label(self.labelframe2, text='RETAIL PRICE').grid(
            row=2, column=2, sticky=tk.W+tk.N)

        # ----------------------------------entry(BARCODE, PRODUCT NAME, QUANTITY LEFT, MRP, RETAIL PRICE) all are StringVar

        '''
        important note. we have to bind
        before you pack or use grid to place the widgit
        '''

        # ==========BARCODE==========

        self.barcode = tk.StringVar()

        self.BarCode = tk.Entry(self.labelframe2, textvariable=self.barcode)
        self.BarCode.bind("<Return>", self.barcode_bind_function)
        self.barcode.set('')
        self.BarCode.grid(row=1, column=1, sticky=tk.W+tk.N)

        # ==========PRODUCT NAME==========

        self.product_name = tk.StringVar()

        self.ProductName = tk.Entry(
            self.labelframe2, textvariable=self.product_name)
        self.ProductName.bind("<Return>", self.product_name_bind_function)
        self.product_name.set('')
        self.ProductName.grid(row=1, column=3, sticky=tk.W+tk.N)

        # ==========QUANTITY==========

        self.quantity = tk.StringVar()

        self.Quantity = tk.Entry(self.labelframe2, textvariable=self.quantity)
        self.Quantity.bind("<Return>", self.quantity_bind_function)
        self.quantity.set('')
        self.Quantity.grid(row=1, column=5, sticky=tk.W+tk.N)

        # ===============MRP=======================
        self.mrp = tk.StringVar()

        self.Mrp = tk.Entry(self.labelframe2, textvariable=self.mrp)
        self.Mrp.bind("<Return>", self.mrp_name_bind_function)
        self.mrp.set('')
        self.Mrp.grid(row=2, column=1, sticky=tk.W+tk.N)

        # ==============RETAIL PRICE===================
        self.retail_price = tk.StringVar()

        self.RetailPrice = tk.Entry(
            self.labelframe2, textvariable=self.retail_price)
        self.RetailPrice.bind("<Return>", self.retail_price_bind_function)
        self.retail_price.set('')
        self.RetailPrice.grid(row=2, column=3, sticky=tk.W+tk.N)

        tabcontrol.add(Inventory,text='Inventory')
        tabcontrol.pack(expand=1,fill="both")

        tabcontrol1 = ttk.Notebook(self.mas)
        Inventory1 = ttk.Frame(tabcontrol1)

        
        # -----------------------------------treeview----------------------------
        invoice_list = ['Barcode', 'Product Name',
                        'Quantity Left', 'MRP', 'Retail Price']
        listbar = tk.Frame(Inventory1)

        bary3 = tk.Scrollbar(listbar)
        bary3.pack(side=tk.RIGHT, fill=tk.Y)
        barx3 = tk.Scrollbar(listbar, orient=tk.HORIZONTAL)
        barx3.pack(side=tk.BOTTOM, fill=tk.X)

        self.invoiceList = ttk.Treeview(listbar, columns=invoice_list)
        self.invoiceList.column(column='#0', width=0, stretch=False)
        for i in range(len(invoice_list)):
            self.invoiceList.heading(i, text=invoice_list[i])
            self.invoiceList.column(i, width=100)
        self.invoiceList.column(1, width=100)
        self.invoiceList['height'] = 20
        # self.invoiceList.bind('<<TreeviewSelect>>',self.getInvoiceItem)
        self.invoiceList.pack(side=tk.LEFT, fill=tk.BOTH)

        self.invoiceList.insert('', 'end', values=(
            '0000010', 'lifeboy soap', '86', '20', '18'))

        barx3.config(command=self.invoiceList.xview)
        bary3.config(command=self.invoiceList.yview)

        self.invoiceList.config(xscrollcommand=barx3.set,
                                yscrollcommand=bary3.set)

        listbar.pack(fill=tk.X)

        tabcontrol1.add(Inventory1,text='Inventory1')
        tabcontrol1.pack(expand=1,fill="both")
    

    def barcode_bind_function(self):
        pass

    def product_name_bind_function(self):
        pass

    def quantity_bind_function(self):
        pass

    def mrp_name_bind_function(self):
        pass

    def retail_price_bind_function(self):
        pass

    def update_button(self):
        pass



class invoice(object):
    def __init__(self, master, user=''):
        self.master = master
        self.user = user
        self.DATALIST = {}

        self.mas = tk.Toplevel(master)
        # ----------------------------------menubar(File[Add Invoice, Delete Invoice, Exit], Project[Update Project List], About[About Me])
        menubar = tk.Menu(self.mas)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Add Invoice')
        filemenu.add_command(label='Delete Invoice')
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=master.quit)
        menubar.add_cascade(label='File', menu=filemenu)

        projmenu = tk.Menu(menubar, tearoff=0)
        projmenu.add_command(label='Update Stocks', command=self.updatestocks)
        menubar.add_cascade(label='Stocks', menu=projmenu)

        aboutmenu = tk.Menu(menubar, tearoff=0)
        aboutmenu.add_command(label='About Me')
        menubar.add_cascade(label='About', menu=aboutmenu)

        self.mas['menu'] = menubar
        # ----------------------------------labelframes(invoice)
        self.labelframe1 = tk.LabelFrame(
            self.mas, text="invoice")  # change name labelframe1
        self.labelframe1.pack(side=tk.TOP, fill=tk.X)

        # ----------------------------------buttons(Add, Remove)
        tk.Button(self.labelframe1, text='Add', command=self.bill_add).grid(
            row=6, column=7, sticky=tk.W+tk.N)
        tk.Button(self.labelframe1, text='Remove', command=self.bill_remove).grid(
            row=6, column=8, sticky=tk.W+tk.N)

        # ----------------------------------labels(DATE, PHONE NO, ADDRESS, CUSTOMER NAME, BARCODE, PRODUCT NAME, QUANTITY)

        # tk.Label(self.labelframe1,text='USER').grid(
        #   row=0, column=0, sticky=tk.W+tk.N)
        tk.Label(self.labelframe1, text='DATE').grid(
            row=1, column=0, sticky=tk.W+tk.N)
        tk.Label(self.labelframe1, text='PHONE NO').grid(
            row=1, column=3, sticky=tk.W+tk.N)
        tk.Label(self.labelframe1, text='ADDRESS').grid(
            row=3, column=3, sticky=tk.W+tk.N)
        tk.Label(self.labelframe1, text='CUSTOMER NAME').grid(
            row=2, column=3, sticky=tk.W+tk.N)
        tk.Label(self.labelframe1, text='BARCODE').grid(
            row=6, column=0, sticky=tk.W+tk.N)
        tk.Label(self.labelframe1, text='PRODUCT NAME').grid(
            row=6, column=3, sticky=tk.W+tk.N)
        tk.Label(self.labelframe1, text='QUANTITY').grid(
            row=6, column=5, sticky=tk.W+tk.N)

        # =====USER NAME=====
        #self.username = StringVar()
        # self.username.set(self.user)
        #tk.Label(self.labelframe1, text=self.user).grid(row=0, column=1, sticky=W+N)

        # ADD ENTRY FOR DATE WITH DATE AS OS.DATE

        # ----------------------------------entry(date, phone_no, address, customer_name, barcode, product_name, quantity) all are StringVar

        '''
        important note. we have to bind
        before you pack or use grid to place the widgit
        '''

        # ===============Date=======================
        self.date = tk.StringVar()

        # today's date
        formatted_date = datetime.date.strftime(
            datetime.date.today(), "%m/%d/%Y")

        self.Date = tk.Entry(self.labelframe1, textvariable=self.date)
        self.Date.bind("<Return>", self.Print1)
        self.date.set(formatted_date)
        self.Date.grid(row=1, column=1, sticky=tk.W+tk.N)

        # ==============PHONE NO===================
        self.phone_no = tk.StringVar()

        self.PhoneNo = tk.Entry(self.labelframe1, textvariable=self.phone_no)
        self.PhoneNo.bind("<Return>", self.phone_no_bind_function)
        self.phone_no.set('')
        self.PhoneNo.grid(row=1, column=4, sticky=tk.W+tk.N)

        # ===============ADDRESS====================
        self.address = tk.StringVar()

        f1 = tk.Frame(self.labelframe1)
        bary1 = tk.Scrollbar(f1)
        bary1.pack(side=tk.RIGHT, fill=tk.Y)
        self.Address = tk.Text(f1, width=27, height=1)
        self.Address.bind("<Return>", self.address_bind_function)
        self.address.set('')
        self.Address.pack(side=tk.LEFT, fill=tk.BOTH)
        bary1.config(command=self.Address.yview)
        self.Address.config(yscrollcommand=bary1.set)
        f1.grid(row=4, column=3, rowspan=2, columnspan=3, sticky=tk.W+tk.N)

        # =====CUSTOMER NAME==============================
        self.customer_name = tk.StringVar()

        self.CustomerName = tk.Entry(
            self.labelframe1, textvariable=self.customer_name)
        self.CustomerName.bind("<Return>", self.customer_name_bind_function)
        self.customer_name.set('')
        self.CustomerName.grid(row=2, column=4, sticky=tk.W+tk.N)

        # ==========BARCODE==========

        self.barcode = tk.StringVar()

        self.BarCode = tk.Entry(self.labelframe1, textvariable=self.barcode)
        self.BarCode.bind("<Return>", self.barcode_bind_function)
        self.barcode.set('')
        self.BarCode.grid(row=6, column=1, sticky=tk.W+tk.N)

        # ==========PRODUCT NAME==========

        self.product_name = tk.StringVar()

        self.ProductName = tk.Entry(
            self.labelframe1, textvariable=self.product_name)
        self.ProductName.bind("<Return>", self.product_name_bind_function)
        self.product_name.set('')
        self.ProductName.grid(row=6, column=4, sticky=tk.W+tk.N)

        # ==========QUANTITY==========

        self.quantity = tk.StringVar()

        self.Quantity = tk.Entry(self.labelframe1, textvariable=self.quantity)
        self.Quantity.bind("<Return>", self.quantity_bind_function)
        self.quantity.set('')
        self.Quantity.grid(row=6, column=6, sticky=tk.W+tk.N)

        # -----------------------------------treeview----------------------------
        invoice_list = ['Sr no', 'Barcode', 'Product Name',
                        'MRP', 'Price', 'Quantity', 'Total']
        listbar = tk.Frame(self.mas)

        bary3 = tk.Scrollbar(listbar)
        bary3.pack(side=tk.RIGHT, fill=tk.Y)
        barx3 = tk.Scrollbar(listbar, orient=tk.HORIZONTAL)
        barx3.pack(side=tk.BOTTOM, fill=tk.X)

        self.invoiceList = ttk.Treeview(listbar, columns=invoice_list)
        self.invoiceList.column(column='#0', width=0, stretch=False)
        for i in range(len(invoice_list)):
            self.invoiceList.heading(i, text=invoice_list[i])
            self.invoiceList.column(i, stretch=tk.YES)
        self.invoiceList.column(1, width=100)
        self.invoiceList['height'] = 20
        # self.invoiceList.bind('<<TreeviewSelect>>',self.getInvoiceItem)
        self.invoiceList.pack(side=tk.LEFT, fill=tk.BOTH)

        barx3.config(command=self.invoiceList.xview)
        bary3.config(command=self.invoiceList.yview)

        self.invoiceList.config(xscrollcommand=barx3.set,
                                yscrollcommand=bary3.set)

        listbar.pack(fill=tk.X)

    def Print1(self, *args):
        print('date:', self.Date.get())
        self.Date.delete(0, tk.END)

    def phone_no_bind_function(self):
        pass

    def customer_name_bind_function(self):
        pass

    def address_bind_function(self):
        pass

    def barcode_bind_function(self):
        pass

    def product_name_bind_function(self):
        pass

    def quantity_bind_function(self):
        pass

    def bill_add(self):
        pass

    def bill_remove(self):
        pass

    def updatestocks(self):
        self.stocks = stocks(self.master)


if __name__ == '__main__':

    root = tk.Tk()
    root.title('')

    myLogin = loginPage(root)

    # stock=stocks(root)

    # root.wait_window(myLogin.mySendMail.labelframe1)
    tk.mainloop()
