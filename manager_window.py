import datetime
import tkinter as tk
from tkinter import Toplevel
import tkinter.font as font
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
from smtplib import *
import sqlite3
db = sqlite3.connect('database.db')
c = db.cursor()


class manager_win(object):

    def __init__(self, master):
        self.master = master
        self.mas = Toplevel(self.master)
        self.mas.title('Manage store')

        # ----------------------------------menubar(File[Exit], About[About Me])
        menubar = tk.Menu(self.mas)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Exit', command=master.quit)
        menubar.add_cascade(label='File', menu=filemenu)

        aboutmenu = tk.Menu(menubar, tearoff=0)
        aboutmenu.add_command(label='About Me')
        menubar.add_cascade(label='About', menu=aboutmenu)

        self.mas['menu'] = menubar

        # labels
        tk.Label(self.mas, text='Master Functions', font=(
            "Times", "12", "bold")).grid(row=0, column=0)

        # buttons
        tk.Button(self.mas, text='Stocks', command=self.Stocks_button).grid(
            row=1, column=0, sticky=tk.N+tk.W, padx=10, pady=10, ipadx=36, ipady=5)
        # tk.Button(self.mas, text='Sales', command=self.Sales_button).grid(
        #     row=1, column=1, sticky=tk.N+tk.W, padx=10, pady=10, ipadx=36, ipady=5)
        tk.Button(self.mas, text='Employyee details', command=self.Employyee_details_button).grid(
            row=1, column=1, sticky=tk.N+tk.W, padx=10, pady=10, ipadx=5, ipady=5)
        # tk.Button(self.mas, text='Customer details', command=self.Customer_details_button).grid(
        #     row=2, column=1, sticky=tk.N+tk.W, padx=10, pady=10, ipadx=5, ipady=5)

    def Stocks_button(self):
        stock_window = stocks(self.master)

    def Sales_button(self):
        # sales_window = sales(self.master)
        pass

    def Employyee_details_button(self):
        # employyee_details = EmployyeeDetails(self.master)
        pass

    def Customer_details_button(self):
        # customer_details = CustomerDetails(self.master)
        pass


