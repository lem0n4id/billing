import datetime
import tkinter as tk
from tkinter import Toplevel
import tkinter.font as font
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
import sqlite3
db = sqlite3.connect('database.db')
c = db.cursor()


class manager_win(object):

    def __init__(self, master):
        self.master = master
        self.mas = Toplevel(self.master)
        self.mas.title('Manage store')

        # ----------------------------------menubar(File[Exit])

        menubar = tk.Menu(self.mas)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Exit', command=master.quit)
        menubar.add_cascade(label='File', menu=filemenu)

        self.mas['menu'] = menubar

        # ----------------------------------label

        tk.Label(self.mas, text='Master Functions', font=(
            "Times", "12", "bold")).grid(row=0, column=0)

        # ----------------------------------buttons

        tk.Button(self.mas, text='Stocks', command=self.Stocks_button).grid(
            row=1, column=0, sticky=tk.N+tk.W, padx=10, pady=10, ipadx=36, ipady=5)

        tk.Button(self.mas, text='Employyee details', command=self.Employyee_details_button).grid(
            row=1, column=1, sticky=tk.N+tk.W, padx=10, pady=10, ipadx=5, ipady=5)

    def Stocks_button(self):
        stock_window = stocks(self.master)

    def Employyee_details_button(self):
        employyee_details = EmployyeeDetails(self.master)
        pass


