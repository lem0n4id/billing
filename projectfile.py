import datetime
import tkinter as tk
import tkinter.font as font
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
from smtplib import *


class loginPage(object):

    def __init__(self, master, info='Invoice Management'):
        self.master = master
        self.master.title('Login')
        self.mainlabel = tk.Label(master, text=info, justify=tk.CENTER)
        self.mainlabel.grid(row=0, columnspan=3)

        self.user = tk.Label(master, text='username', borderwidth=2)
        self.user.grid(row=1, sticky=tk.W)

        self.pwd = tk.Label(master, text='password', borderwidth=2)
        self.pwd.grid(row=2, sticky=tk.W)

        attn = ['user1', 'user2']
        self.userEntry = ttk.Combobox(master)
        self.userEntry['values'] = tuple(attn)
        self.userEntry.bind('<Return>', self.pwdEntry_focus)
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

    def pwdEntry_focus(self, event):
        self.pwdEntry.focus_set()

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

        self.connect(self.username)

    def connect(self, username):
        self.invoice = invoice(self.master, user=self.username)
        #self.stock = stocks(self.master, self.username)


class stocks(object):
    '''
    retail price=wholesale price/(1-markup percentage[in decimal]) *markup percentage=profit margin
    '''
    def __init__(self, master, user=''):
        self.user = user
        self.mas = tk.Toplevel(master)
        self.mas.title('Stock Management')

        tabcontrol = ttk.Notebook(self.mas)
        tab = ttk.Frame(tabcontrol)
        # ----------------------------------labelframes(invoice)
        self.labelframe2 = tk.LabelFrame(tab, text="Add to Stocks")
        self.labelframe2.pack(side=tk.TOP, fill=tk.X)

        # ----------------------------------buttons(Add, Remove)
        tk.Button(self.labelframe2, text='Add', command=self.add_button).grid(
            row=3, column=1, sticky=tk.W+tk.N)

        # ----------------------------------labels(PRODUCT CODE , PRODUCT NAME, QUANTITY LEFT, MRP, RETAIL PRICE)
        tk.Label(self.labelframe2, text='DATE').grid(
            row=0, column=0, sticky=tk.W+tk.N)
        tk.Label(self.labelframe2, text='PRODUCT CODE ').grid(
            row=1, column=0, sticky=tk.W+tk.N)
        tk.Label(self.labelframe2, text='PRODUCT NAME').grid(
            row=1, column=2, sticky=tk.W+tk.N)
        tk.Label(self.labelframe2, text='QUANTITY').grid(
            row=1, column=4, sticky=tk.W+tk.N)
        tk.Label(self.labelframe2, text='MRP').grid(
            row=2, column=0, sticky=tk.W+tk.N)
        # ----------------------------------entry(PRODUCT CODE, PRODUCT NAME, QUANTITY LEFT, MRP, RETAIL PRICE) all are StringVar

        '''
        important note. we have to bind
        before you pack or use grid to place the widgit
        '''

        self.date = tk.StringVar()

        # today's date
        formatted_date = datetime.date.strftime(
            datetime.date.today(), "%m/%d/%Y")

        self.Date = tk.Entry(self.labelframe2, textvariable=self.date)
        #self.Date.bind("<Return>", self.Print1)
        self.date.set(formatted_date)
        self.Date.grid(row=0, column=1, sticky=tk.W+tk.N)

        self.productcode = tk.StringVar()

        self.ProductCode = tk.Entry(self.labelframe2, textvariable=self.productcode)
        self.ProductCode.bind("<Return>", self.barcode_bind_function)
        self.productcode.set('')
        self.ProductCode.grid(row=1, column=1, sticky=tk.W+tk.N)

        self.product_name = tk.StringVar()

        self.ProductName = tk.Entry(
            self.labelframe2, textvariable=self.product_name)
        self.ProductName.bind("<Return>", self.product_name_bind_function)
        self.product_name.set('')
        self.ProductName.grid(row=1, column=3, sticky=tk.W+tk.N)

        self.quantity = tk.StringVar()

        self.Quantity = tk.Entry(self.labelframe2, textvariable=self.quantity)
        self.Quantity.bind("<Return>", self.quantity_bind_function)
        self.quantity.set('')
        self.Quantity.grid(row=1, column=5, sticky=tk.W+tk.N)

        self.mrp = tk.StringVar()

        self.Mrp = tk.Entry(self.labelframe2, textvariable=self.mrp)
        self.Mrp.bind("<Return>", self.mrp_name_bind_function)
        self.mrp.set('')
        self.Mrp.grid(row=2, column=1, sticky=tk.W+tk.N)

        tabcontrol.add(tab, text='add stock purchase details')
        tabcontrol.pack(expand=1, fill="both")

        tab2 = ttk.Frame(tabcontrol)

        # -----------------------------------treeview(stock available)----------------------------
        invoice_list = ['Product Code', 'Product Name',
                        'Quantity']
        listbar = tk.Frame(tab2)

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
            '0000010', 'lifeboy soap', '86'))

        barx3.config(command=self.invoiceList.xview)
        bary3.config(command=self.invoiceList.yview)

        self.invoiceList.config(xscrollcommand=barx3.set,
                                yscrollcommand=bary3.set)

        listbar.pack(fill=tk.X)

        tabcontrol.add(tab2, text='stock available')
        tabcontrol.pack(expand=1, fill="both")

        tab3 = ttk.Frame(tabcontrol)

        # -----------------------------------treeview(purchase history)----------------------------
        invoice_list = ['date', 'Product Code', 'Product Name',
                        'Quantity']
        listbar = tk.Frame(tab3)

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

        self.invoiceList.insert('', 'end', values=('11/24/2020',
                                                   '0000010', 'lifeboy soap', '50'))

        barx3.config(command=self.invoiceList.xview)
        bary3.config(command=self.invoiceList.yview)

        self.invoiceList.config(xscrollcommand=barx3.set,
                                yscrollcommand=bary3.set)

        listbar.pack(fill=tk.X)

        tabcontrol.add(tab3, text='purchase history')
        tabcontrol.pack(expand=1, fill="both")
        self.BarCode_focus()
    #focus
    def BarCode_focus(self):
        self.ProductCode.focus_set()

    def barcode_bind_function(self, event):
        pass

    def product_name_bind_function(self, event):
        pass

    def quantity_bind_function(self, event):
        pass

    def mrp_name_bind_function(self, event):
        pass

    def add_button(self):
        pass


