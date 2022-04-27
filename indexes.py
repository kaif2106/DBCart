from flask import Flask, render_template, request, flash, url_for, redirect
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="password"
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_DB']="ecommerce"
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = "super secret"


mysql = MySQL(app)
mycursor = mysql.connection.cursor()

query="SHOW INDEX FROM ecommerce.user;"
mycursor.execute(query)
user = mycursor.fetchall()
print('Indexes for the table user: ')
for x in user:
   print(x)

query="SHOW INDEX FROM ecommerce.customer;"
mycursor.execute(query)
customer = mycursor.fetchall()
print('Indexes for the table customer: ')
for x in customer:
   print(x)

query="SHOW INDEX FROM ecommerce.seller;"
mycursor.execute(query)
seller = mycursor.fetchall()
print('Indexes for the table seller: ')
for x in seller:
   print(x)

query="SHOW INDEX FROM ecommerce.personal_info;"
mycursor.execute(query)
p_i = mycursor.fetchall()
print('Indexes for the table personal_info: ')
for x in p_i:
   print(x)

query="SHOW INDEX FROM ecommerce.product;"
mycursor.execute(query)
product = mycursor.fetchall()
print('Indexes for the table product: ')
for x in product:
   print(x)

query="SHOW INDEX FROM ecommerce.cart;"
mycursor.execute(query)
cart = mycursor.fetchall()
print('Indexes for the table cart: ')
for x in cart:
   print(x)

query="SHOW INDEX FROM ecommerce._order;"
mycursor.execute(query)
order = mycursor.fetchall()
print('Indexes for the table _order: ')
for x in order:
   print(x)

query="SHOW INDEX FROM ecommerce.history;"
mycursor.execute(query)
hist = mycursor.fetchall()
print('Indexes for the table history: ')
for x in hist:
   print(x)

query="SHOW INDEX FROM ecommerce.billing_info;"
mycursor.execute(query)
b_i = mycursor.fetchall()
print('Indexes for the table billing_info: ')
for x in b_i:
   print(x)

query="SHOW INDEX FROM ecommerce.shipping;"
mycursor.execute(query)
shipping = mycursor.fetchall()
print('Indexes for the table shipping: ')
for x in shipping:
   print(x)
