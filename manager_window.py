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

        # ----------------------------------menubar(File[Exit], About[About Me])
        menubar = tk.Menu(self.mas)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Exit', command=master.quit)
        menubar.add_cascade(label='File', menu=filemenu)

        aboutmenu = tk.Menu(menubar, tearoff=0)
        aboutmenu.add_command(label='About Me')
        menubar.add_cascade(label='About', menu=aboutmenu)

        self.mas['menu'] = menubar

        # frame
        self.frame = tk.Frame(self.mas).grid(
            row=0, column=0, columnspan=2, rowspan=2)

        # labels
        tk.Label(self.frame, text='Master Functions', font=(
            "Times", "12", "bold")).grid(row=0, column=0)

        # buttons
        tk.Button(self.mas, text='Stocks', command=self.Stocks_button).grid(
            row=1, column=0, sticky=tk.N+tk.W, padx=10, pady=10, ipadx=36, ipady=5)
        tk.Button(self.mas, text='Sales', command=self.Sales_button).grid(
            row=1, column=1, sticky=tk.N+tk.W, padx=10, pady=10, ipadx=36, ipady=5)
        tk.Button(self.mas, text='Employyee details', command=self.Employyee_details_button).grid(
            row=2, column=0, sticky=tk.N+tk.W, padx=10, pady=10, ipadx=5, ipady=5)
        tk.Button(self.mas, text='Customer details', command=self.Customer_details_button).grid(
            row=2, column=1, sticky=tk.N+tk.W, padx=10, pady=10, ipadx=5, ipady=5)

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

        self.ProductCode = tk.Entry(
            self.labelframe2, textvariable=self.productcode)
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
    # focus

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


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('325x150')
    manager = manager_win(root)
    screen_width=root.winfo_screenwidth()
    print(screen_width)
    tk.mainloop()