class invoice(object):
    def __init__(self, master, user=''):
        self.master = master
        self.user = user
        self.DATALIST = {}

        self.mas = tk.Toplevel(master)
        self.mas.title('Billing')
        # ----------------------------------menubar(File[Exit], Stocks[View Stocks],Customer Details[View Customer Purchase History], About[About Me])
        menubar = tk.Menu(self.mas)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Exit', command=master.quit)
        menubar.add_cascade(label='File', menu=filemenu)

        stocksmenu = tk.Menu(menubar, tearoff=0)
        stocksmenu.add_command(label='View Stocks', command=self.stocks_window)
        menubar.add_cascade(label='Stocks', menu=stocksmenu)

        custdetlmenu = tk.Menu(menubar, tearoff=0)
        custdetlmenu.add_command(label='View Customer Purchase History')
        menubar.add_cascade(label='Customer Details', menu=custdetlmenu)

        aboutmenu = tk.Menu(menubar, tearoff=0)
        aboutmenu.add_command(label='About Me')
        menubar.add_cascade(label='About', menu=aboutmenu)

        self.mas['menu'] = menubar
        # ----------------------------------labelframes

        self.labelframeN = tk.LabelFrame(
            self.mas, text="Employyee details")
        self.labelframeN.pack(side=tk.TOP, fill=tk.X)

        self.frame = tk.Frame(self.mas)
        self.frame.pack(side=tk.TOP, fill=tk.X)

        self.labelframe1 = tk.LabelFrame(
            self.frame, text="invoice")
        self.labelframe1.pack(side=tk.LEFT, fill=tk.BOTH)

        self.labelframeN1 = tk.LabelFrame(self.frame, text="customer details")
        self.labelframeN1.pack(side=tk.LEFT, fill=tk.BOTH)

        # ----------------------------------buttons in Employyee details(logout)

        tk.Button(self.labelframeN, text='logout', command=self.mas.quit).grid(
            row=1, column=0, sticky=tk.W+tk.N)

        # ----------------------------------labels in Employyee details(User)

        tk.Label(self.labelframeN, text='User: ').grid(
            row=0, column=0, sticky=tk.W+tk.N)

        # self.username = tk.StringVar()
        # self.username.set(self.user)
        tk.Label(self.labelframeN, text=user).grid(
            row=0, column=1, sticky=tk.W+tk.N)

        # ----------------------------------buttons in invoice(Add, Remove)

        tk.Button(self.labelframe1, text='Add', command=self.bill_add).grid(
            row=1, column=0, sticky=tk.W+tk.N)
        tk.Button(self.labelframe1, text='Remove', command=self.bill_remove).grid(
            row=1, column=1, sticky=tk.W+tk.N)

        # ----------------------------------labels in invoice(PRODUCT CODE , PRODUCT NAME, QUANTITY)


        tk.Label(self.labelframe1, text='PRODUCT CODE ').grid(
            row=0, column=0, sticky=tk.W+tk.N)
        tk.Label(self.labelframe1, text='PRODUCT NAME').grid(
            row=0, column=3, sticky=tk.W+tk.N)
        tk.Label(self.labelframe1, text='QUANTITY').grid(
            row=0, column=5, sticky=tk.W+tk.N)

        # ----------------------------------entries in invoice(productcode, product_name, quantity) all are StringVar

        '''
        important note- we have to bind
        before you pack or use grid to place the widgit
        '''


        self.productcode = tk.StringVar()

        self.ProductCode = tk.Entry(self.labelframe1, textvariable=self.productcode)
        self.ProductCode.bind("<Return>", self.barcode_bind_function)
        self.productcode.set('')
        self.ProductCode.grid(row=0, column=1, sticky=tk.W+tk.N)

        self.product_name = tk.StringVar()

        self.ProductName = tk.Entry(
            self.labelframe1, textvariable=self.product_name)
        self.ProductName.bind("<Return>", self.product_name_bind_function)
        self.product_name.set('')
        self.ProductName.grid(row=0, column=4, sticky=tk.W+tk.N)

        self.quantity = tk.StringVar()

        self.Quantity = tk.Entry(self.labelframe1, textvariable=self.quantity)
        self.Quantity.bind("<Return>", self.quantity_bind_function)
        self.quantity.set('')
        self.Quantity.grid(row=0, column=6, sticky=tk.W+tk.N)

        # ----------------------------------buttons in customer details(okay, clear)
        tk.Button(self.labelframeN1, text='Okay', command=self.enter_customer_details).grid(
            row=1, column=0, sticky=tk.W+tk.N)
        tk.Button(self.labelframeN1, text='Clear', command=self.clear_customer_details).grid(
            row=1, column=1, sticky=tk.W+tk.N)
        
        
        # ----------------------------------labels in customer details(PHONE NO, ADDRESS, CUSTOMER NAME)

        tk.Label(self.labelframeN1, text='PHONE NO').grid(
            row=0, column=0, sticky=tk.W+tk.N)
        tk.Label(self.labelframeN1, text='CUSTOMER NAME').grid(
            row=2, column=0, sticky=tk.W+tk.N)
        tk.Label(self.labelframeN1, text='ADDRESS').grid(
            row=3, column=0, sticky=tk.W+tk.N)
        tk.Label(self.labelframeN1, text='Customer type:').grid(
            row=0, column=2, sticky=tk.W+tk.N)

        # ----------------------------------entries in customer details(phone_no, customer_name, address, customer_type)

        self.phone_no = tk.StringVar()

        self.PhoneNo = tk.Entry(self.labelframeN1, textvariable=self.phone_no)
        self.PhoneNo.bind("<Return>", self.phone_no_bind_function)
        self.phone_no.set('')
        self.PhoneNo.grid(row=0, column=1, sticky=tk.W+tk.N)

        self.customer_name = tk.StringVar()

        self.CustomerName = tk.Entry(
            self.labelframeN1, textvariable=self.customer_name)
        self.CustomerName.bind("<Return>", self.customer_name_bind_function)
        self.customer_name.set('')
        self.CustomerName.grid(row=2, column=1, sticky=tk.W+tk.N)

        self.address = tk.StringVar()

        f1 = tk.Frame(self.labelframeN1)
        bary1 = tk.Scrollbar(f1)
        bary1.pack(side=tk.RIGHT, fill=tk.Y)
        self.Address = tk.Text(f1, width=27, height=1)
        self.Address.bind("<Return>", self.address_bind_function)
        self.address.set('')
        self.Address.pack(side=tk.LEFT, fill=tk.BOTH)
        bary1.config(command=self.Address.yview)
        self.Address.config(yscrollcommand=bary1.set)
        f1.grid(row=3, column=1, rowspan=3, columnspan=3, sticky=tk.W+tk.N)

        self.customer_type = tk.StringVar()

        self.CustomerType = tk.Entry(
            self.labelframeN1, textvariable=self.customer_type)
        self.customer_type.set('N/A')
        self.CustomerType.grid(row=0, column=3, sticky=tk.W+tk.N)

        # -----------------------------------treeview----------------------------
        invoice_list = ['Sr no', 'Product Code', 'Product Name',
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

        self.PhoneNo_focus()
    #focus
    def PhoneNo_focus(self):
        self.PhoneNo.focus_set()
    #menubar
    def stocks_window(self):
        self.stocks = stocks(self.master)
    
    #invoice
    def barcode_bind_function(self, event):
        pass

    def product_name_bind_function(self, event):
        pass

    def quantity_bind_function(self, event):
        pass

    def bill_add(self):
        pass

    def bill_remove(self):
        pass

    #customer details
    def phone_no_bind_function(self, event):
        pass

    def customer_name_bind_function(self, event):
        pass

    def address_bind_function(self, event):
        pass
    
    def enter_customer_details(self):
        #phone_no_bind_function(self)
        pass
        
    def clear_customer_details(self):
        self.PhoneNo.delete(0, tk.END)
        self.CustomerName.delete(0, tk.END)
        self.Address.delete('1.0', tk.END)
        self.CustomerType.delete(0, tk.END)

        self.phone_no.set('')
        self.customer_name.set('')
        self.address.set('')
        self.customer_type.set('N/A')


if __name__ == '__main__':

    root = tk.Tk()
    root.title('')

    myLogin = loginPage(root)

    # stock=stocks(root)

    # root.wait_window(myLogin.mySendMail.labelframe1)
    tk.mainloop()