class stocks(object):

    def __init__(self, master, user=''):
        self.user = user
        self.mas = tk.Toplevel(master)
        self.mas.title('Stock Management')

        tabcontrol = ttk.Notebook(self.mas)

        frame = ttk.Frame(tabcontrol)

        # ----------------------------------treeview(stock available)

        invoice_list = ['Product Code', 'Product Name',
                        'Quantity', 'Mrp', 'Price']
        listbar = tk.Frame(frame)

        bary3 = tk.Scrollbar(listbar)
        bary3.pack(side=tk.RIGHT, fill=tk.Y)
        barx3 = tk.Scrollbar(listbar, orient=tk.HORIZONTAL)
        barx3.pack(side=tk.BOTTOM, fill=tk.X)

        self.StockList = ttk.Treeview(listbar, columns=invoice_list)
        self.StockList.column(column='#0', width=0, stretch=False)
        for i in range(len(invoice_list)):
            self.StockList.heading(i, text=invoice_list[i])
            self.StockList.column(i, width=200)
        self.StockList.column(1, width=100)
        self.StockList['height'] = 20
        self.StockList.pack(side=tk.LEFT, fill=tk.BOTH)

        self.iid_1 = 0
        self.available_stock_inserted = []

        self.stocks = self.get_available_stock()
        for i in self.stocks:

            self.StockList.insert('', 'end', iid=self.iid_1, values=(i))
            self.available_stock_inserted.append([i, self.iid_1])

            self.iid_1 += 1

        print(self.available_stock_inserted)

        barx3.config(command=self.StockList.xview)
        bary3.config(command=self.StockList.yview)

        self.StockList.config(xscrollcommand=barx3.set,
                              yscrollcommand=bary3.set)

        listbar.pack(fill=tk.X)

        tabcontrol.add(frame, text='stock available')
        tabcontrol.pack(expand=1, fill="both")

        tab3 = ttk.Frame(tabcontrol)

        tab = ttk.Frame(tabcontrol)

        # ----------------------------------labelframes(Add to Stocks)

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

        # ----------------------------------entry(PRODUCT CODE, PRODUCT NAME, QUANTITY LEFT, Price per quantity)

        self.date = tk.StringVar()

        # today's date
        formatted_date = datetime.date.strftime(
            datetime.date.today(), "%m/%d/%Y")

        self.Date = tk.Entry(self.labelframe2, textvariable=self.date)
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
        self.PricePerQuantity.bind(
            "<Return>", self.price_per_quantity_bind_function)
        self.price_per_quantity.set('')
        self.PricePerQuantity.grid(row=2, column=3, sticky=tk.W+tk.N)

        tabcontrol.add(tab, text='add stock purchase details')
        tabcontrol.pack(expand=1, fill="both")

        # ----------------------------------treeview(purchase history)
        invoice_list = ['date', 'Product Code', 'Product Name',
                        'Quantity', 'Mrp', 'Price Per Quantity']
        listbar = tk.Frame(tab3)

        bary3 = tk.Scrollbar(listbar)
        bary3.pack(side=tk.RIGHT, fill=tk.Y)
        barx3 = tk.Scrollbar(listbar, orient=tk.HORIZONTAL)
        barx3.pack(side=tk.BOTTOM, fill=tk.X)

        self.PurchaseHistoryList = ttk.Treeview(listbar, columns=invoice_list)
        self.PurchaseHistoryList.column(column='#0', width=0, stretch=False)
        for i in range(len(invoice_list)):
            self.PurchaseHistoryList.heading(i, text=invoice_list[i])
            self.PurchaseHistoryList.column(i, width=200)
        self.PurchaseHistoryList.column(1, width=100)
        self.PurchaseHistoryList['height'] = 20
        self.PurchaseHistoryList.pack(side=tk.LEFT, fill=tk.BOTH)

        self.iid_2 = 0

        self.history = self.get_stock_purchase_history()

        # debug
        self.purchase_history_inserted = []

        for i in self.history:

            self.PurchaseHistoryList.insert(
                '', 'end', iid=self.iid_2, values=(i))
            self.purchase_history_inserted.append([i, self.iid_2])

            self.iid_2 += 1

        barx3.config(command=self.PurchaseHistoryList.xview)
        bary3.config(command=self.PurchaseHistoryList.yview)

        self.PurchaseHistoryList.config(xscrollcommand=barx3.set,
                                        yscrollcommand=bary3.set)

        listbar.pack(fill=tk.X)

        tabcontrol.add(tab3, text='purchase history')
        tabcontrol.pack(expand=1, fill="both")

        self.ProductCode.focus_set()

    def get_available_stock(self):
        stocks = ()
        x = '''select product_code, product_name, quantity, mrp, price  
        from available_stock;'''
        c.execute(x)
        for i in c.fetchall():
            stocks += (i,)

        return stocks

    def get_stock_purchase_history(self):
        history = ()
        x = '''select date_of_purchase, product_code, product_name, quantity, mrp, price   
        from stock_purchase_history;'''
        c.execute(x)
        for i in c.fetchall():
            history += (i,)

        return history

    def insert_available_stock(self):
        stocks = self.get_available_stock()
        self.StockList.insert('', 'end', iid=self.iid_1, values=(stocks[-1]))
        self.iid_1 += 1

    def insert_stock_purchase_history(self):
        history = self.get_stock_purchase_history()
        self.PurchaseHistoryList.insert(
            '', 'end', iid=self.iid_2, values=(history[-1]))

    def update_available_stock(self, product_code, quantity):
        row_id = 0

        for i in self.available_stock_inserted:
            if i[0][0] == product_code:
                row_id = i[1]
                print(row_id, type(row_id))
                product_name = i[0][1]
                Quantity = i[0][2]
                mrp = i[0][3]
                price = i[0][4]

        try:
            self.StockList.delete(row_id)
            Quantity += quantity

            self.StockList.insert('', 'end', iid=row_id, values=(
                product_code, product_name, Quantity, mrp, price))
            return True
        except:
            tkMessageBox.showerror(
                'ERROR!', 'Cannot update the item right now, please restart the app!')
            return False

    # function to check if product code is in self.available_stock_inserted
    def check_if_in_available_stock_inserted(self, product_code):
        there = False
        for i in self.available_stock_inserted:
            if i[0][0] == product_code:
                there = True
        return there

    def productcode_bind_function(self, event):

        product_code = int(self.ProductCode.get())
        if self.check_if_in_available_stock_inserted(product_code):

            for i in self.available_stock_inserted:
                if i[0][0] == product_code:
                    product_name = i[0][1]
                    Quantity = i[0][2]
                    mrp = i[0][3]
                    price = i[0][4]

                    self.product_name.set(product_name)
                    self.mrp.set(str(mrp))
                    self.price_per_quantity.set(str(price))
                    self.Quantity.focus_set()
                    break
        else:
            tkMessageBox.showwarning(
                'Alert', 'New productcode, add all details')

        self.ProductName.focus_set()

    def product_name_bind_function(self, event):
        self.Quantity.focus_set()

    def quantity_bind_function(self, event):
        self.Mrp.focus_set()

    def mrp_bind_function(self, event):
        self.PricePerQuantity.focus_set()

    def price_per_quantity_bind_function(self, event):
        self.add_button()

    def product_codes(self):
        x = '''select product_code from available_stock'''
        c.execute(x)
        product_codes = c.fetchall()
        return product_codes

    def clear_enteries(self):
        self.ProductCode.delete(0, tk.END)
        self.ProductName.delete(0, tk.END)
        self.Quantity.delete(0, tk.END)
        self.Mrp.delete(0, tk.END)
        self.PricePerQuantity.delete(0, tk.END)

        self.product_name.set('')
        self.productcode.set('')
        self.quantity.set('')
        self.mrp.set('')
        self.price_per_quantity.set('')

    def add_button(self):
        quantity = int(self.Quantity.get())
        product_code = int(self.ProductCode.get())
        product_name = self.ProductName.get()
        date = self.Date.get()
        mrp = int(self.Mrp.get())
        price = int(self.PricePerQuantity.get())

        # insert into stock_purchase_history ,update available_stock
        if self.check_if_in_available_stock_inserted(product_code) == True:

            a = self.update_available_stock(product_code, quantity)
            if a == True:
                x = '''update available_stock
                set quantity= quantity+?
                where product_code=?'''
                c.execute(x, (quantity, product_code))

                x1 = '''insert into stock_purchase_history
                (product_code, product_name, quantity, date_of_purchase, price, mrp)
                values (?,?,?,?,?,?)'''
                c.execute(x1, (product_code, product_name,
                               quantity, date, price, mrp))

                db.commit()

                self.insert_stock_purchase_history()
                self.iid_2 += 1

                self.clear_enteries()
        else:  # insert into stock_purchase_history ,insert into available_stock
            self.available_stock_inserted += [
                [(product_code, product_name, quantity, mrp, price), self.iid_1]]
            self.iid_1 += 1

            x = '''insert into available_stock
            (product_code, product_name, quantity, price, mrp)
            values(?,?,?,?,?)'''
            c.execute(x, (product_code, product_name, quantity, price, mrp))

            x1 = '''insert into stock_purchase_history
            (product_code, product_name, quantity, date_of_purchase, price, mrp)
            values (?,?,?,?,?,?)'''
            c.execute(x1, (product_code, product_name,
                           quantity, date, price, mrp))

            db.commit()

            self.insert_available_stock()
            self.insert_stock_purchase_history()
            self.iid_2 += 1

            self.clear_enteries()


