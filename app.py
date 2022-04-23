from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="kushiluv25"
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_DB']="ecommerce"


mysql = MySQL(app)

@app.route("/")
def hello_world():
    cur = mysql.connection.cursor()
    cur.execute("insert into user (username, _type, passwd) values ('kaif', 'C', 'sjxli9SQ')")
    mysql.connection.commit()
    cur.close()
    return render_template('homepage.html')

if __name__ == "__main__":
    app.run(debug=True)