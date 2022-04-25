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
    if request.method == "POST":
        if request.form['aud'] == 'updateCustomer':
            customer_first_name = request.form['First_name']
            customer_last_name = request.form['Last_name']
            pincode = request.form['Pincode']
            ph_num = request.form['Phone_num']
            email = request.form['email']
            add_line1 = request.form['add_line1']
            add_line2 = request.form['add_line2']
            landmark = request.form['Landmark']
            cur.execute(f"update personal_info set first_name = '{customer_first_name}', last_name = '{customer_last_name}', add_line1 = '{add_line1}', add_line2 = '{add_line2}', landmark = '{landmark}', pincode = '{pincode}', ph_no = '{ph_num}', email_id = '{email}' where username='{cid}'")
            cur.connection.commit()
    cur.close()
    return render_template('customer.html')  

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
    return render_template('homepage.html')

@app.route('/products/<cid>', methods=['GET', 'POST'])
def products(cid):
    cur = mysql.connection.cursor()
    cur.execute("select * from product")
    results = cur.fetchall()
    if request.method=='POST':
        cur.execute(f"insert into cart (p_id, c_id, quantity) values ('{request.form['action1']}', '{cid}', '1')")
        cur.connection.commit()
        select = request.form.get('quantity')
        print(str(select))
        
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
            
        elif request.form['aud'] == 'updateProduct':
            local_product_id = request.form['Product_id']
            product_name = request.form['Product_name']
            product_category = request.form['Product_category']
            product_price = request.form['Product_price']
            product_discount = request.form['Product_discount']
            product_image = request.form['Product_image']
            product_desc = request.form['Product_desc']
            cur.execute(f"update product set p_name = '{product_name}', category='{product_category}', price = '{product_price}', discount='{product_discount}', images = '{product_image}', _desc = '{product_desc}' where p_id='{local_product_id}' and s_id = '{sid}'")
            
        elif request.form['aud'] == 'delete':
            local_product_id = request.form['Product_id']
            cur.execute(f"delete from product where p_id='{local_product_id}'")

        elif request.form['aud'] == 'updateSeller':
            seller_first_name = request.form['First_name']
            seller_last_name = request.form['Last_name']
            pincode = request.form['Pincode']
            ph_num = request.form['Phone_num']
            email = request.form['email']
            add_line1 = request.form['add_line1']
            add_line2 = request.form['add_line2']
            landmark = request.form['Landmark']
            cur.execute(f"update personal_info set first_name = '{seller_first_name}', last_name = '{seller_last_name}', add_line1 = '{add_line1}', add_line2 = '{add_line2}', landmark = '{landmark}', pincode = '{pincode}', ph_no = '{ph_num}', email_id = '{email}' where username='{sid}'")


    cur.connection.commit()
    cur.close()
    return render_template('seller.html')    


@app.route("/history", methods=['GET', 'POST'])

def history():
    cur = mysql.connection.cursor()
    cur.execute("SELECT history.quantity, history.order_date ,history.p_id,history.order_id,history._status,product.p_name ,product.price ,product.category ,product.images,product.s_id,product._desc FROM history INNER JOIN product ON history.p_id=product.p_id;")
    results = cur.fetchall()
    for i in results:
        i['price'] = "{:.2f}".format(i['price']*i['quantity'])
    
    return render_template('history.html',history = results) 

if __name__ == "__main__":
    app.run(debug=True)