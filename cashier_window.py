import datetime
import tkinter as tk
from tkinter import Toplevel
import tkinter.font as font
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
import sqlite3
db = sqlite3.connect('database.db')
c = db.cursor()


class invoice(object):
    def __init__(self, master, user=''):
        self.master = master
        self.user = user
        self.DATALIST = {}

        self.mas = tk.Toplevel(master)
        self.mas.title('Billing')

        # ----------------------------------menubar(File[Exit])
        menubar = tk.Menu(self.mas)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Exit', command=master.quit)
        menubar.add_cascade(label='File', menu=filemenu)

        self.mas['menu'] = menubar
        # ----------------------------------labelframes and frames

        self.labelframeN = tk.LabelFrame(
            self.mas, text="Employyee details")
        self.labelframeN.pack(side=tk.TOP, fill=tk.X)

        self.frame = tk.Frame(self.mas)
        self.frame.pack(side=tk.TOP, fill=tk.X)

        self.labelframe1 = tk.LabelFrame(
            self.frame, text="billing")
        self.labelframe1.pack(side=tk.LEFT, fill=tk.BOTH)

        self.labelframeN1 = tk.LabelFrame(
            self.frame, text="customer details")
        self.labelframeN1.pack(side=tk.LEFT, fill=tk.BOTH)

        self.labelframeN2 = tk.LabelFrame(
            self.frame, text="total")
        self.labelframeN2.pack(side=tk.LEFT, fill=tk.BOTH)

        # ----------------------------------buttons in Employyee details(logout)

        tk.Button(self.labelframeN, text='logout', command=self.mas.quit).grid(
            row=2, column=0, sticky=tk.W+tk.N)

        # ----------------------------------labels in Employyee details(User)

        tk.Label(self.labelframeN, text='User: ').grid(
            row=0, column=0, sticky=tk.W+tk.N)

        tk.Label(self.labelframeN, text=user).grid(
            row=0, column=1, sticky=tk.W+tk.N)

        tk.Label(self.labelframeN, text='Name: ').grid(
            row=1, column=0, sticky=tk.W+tk.N)

        self.name = self.get_name(user)
        tk.Label(self.labelframeN, text=self.name).grid(
            row=1, column=1, sticky=tk.W+tk.N)

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

        # ----------------------------------entries in invoice(productcode, product_name, quantity)

        self.productcode = tk.StringVar()

        self.ProductCode = tk.Entry(
            self.labelframe1, textvariable=self.productcode)
        self.ProductCode.bind("<Return>", self.productcode_bind_function)
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
            row=4, column=0, sticky=tk.W+tk.N)

        tk.Button(self.labelframeN1, text='Clear', command=self.clear_customer_details).grid(
            row=4, column=1, sticky=tk.W+tk.N)

        # ----------------------------------labels in customer details(PHONE NO, ADDRESS, CUSTOMER NAME)

        tk.Label(self.labelframeN1, text='Phone No').grid(
            row=0, column=0, sticky=tk.W+tk.N)

        tk.Label(self.labelframeN1, text='Customer Name').grid(
            row=2, column=0, sticky=tk.W+tk.N)

        tk.Label(self.labelframeN1, text='Email Address').grid(
            row=3, column=0, sticky=tk.W+tk.N)

        tk.Label(self.labelframeN1, text='Membership id:').grid(
            row=0, column=2, sticky=tk.W+tk.N)

        # ----------------------------------entries in customer details(phone_no, customer_name, address, customer_type)

        self.phone_no = tk.StringVar()

        self.PhoneNo = tk.Entry(self.labelframeN1)
        self.PhoneNo.bind("<Return>", self.phone_no_bind_function)
        self.PhoneNo.grid(row=0, column=1, sticky=tk.W+tk.N)

        self.customer_name = tk.StringVar()

        self.CustomerName = tk.Entry(
            self.labelframeN1, textvariable=self.customer_name)
        self.CustomerName.bind("<Return>", self.customer_name_bind_function)
        self.customer_name.set('')
        self.CustomerName.grid(row=2, column=1, sticky=tk.W+tk.N)

        self.email_address = tk.StringVar()

        self.EmailAddress = tk.Entry(
            self.labelframeN1, textvariable=self.email_address)
        self.EmailAddress.bind("<Return>", self.email_address_bind_function)
        self.email_address.set('')
        self.EmailAddress.grid(row=3, column=1, sticky=tk.W+tk.N)

        self.membership_id = tk.StringVar()

        self.MembershipId = tk.Entry(
            self.labelframeN1, textvariable=self.membership_id)
        self.membership_id.set('N/A')
        self.MembershipId.grid(row=0, column=3, sticky=tk.W+tk.N)

        # -----------------------------------treeview----------------------------

        invoice_list = ['Sr no', 'Product Code', 'Product Name',
                        'MRP', 'Price', 'Quantity', 'Total']
        self.items_billed = []

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
        self.invoiceList.pack(side=tk.LEFT, fill=tk.BOTH)

        self.id = 0
        self.iid = 0

        barx3.config(command=self.invoiceList.xview)
        bary3.config(command=self.invoiceList.yview)

        self.invoiceList.config(xscrollcommand=barx3.set,
                                yscrollcommand=bary3.set)

        listbar.pack(fill=tk.X)

        self.PhoneNo.focus_set()

        # ----------------------------------label in total

        tk.Label(self.labelframeN2, text='Total ').grid(
            row=0, column=0, sticky=tk.W+tk.N)

        # ----------------------------------Entry in total

        self.total = tk.IntVar()
        self.inttotal = 0

        self.Total = tk.Entry(
            self.labelframeN2, textvariable=self.total)
        self.total.set(self.inttotal)
        self.Total.grid(row=0, column=1, sticky=tk.W+tk.N)

        # ----------------------------------Button in total

        tk.Button(self.labelframeN2, text='Pay', command=self.thank_you_window).grid(
            row=1, column=1, sticky=tk.W+tk.N)

    def get_name(self, emp_id):
        x = '''select name from emp_details 
        where emp_id = ?'''
        name = ''
        c.execute(x, (emp_id,))
        for i in c.fetchall():
            name = i[0]
        return name

    def get_productcode(self):
        x = '''select product_name, quantity from available_stock
            where product_code=?'''
        product_code = int(self.ProductCode.get())
        c.execute(x, (product_code,))
        try:
            product_name, quantity_available = c.fetchall()[0]
            self.product_name.set(product_name)
            self.ProductName.focus_set()
            return (product_code, product_name, int(quantity_available))
        except:
            tkMessageBox.showinfo(
                'Notice', 'please enter a valid product code')
            return (0, 0, 0)

    def productcode_bind_function(self, event):
        product_code, product_name, quantity_available = self.get_productcode()

    def product_name_bind_function(self, event):
        self.Quantity.focus_set()

    def quantity_bind_function(self, event):
        product_code, product_name, quantity_available = self.get_productcode()

        quantity = self.Quantity.get()
        if quantity == '':
            tkMessageBox.showinfo('Notice', 'please enter a valid quantity')
        try:

            if quantity_available - int(self.Quantity.get()) < 0:
                raise ArithmeticError
            else:
                self.ProductCode.focus_get()
                self.bill_add()
        except:
            tkMessageBox.showinfo(
                'Notice', 'please enter a valid quantity,stock not available')

    def bill_add(self):
        self.id += 1
        self.iid += 1
        # add into treeview(productcode, productname,mrp,price,quantity,total)
        productcode = int(self.ProductCode.get().strip().lower())
        productname = self.ProductName.get().strip().lower()
        quantity = int(self.Quantity.get().strip().lower())

        x = '''select mrp,price from available_stock
        where product_code = ?'''
        c.execute(x, (productcode,))
        mrp, price = c.fetchone()
        total = price*quantity

        self.inttotal += total
        self.total.set(self.inttotal)

        item = (productcode, productname, mrp, price, quantity, total)
        self.invoiceList.insert('', 'end', iid=self.iid,
                                values=((self.id,)+item))

        self.clear_billing()

        self.items_billed.append([item, self.iid])

    def bill_remove(self):
        row_id = int(self.iid)
        try:

            for i in range(0, (len(self.items_billed)+1)):
                # print(i)
                # print('self.items_billed[i][1]',self.items_billed[i][1],type(self.items_billed[i][1]))
                # print('row_id',row_id,type(row_id))

                if self.items_billed[i][1] == row_id:
                    total = self.items_billed[0][0][5]
                    break

            self.inttotal -= total
            self.total.set(self.inttotal)

            self.iid -= 1
            self.id -= 1
            self.invoiceList.delete(row_id)
        except:
            tkMessageBox.showinfo('Notice', 'error- no entry to remove')

    # customer details

    def phone_no_bind_function(self, event):
        x = '''
        select name, email_address, m_id from customer_details where phone_no = ?'''
        phone_no = self.PhoneNo.get().strip()
        print(phone_no)
        c.execute(x, (phone_no,))
        try:
            name, email, m_id = c.fetchall()[0]
            print(name, len(name))
            self.customer_name.set(name)
            self.email_address.set(email)
            self.membership_id.set(m_id)
        except:
            tkMessageBox.showinfo(
                'Notice', 'phone no. does not exist, please enter a valid phone no.')

    def customer_name_bind_function(self, event):
        pass

    def email_address_bind_function(self, event):
        pass

    def enter_customer_details(self):
        self.phone_no_bind_function(self)
        pass

    def clear_billing(self):
        self.ProductCode.delete(0, tk.END)
        self.ProductName.delete(0, tk.END)
        self.Quantity.delete(0, tk.END)

        self.productcode.set('')
        self.product_name.set('')
        self.quantity.set('')

    def clear_customer_details(self):
        self.PhoneNo.delete(0, tk.END)
        self.CustomerName.delete(0, tk.END)
        self.EmailAddress.delete(0, tk.END)
        self.MembershipId.delete(0, tk.END)

        self.phone_no.set('')
        self.customer_name.set('')
        self.email_address.set('')
        self.membership_id.set('N/A')

    def thank_you_window(self):

        for i in range(len(self.items_billed)):
            product_code = self.items_billed[i][0][0]
            product_name = self.items_billed[i][0][1]
            quantity = self.items_billed[i][0][4]

            x = '''select product_name, quantity from available_stock
            where product_code=?'''
            c.execute(x, (product_code,))
            try:
                product_name, quantity_available = c.fetchall()[0]
                if (quantity_available - int(quantity)) < 0:
                    raise ArithmeticError
                else:
                    x = '''update available_stock
                    set quantity = quantity - ?
                    where product_code = ?'''
                    c.execute(x, (quantity, product_code))
                    db.commit()
                    self.mas1 = Toplevel(self.mas)
                    self.mas1.title('window')
                    tk.Label(self.mas1, text='Thank you for shopping!').grid(
                        row=0, column=0, sticky=tk.W+tk.N)
                    tk.Button(self.mas1, text='Okay!', command=self.mas1.quit).grid(
                        row=1, column=0, sticky=tk.W+tk.N)

            except:
                tkMessageBox.showinfo(
                    'Notice', f'not enough stock of {product_name}')


if __name__ == "__main__":
    root = tk.Tk()
    manager = invoice(root, '000001')

    tk.mainloop()
