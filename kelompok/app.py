from flask import Flask, render_template, json, session,request,redirect,url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

# init main app
app = Flask(__name__)
# datebase config
app.secret_key= '!@#$%'
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_user'

# init mysql
mysql = MySQL(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
# function login
def login():
    # cek jika method POST dan ada pada form data maka proses login
    if request.method == 'POST' and 'InpEmail' in request.form and 'InpPass' in request.form:
        # buat variabel untuk memudahkan pengolahan data
        email = request.form['InpEmail']
        passwd = request.form['InpPass']
        # cursor koneksi mysql
        cur = mysql.connection.cursor()
        # eksekusi queri
        cur.execute("SELECT * FROM user where email = %s and password = %s", (email, passwd))
        # fetch hasil queri
        result = cur.fetchall()
        # cek hasil kueri
        if result:
            # jika login valid
            session['is_logged_in'] = True
            session['username'] = result[0]
            # redirect home
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/signup', methods =['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (username,email, password))
        mysql.connection.commit()
        msg = 'You have successfully registered !'
        return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg = msg)
        
# route home dan logout
@app.route('/home')
# function home
def home():
    # cek session
    if 'is_logged_in' in session:
        return render_template('home.html')
    
# route logout
@app.route('/logout')
def logout():
    # hapus data
    session.pop('is_logged_in', None)
    session.pop('username', None)
    # redirect to login page
    return redirect(url_for('login'))
# debug
if __name__ == '__main__':
    app.run(debug=True)