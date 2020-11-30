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
  quantity      int(10),
  FOREIGN KEY(product_code) REFERENCES inventory(product_code),
  FOREIGN KEY(product_name) REFERENCES inventory(product_name));''',
          '''CREATE TABLE stock_purchase_history (
  product_code      int(13), 
  product_name      varchar(355), 
  quantity          int(10),
  date_of_purchase  date,
  FOREIGN KEY(product_code) REFERENCES inventory(product_code),
  FOREIGN KEY(product_name) REFERENCES inventory(product_name));''',
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
("000002","000002", "cashier");'''
                   )
# for i in insert_commands:
#     c.execute(i)
#     db.commit()
