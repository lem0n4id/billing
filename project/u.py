def create():
    global d
    d = {}
    while True:
        a = input('enter the name')
        b = input('enter the marks')
        d[a] = b
        c = int(input('press 1 to continue, press 2 to exit'))
        if c == 1:
            continue
        elif c == 2:
            break
def disp():
    if  len(d.items()) > 0:
        print(d)
    else:
        print('the dictionary is empty')

def rec(a):
    if a in d.items():
        print(d[a])
    else:
        print('the given name doesnot exists')
while True:
    f = int(input('press 1 to create,press 2 to display,press 3 to display marks,press 4 to exit'))
    if f == 1:            
        create()
    elif f == 2:
        disp()
    elif f == 3:
        a = input('enter the name')
        rec(a)
    elif f == 4:
        break            