class stocks(object):
    '''
    retail price=wholesale price/(1-markup percentage[in decimal]) *markup percentage=profit margin
    '''

    def __init__(self, master, user=''):
        self.user = user
        self.mas = tk.Toplevel(master)
        self.mas.title('Stock Management')

        tabcontrol = ttk.Notebook(self.mas)

        tab2 = ttk.Frame(tabcontrol)

        # -----------------------------------treeview(stock available)----------------------------
        invoice_list = ['Product Code', 'Product Name',
                        'Quantity', 'Mrp', 'Price']
        listbar = tk.Frame(tab2)

        bary3 = tk.Scrollbar(listbar)
        bary3.pack(side=tk.RIGHT, fill=tk.Y)
        barx3 = tk.Scrollbar(listbar, orient=tk.HORIZONTAL)
        barx3.pack(side=tk.BOTTOM, fill=tk.X)

        self.invoiceList = ttk.Treeview(listbar, columns=invoice_list)
        self.invoiceList.column(column='#0', width=0, stretch=False)
        for i in range(len(invoice_list)):
            self.invoiceList.heading(i, text=invoice_list[i])
            self.invoiceList.column(i, width=200)
        self.invoiceList.column(1, width=100)
        self.invoiceList['height'] = 20
        self.invoiceList.pack(side=tk.LEFT, fill=tk.BOTH)

        self.id_1 = 1
        self.iid_1 = 0

        self.stocks = self.get_available_stock()
        for i in self.stocks:

            self.invoiceList.insert('', 'end', iid=self.iid_1, values=(i))

            self.id_1 += 1
            self.iid_1 += 1

        barx3.config(command=self.invoiceList.xview)
        bary3.config(command=self.invoiceList.yview)

        self.invoiceList.config(xscrollcommand=barx3.set,
                                yscrollcommand=bary3.set)

        listbar.pack(fill=tk.X)

        tabcontrol.add(tab2, text='stock available')
        tabcontrol.pack(expand=1, fill="both")

        tab3 = ttk.Frame(tabcontrol)

        tab = ttk.Frame(tabcontrol)

        # ----------------------------------labelframes(invoice)
        self.labelframe2 = tk.LabelFrame(tab, text="Add to Stocks")
        self.labelframe2.pack(side=tk.TOP, fill=tk.X)

        # ----------------------------------buttons(Add)
        tk.Button(self.labelframe2, text='Add', command=self.add_button).grid(
            row=3, column=1, sticky=tk.W+tk.N)

        # ----------------------------------labels(PRODUCT CODE , PRODUCT NAME, QUANTITY LEFT, Price per quantity)
        tk.Label(self.labelframe2, text='Date').grid(
            row=0, column=0, sticky=tk.W+tk.N)
        tk.Label(self.labelframe2, text='Product code ').grid(
            row=1, column=0, sticky=tk.W+tk.N)
        tk.Label(self.labelframe2, text='Product name').grid(
            row=1, column=2, sticky=tk.W+tk.N)
        tk.Label(self.labelframe2, text='Quantity').grid(
            row=1, column=4, sticky=tk.W+tk.N)
        tk.Label(self.labelframe2, text='Mrp').grid(
            row=2, column=0, sticky=tk.W+tk.N)
        tk.Label(self.labelframe2, text='Price per quantity').grid(
            row=2, column=2, sticky=tk.W+tk.N)
        # ----------------------------------entry(PRODUCT CODE, PRODUCT NAME, QUANTITY LEFT, Price per quantity) all are StringVar

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

        self.ProductCode = tk.Entry(
            self.labelframe2, textvariable=self.productcode)
        self.ProductCode.bind("<Return>", self.productcode_bind_function)
        self.productcode.set('')
        self.ProductCode.grid(row=1, column=1, sticky=tk.W+tk.N)

        self.product_name = tk.StringVar()

        self.ProductName = tk.Entry(
            self.labelframe2, textvariable=self.product_name)
        self.ProductName.bind("<Return>", self.product_name_bind_function)
        self.product_name.set('')
        self.ProductName.grid(row=1, column=3, sticky=tk.W+tk.N)

        self.quantity = tk.StringVar()

        self.Quantity = tk.Entry(
            self.labelframe2, textvariable=self.quantity)
        self.Quantity.bind("<Return>", self.quantity_bind_function)
        self.quantity.set('')
        self.Quantity.grid(row=1, column=5, sticky=tk.W+tk.N)

        self.mrp = tk.StringVar()

        self.Mrp = tk.Entry(
            self.labelframe2, textvariable=self.mrp)
        self.Mrp.bind("<Return>", self.mrp_bind_function)
        self.mrp.set('')
        self.Mrp.grid(row=2, column=1, sticky=tk.W+tk.N)

        self.price_per_quantity = tk.StringVar()

        self.PricePerQuantity = tk.Entry(
            self.labelframe2, textvariable=self.price_per_quantity)
        self.PricePerQuantity.bind("<Return>", self.price_per_quantity_bind_function)
        self.price_per_quantity.set('')
        self.PricePerQuantity.grid(row=2, column=3, sticky=tk.W+tk.N)

        tabcontrol.add(tab, text='add stock purchase details')
        tabcontrol.pack(expand=1, fill="both")

        # -----------------------------------treeview(purchase history)----------------------------
        invoice_list = ['date', 'Product Code', 'Product Name',
                        'Quantity', 'Mrp', 'Price Per Quantity']
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

        self.id_2 = 1
        self.iid_2 = 0

        self.history = self.get_stock_purchase_history()
        for i in self.history:

            self.invoiceList.insert('', 'end', iid=self.iid_2, values=(i))

            self.id_2 += 1
            self.iid_2 += 1

        barx3.config(command=self.invoiceList.xview)
        bary3.config(command=self.invoiceList.yview)

        self.invoiceList.config(xscrollcommand=barx3.set,
                                yscrollcommand=bary3.set)

        listbar.pack(fill=tk.X)

        tabcontrol.add(tab3, text='purchase history')
        tabcontrol.pack(expand=1, fill="both")
        self.ProductCode.focus_set()


    # database integration
    def get_available_stock(self):
        stocks = ()
        x = '''select product_code, product_name, quantity, mrp, price  
        from available_stock;'''
        c.execute(x)
        for i in c.fetchall():
            stocks += (i,)
        # print(stocks)

        return stocks

    def get_stock_purchase_history(self):
        history = ()
        x = '''select date_of_purchase, product_code, product_name, quantity, mrp, price   
        from stock_purchase_history;'''
        c.execute(x)
        for i in c.fetchall():
            history += (i,)
        print(history)

        return history


    def productcode_bind_function(self, event):
        self.ProductName.focus_set()


    def product_name_bind_function(self, event):
        self.quantity.focus_set()


    def quantity_bind_function(self, event):
        self.Mrp.focus_set()

    def mrp_bind_function(self, event):
        self.PricePerQuantity.focus_set()

    def price_per_quantity_bind_function(self, event):
        self.add_button()

    def add_button(self):
        # #update database
        # quantity=int(self.Quantity.get())
        # product_code=int(self.ProductCode.get())
        # product_name=self.ProductName.get()
        # date=self.Date.get()
        # mrp=int(self.Mrp.get())
        # price=int(self.PricePerQuantity.get())

        # x='''update available_stock
        # set quantity= quantity+?
        # where product_code=?'''
        # c.execute(x,(quantity,product_code))
        # x1='''insert into stock_purchase_history
        # (product_code, product_name, quantity, date_of_purchase, price, mrp)
        # values (?,?,?,?,?,?)'''
        # c.execute(x1,(product_code, product_name, quantity, date, price, mrp))
        pass


if __name__ == "__main__":
    root = tk.Tk()
    manager = manager_win(root)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 325
    window_height = 150
    x = (screen_width/2) - (window_width/2)
    y = (screen_height/2) - (window_height/2)
    root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
    tk.mainloop()
