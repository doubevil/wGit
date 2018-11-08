from flask import Flask, render_template, request, redirect, url_for

# from wxrid import db_util

app = Flask(__name__)


@app.route('/wxrid/<name>')
def redi(name):
    return render_template('hello.html', name=name)


@app.route('/wxrid/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        print(request.form['username'] + ' ' + request.form['password'])
        if valid_login(request.form['username'],request.form['password']):
            return login_success(request.form['username'])
        else:
            error = 'Invalid username/password'
            return render_template('login_error.html', error=error)


def valid_login(username, password):
    if username == 'admin' and password == 'admin':
        return True


def login_success(username):
    return render_template('login_success.html', username=username)


if __name__ == '__main__':
    app.run()
