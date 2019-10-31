from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


@app.route('/')
def main():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['email'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid username or password'
        else:
            return redirect(url_for('home'))
    return render_template('auth/login.html', error=error)

@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['name'] == '' or request.form['password'] == '' or request.form['email'] == '':
            error = 'Input cannot be empty'
        else:
            #capture and send credentials to DB
            return redirect(url_for('home'))
    return render_template("/auth/register.html",error=error)
@app.route('/forgot_password')
def forgot_password():
    return render_template("/auth/forgot_password.html")
if __name__ == '__main__':
    app.run()
