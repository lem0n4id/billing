from tkinter import *
import tkinter.font as font
import tkinter.ttk as ttk

root=Tk()
root.geometry('1200x600')
font2 = font.Font(family='ariel', size=10)


lblTitle = Label(root, font=('arial', 25), text='SALES INVOICE ', justify=CENTER)
lblTitle.place(x=470,y=0)

#group invoice
invoice_group = LabelFrame(root, text="invoice", padx=5, pady=5,width=1190,height=500)
invoice_group.place(x=5,y=100)

#motion
def motion(event):
    x,y=event.x,event.y
    print(f'{x},{y}')
root.bind('<Button-1>',motion)

#date

def Print1(*args):
    print('date:',date_entry.get())
    date_entry.delete(0, END)
date_entry = Entry(invoice_group,width =25,font =font2)
date_label = Label(invoice_group,text='date',font =font2)
date_label.place(x =5,y=5)
date_entry.place(x=110,y=5)
date_entry.bind("<Return>", Print1)

#invoice no
def Print2(*args):
    print('invoice no:',invoice_no_entry.get())
    invoice_no_entry.delete(0, END)
invoice_no_entry = Entry(invoice_group,width =25,font =font2)
invoice_no_label = Label(invoice_group,text='invoice no',font =font2)
invoice_no_label.place(x =5,y=30)
invoice_no_entry.place(x=110,y=30)
invoice_no_entry.bind("<Return>", Print2)

#phone no
def Print3(*args):
    print('phone no:',phone_no_entry.get())
    phone_no_entry.delete(0, END)
phone_no_entry = Entry(invoice_group,width =25,font =font2)
phone_no_label = Label(invoice_group,text='phone no',font =font2)
phone_no_label.place(x =880,y=5)
phone_no_entry.place(x=990,y=5)
phone_no_entry.bind("<Return>", Print3)

#customer name
def Print4(*args):
    print('customer name:',customer_name_entry.get())
    customer_name_entry.delete(0, END)
customer_name_entry = Entry(invoice_group,width =25,font =font2)
customer_name_label = Label(invoice_group,text='customer name',font =font2)
customer_name_label.place(x =880,y=30)
customer_name_entry.place(x=990,y=30)
customer_name_entry.bind("<Return>", Print4)

#address 
def Print5(*args):
    print('address:',address_text.get())
    address_text.delete(0, END)
address_text = Text(invoice_group, width=25, height=4, bg='white', bd=4, font=font2)
address_label = Label(invoice_group,text='address',font =font2)
address_label.place(x =880,y=55)
address_text.place(x=989,y=55)
address_text.bind("<Return>", Print5)




	



mainloop()
        
