import sqlite3


def select_query(x: str):
    c.execute(x)
    for i in c.fetchall():
        print(i)


def create_table_query(x: str):
    c.execute(x)
    db.commit()


db = sqlite3.connect('database.db')
c = db.cursor()
tables = ('''CREATE TABLE emp_details (
  emp_id   	varchar(6) not null primary key,
  name 	        varchar(355),
  desgn    	varchar(10),
  sex      	varchar(6),
  age      	int(2),
  address  	varchar(355),
  phone_no 	int(10),
  email_address varchar(355),
  date_joined   date);''',
          '''CREATE TABLE users (
  emp_id   varchar(6) not null,
  password varchar(6),
  desgn    varchar(10),
  FOREIGN KEY(emp_id) REFERENCES emp_details(emp_id));''',
          '''CREATE TABLE inventory (
  product_code  int(13) not null primary key, 
  product_name  varchar(355) not null);''',
          '''CREATE TABLE available_stock (
  product_code  int(13), 
  product_name  varchar(355), 
  quantity      int(10));''',
          '''CREATE TABLE stock_purchase_history (
  product_code      int(13), 
  product_name      varchar(355), 
  quantity          int(10),
  date_of_purchase  date);''',
          '''CREATE TABLE customer_details (
  m_id 		int(10),
  name 		varchar(355),
  phone_no 	int(10),
  email_address varchar(355));'''
          )
# for i in tables:
#   create_table_query(tables[5])
# select_query('select * from sqlite_master')
insert_commands = ('''
insert into emp_details
(emp_id, name, desgn, sex, age, address, phone_no, email_address, date_joined)
values
("000001", "yashas", "manager", "male", 18, "seawoods", "1234567890", "yashas123@gmail.com", "2020-11-30"),
("000002", "rohan", "cashier", "male", 21, "nerul", "1111111110", "rohan123@gmail.com", "2020-11-30");''',
                   '''
insert into users
(emp_id, password, desgn)
values
("000001","000001", "manager"),
("000002","000002", "cashier");''',
                   '''
insert into stock_purchase_history 
(product_code, product_name, quantity, date_of_purchase)
values (90162602, "red bull 250ml", 120, "2020-10-25"),
(8515135837011, "colgate maxfresh toothpaste", 200, "2020-10-25");''',
                   '''
insert into available_stock
(product_code, product_name, quantity)
values (90162602, "red bull 250ml", 120),
(8515135837011, "colgate maxfresh toothpaste", 200);''',
                   '''
insert into customer_details
(m_id, name, phone_no, email_address)
values (000001, 'ramprasad', 1124578945, 'ramprasad111@gmail.com'),
(000002, 'dev', 1547649164, 'dev64@gmail.com')
                '''
                   )
# for i in insert_commands:
#     c.execute(i)
#     db.commit()

# # retrive name using emp_id
# x='''select name from emp_details
#     where emp_id = ?'''
# emp_id='000001'
# c.execute(x,(emp_id,))
# for i in c.fetchall():
#     print(i[0])


# # retrive customer_name, email_address, membership_id using phone_no
# x='''
# select name, email_address, m_id
# from customer_details
# where phone_no = ?'''
# phone_no=1234567890
# c.execute(x,(phone_no,))

# retrive product_name, mrp, price using product_code

# #available_stock
# x='''select product_code,product_name,quantity from available_stock;'''
# c.execute(x)
# for i in c.fetchall():
#     product_code, product_name, quantity = i
#     # insert into treeview(product_code, product_name, quantity)

# #inserting into purchase_history
# c.execute(insert_commands[2])
# db.commit()

# x='''select product_code, product_name, quantity, date_of_purchase
#         from stock_purchase_history;'''
# c.execute(x)
# for i in c.fetchall():
#     print(i)

# #inserting into available_stock
# c.execute(insert_commands[3])
# db.commit()

# #inserting into customer_details
# c.execute(insert_commands[4])
# db.commit()
select_query('select * from customer_details')