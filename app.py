from flask import Flask, render_template, request, redirect, url_for
from controller import register as Register
from model.account_pkg import author_account as author
from flask import jsonify
import pymongo
import urllib.parse
from flask_pymongo import PyMongo
app = Flask(__name__, template_folder="view")
app.config["MONGO_URI"] = "mongodb+srv://" + urllib.parse.quote_plus("USER2") + ":" + urllib.parse.quote_plus(
    "1q2w3e4r") + "@cluster0-tk7v1.mongodb.net/SAM2020?retryWrites=true&w=majority"
mongo = PyMongo(app)


#Remove later
# client = pymongo.MongoClient("mongodb+srv://"+urllib.parse.quote_plus("USER2")+":"+urllib.parse.quote_plus("1q2w3e4r")+"@cluster0-tk7v1.mongodb.net/test?retryWrites=true&w=majority")
# db = client.get_database('SAME2020')

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

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

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
    if request.method == 'POST':
        title= request.form['title']
        topic = request.form['topic']
        version = request.form['version']
        mongo.save_file(title, request.files["fileUpload"])
        #add code to add file to the db
        return redirect(url_for('home'))
    return render_template("/upload_file.html")

@app.route('/forgot_password')
def forgot_password():
    return render_template("/auth/forgot_password.html")

@app.route('/resubmit')
def resubmit():
    return render_template("/resubmit.html", files = [{'id':'1223','title':'saad', 'version': '234', 'paperId':'123'},{'id':'1223','title':'saad', 'version': '234', 'paperid': '3122'}])

@app.route('/resubmitPaper', methods=['GET', 'POST'])
def resubmitPaper():
    paperId = request.args.get('paperId')
    #code to fetch the doc from the artifact list, increment version by 1
    title = 'find from artifacts'
    mongo.save_file(title, request.files["fileUpload"])
    # add code to add file to the db
    return jsonify(status='success')

if __name__ == '__main__':
    app.run()