class EmployyeeDetails(object):
    def __init__(self, master, user=''):
        self.user = user
        self.mas = tk.Toplevel(master)
        self.mas.title('Employyee Details')

        # ----------------------------------menubar(File[Exit])
        menubar = tk.Menu(self.mas)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Exit', command=master.quit)
        menubar.add_cascade(label='File', menu=filemenu)

        self.mas['menu'] = menubar

        # ----------------------------------treeview(employyee details)
        invoice_list = ['emp_id', 'name', 'desgn', 'sex', 'age',
                        'address', 'phone_no', 'email_address', 'date_joined']
        listbar = tk.Frame(self.mas)

        bary3 = tk.Scrollbar(listbar)
        bary3.pack(side=tk.RIGHT, fill=tk.Y)
        barx3 = tk.Scrollbar(listbar, orient=tk.HORIZONTAL)
        barx3.pack(side=tk.BOTTOM, fill=tk.X)

        self.EmployyeeList = ttk.Treeview(listbar, columns=invoice_list)
        self.EmployyeeList.column(column='#0', width=0, stretch=False)
        for i in range(len(invoice_list)):
            self.EmployyeeList.heading(i, text=invoice_list[i])
            self.EmployyeeList.column(i, width=200)
        self.EmployyeeList.column(1, width=100)
        self.EmployyeeList['height'] = 20
        self.EmployyeeList.pack(side=tk.LEFT, fill=tk.BOTH)

        self.employyees = self.get_details()
        for i in self.employyees:

            self.EmployyeeList.insert('', 'end',  values=(i))

        barx3.config(command=self.EmployyeeList.xview)
        bary3.config(command=self.EmployyeeList.yview)

        self.EmployyeeList.config(xscrollcommand=barx3.set,
                                  yscrollcommand=bary3.set)

        listbar.pack(fill=tk.X)

    def get_details(self):

        x = '''select emp_id, name, desgn, sex, age, address, phone_no, email_address, date_joined
         from emp_details'''
        c.execute(x)

        return c.fetchall()


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
