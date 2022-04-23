from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="password"
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_DB']="ecommerce"
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'




mysql = MySQL(app)

@app.route("/")
def login_page():
    print("jh")
    cur = mysql.connection.cursor()
    cur.execute("select * from user")
    results = cur.fetchall()
    cur.close()
    print(results)
    return render_template('homepage.html', item=results)

@app.route("/wtv")
def hello():
    return render_template('new.html')

if __name__ == "__main__":
    app.run(debug=True)