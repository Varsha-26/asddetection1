import sqlite3
from flask import Flask, redirect, url_for, render_template, request, session
import pickle
import numpy as np

from asd import model


def register_user_to_db(username, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('INSERT INTO users(username,password) values (?,?)', (username, password))
    con.commit()
    con.close()


def check_user(username, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('Select username,password FROM users WHERE username=? and password=?', (username, password))

    result = cur.fetchone()
    if result:
        return True
    else:
        return False


app = Flask(__name__)
app.secret_key = "r@nd0mSk_1"


@app.route("/")
def index():
    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        register_user_to_db(username, password)
        return redirect(url_for('index'))

    else:
        return render_template('register.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(check_user(username, password))
        if check_user(username, password):
            session['username'] = username

        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))


@app.route('/home', methods=['POST', "GET"])
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return "Username or Password is wrong!"


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/predict', methods=['POST'])
def predict():
    sum = int(request.form.get('1', False))+int(request.form.get('2', False))+int(request.form.get('3', False))+int(request.form.get('4', False))+int(request.form.get('5', False))+int(request.form.get('6', False))+int(request.form.get('7', False))+int(request.form.get('8', False))+int(request.form.get('9', False))+int(request.form.get('10', False))
    age = float(request.form.get('a', False))
    gender = request.form.get('g', False)
    ethnicity = request.form.get('e', False)
    jaundice = request.form.get('j', False)
    autism = request.form.get('au', False)
    relation = request.form.get('r', False)
    arr = np.array([[age, gender, ethnicity, jaundice, autism, sum, 0, relation]])
    pred = model.predict(arr)
    # print(age)
    return render_template('after.html', data=pred)

if __name__ == '__main__':
    app.run(debug=True)