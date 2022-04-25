

from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="password"
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_DB']="ecommerce"
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = "super secret"

product_id = 0


mysql = MySQL(app)

@app.route("/customer/<cid>", methods=['GET', 'POST'])
def customer(cid):
    cur = mysql.connection.cursor()
    cur.execute("select * from _order")
    results = cur.fetchall()
    print(results)
    return render_template('customer.html',orders = results)  

@app.route("/",methods=["GET","POST"])
def hello_world():
    cur = mysql.connection.cursor()
    if request.method=='POST':
        if request.form['login/signup'] == 'login':
            entered_username = request.form['username']
            #print(entered_username)
            entered_pass = request.form['pass']
            entered_type = request.form['options']
            cur.execute("select exists(select * from user where username='"+str(entered_username)+"' and passwd='"+str(entered_pass)+"' and _type = '"+str(entered_type)+"')")
            result = cur.fetchall()
            first_value = list(result[0].items())[0][1]
            if first_value==1:
                if entered_type == 'C':
                    return redirect(url_for('customer', cid = entered_username))
                else:
                    return redirect(url_for('seller', sid = entered_username))
            else:
                flash("Incorrect Username/Password")
        elif request.form['login/signup'] == 'signup':
            pass
    cur.close()
    
    # cur = mysql.connection.cursor()
    # cur.execute("select * from user")
    # results = cur.fetchall()
    # cur.close()
    # print(results)
    return render_template('homepage.html')

@app.route('/products', methods=['GET', 'POST'])
def hello():
    cur = mysql.connection.cursor()
    cur.execute("select * from product")
    results = cur.fetchall()
    
    if request.method=='POST':
        cur.execute("insert into cart (p_id, c_id, quantity) values ('" + str(request.form['action1']) + "', 'imccollum2', '1')")
        cur.connection.commit()
    cur.close()
    return render_template('products.html', products = results)

@app.route("/cart", methods=['GET', 'POST'])
def cart():
    
    return render_template('cart.html')
@app.route("/seller/<sid>", methods=['GET', 'POST'])
def seller(sid):
    cur = mysql.connection.cursor()
    if request.method == "POST":
        if request.form['aud'] == 'add':
            # product_id = request.form['Product_id']
            global product_id
            product_id+=1
            product_name = request.form['Product_name']
            product_category = request.form['Product_category']
            product_price = request.form['Product_price']
            product_discount = request.form['Product_discount']
            product_image = request.form['Product_image']
            product_desc = request.form['Product_desc']
            cur.execute(f"insert into product (discount, category, p_id, s_id, price, images, _desc, p_name) values ('{product_discount}', '{product_category}', '{product_id}', '{sid}', '{product_price}', '{product_image}', '{product_desc}', '{product_name}')")
            cur.connection.commit()
        elif request.form['aud'] == 'updateProduct':
            product_id = request.form['Product_id']
            product_name = request.form['Product_name']
            product_category = request.form['Product_category']
            product_price = request.form['Product_price']
            product_discount = request.form['Product_discount']
            product_image = request.form['Product_image']
            product_desc = request.form['Product_desc']
            
    cur.close()
    return render_template('seller.html')    



if __name__ == "__main__":
    app.run(debug=True)