#from tkinter import *
'''
#menubar
root = Tk()

def hello():
    print("hello!")

# create a toplevel menu 
menubar = Menu(root)
menubar.add_command(label="Hello!", command=hello)
menubar.add_command(label="Quit!", command=root.quit)

# display the menu
root.config(menu=menubar)
'''
'''
#menubar
root = Tk()

def hello():
    print("hello!")

menubar = Menu(root)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=hello)
filemenu.add_command(label="Save", command=hello)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=hello)
editmenu.add_command(label="Copy", command=hello)
editmenu.add_command(label="Paste", command=hello)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=hello)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menubar)

'''
'''
#menubar with counter
counter = 0

def update():
    global counter
    counter = counter + 1
    menu.entryconfig(0, label=str(counter))

root = Tk()

menubar = Menu(root)

menu = Menu(menubar, tearoff=0, postcommand=update)
menu.add_command(label=str(counter))
menu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="Test", menu=menu)

root.config(menu=menubar)
'''
'''
#do you want to exit?
from tkinter.messagebox import *
#use help(tkinter.messagebox) for info
def callback():
    if askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()

root = Tk()
root.protocol("WM_DELETE_WINDOW", callback)

root.mainloop()
'''
'''
#menubar and status bar
def callback():
    print("called the callback!")

root = Tk()

# create a menu
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=callback)
filemenu.add_command(label="Open...", command=callback)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=callback)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=callback)

status = Label(root, text="", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

mainloop()
'''
'''
root = Tk()
from tkinter.simpledialog import *
class MyDialog(Dialog):

    def body(self, master):

        Label(master, text="Username:").grid(row=0)
        Label(master, text="Password:").grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        first = str(self.e1.get())
        second = (self.e2.get())
        self.result = first, second

d = MyDialog(root)
print(d.result)
'''
# Python program to create a table 

from tkinter import *


class Table: 
	
	def __init__(self,root): 
		
		# code for creating table 
		for i in range(total_rows): 
			for j in range(total_columns): 
				
				self.e = Entry(root, width=20, fg='blue', 
							font=('Arial',16,'bold')) 
				
				self.e.grid(row=i, column=j) 
				self.e.insert(END, lst[i][j]) 

# take the data 
lst = [(1,'Raj','Mumbai',19), 
	(2,'Aaryan','Pune',18), 
	(3,'Vaishnavi','Mumbai',20), 
	(4,'Rachna','Mumbai',21), 
	(5,'Shubham','Delhi',21)] 

# find total number of rows and 
# columns in list 
total_rows = len(lst) 
total_columns = len(lst[0]) 

# create root window 
root = Tk() 
t = Table(root) 
root.mainloop() 
