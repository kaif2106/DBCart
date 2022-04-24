from unittest import result
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="kushiluv25"
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_DB']="ecommerce"
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'




mysql = MySQL(app)

@app.route("/",methods=["GET","POST"])
def hello_world():
    cur = mysql.connection.cursor()
    if request.method=='POST':
        if request.form['login/signup'] == 'login':
            entered_username = request.form['username']
            print(entered_username)
            entered_pass = request.form['pass']
            entered_type = request.form['options']
            cur.execute("select exists(select * from user where username='"+str(entered_username)+"' and passwd='"+str(entered_pass)+"')")
            result = cur.fetchall()
            first_value = list(result[0].items())[0][1]
            print(first_value)
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
@app.route("/seller", methods=['GET', 'POST'])
def seller():
    
    return render_template('seller.html')    

@app.route("/customer", methods=['GET', 'POST'])

def customer():
    cur = mysql.connection.cursor()
    cur.execute("select * from _order")
    results = cur.fetchall()
    print(results)
    return render_template('customer.html',orders = results) 

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