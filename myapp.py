# import library
from flask import Flask, render_template, session, request, redirect, url_for 
from flask_mysqldb import MySQL 

# init main app
app = Flask(__name__)

# kunci rahasia agar session bisa berjalan
app.secret_key = '!@#$%'

# konfigurasi database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskmysql'

# init mysql
mysql = MySQL(app)

# route untuk login (default halaman)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form:
        # ambil data dari form
        email = request.form['inpEmail']
        passwd = request.form['inpPass']

        # buat cursor untuk koneksi mysql
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, passwd))
        result = cur.fetchone()

        # cek hasil kueri
        if result:
            session['is_logged_in'] = True
            session['username'] = result[1]
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

# route halaman home
@app.route('/home')
def home():
    # pastikan user sudah login
    if 'is_logged_in' in session and session['is_logged_in']:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        return render_template('home.html', users=data)
    else:
        return redirect(url_for('login'))

# route logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
