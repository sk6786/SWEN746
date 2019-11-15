from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__, template_folder="view")
from controller import register as Register
from model.account_pkg import author_account as author

@app.route('/')
def main():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        auth = author.AuthorAccount()
        if not auth.login(request.form['email'],request.form['password']):
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
        auth = author.AuthorAccount()
        if auth.user_exists(request.form['email']):
            error = 'Choose different username'
        else:
            #capture and send credentials to DB
            register = author.AuthorAccount()
            register.create_account(username=request.form['email'], password=request.form['password'])
            return redirect(url_for('home'))
    return render_template("/auth/register.html",error=error)

@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method =="POST":
        title= request.form['title']
        topic = request.form['topic']
        version = request.form['version']
        fileUpload = request.form['fileUpload']
        authors = request.form['authors']
        return redirect(url_for('home'))
    return render_template("/upload_file.html")

@app.route('/forgot_password')
def forgot_password():
    return render_template("/auth/forgot_password.html")
if __name__ == '__main__':
    app.run()
