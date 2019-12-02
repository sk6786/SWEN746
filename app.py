from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify
from model.list_pkg.account_list import AccountList
from model.list_pkg.artifact_list import ArtifactList
from model.list_pkg.assignment_list import AssignmentList
from model.list_pkg.template_list import TemplateList
import urllib.parse
from flask_pymongo import PyMongo
app = Flask(__name__, template_folder="view")
app.config["MONGO_URI"] = "mongodb+srv://" + urllib.parse.quote_plus("USER2") + ":" + urllib.parse.quote_plus(
    "1q2w3e4r") + "@cluster0-tk7v1.mongodb.net/SAM2020?retryWrites=true&w=majority"
mongo = PyMongo(app)
ARTIFACT_COLLECTION = mongo.db['Artifacts']
COLLECTION = mongo.db['Accounts']

ARTIFACTS = ArtifactList()
ACCOUNTS = AccountList()
ASSIGNMENTS = AssignmentList()
TEMPLATES = TemplateList()

@app.route('/')
def main():
    user_id = request.cookies.get('userID')
    if user_id:
        user = COLLECTION.find_one({"accountID": int(user_id)})
        if user:
            if user['role'] == "Admin":
                return redirect(url_for("admin_home"))
            return render_template('home.html', user=user)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/adminHome', methods=['GET', 'POST'])
def admin_home():
    return render_template('admin_home.html')


@app.route('/notification', methods=['GET', 'POST'])
def notification():
    return render_template('notification.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if not COLLECTION.find_one({'username': request.form['email'], 'password': request.form['password']}):
            error = 'Invalid username or password'
        else:
            user = COLLECTION.find_one({'username': request.form['email'], 'password': request.form['password']})
            response = redirect(url_for('home'))
            response.set_cookie('userID', str(user['accountID']))
            return response
    return render_template('auth/login.html', error=error, login=True)


@app.route('/logout')
def logout():
    user = COLLECTION.find_one({'accountID':int(request.cookies.get('userID'))})
    resp = redirect(url_for('login'))
    resp.set_cookie('userID', str(user['accountID']), expires=0)
    return resp


@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


@app.route('/home')
def home():
    return redirect(url_for("main"))


@app.route('/addAccount',methods=['GET', 'POST'] )
def add_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        entry = ACCOUNTS.create_entry_object({'username': username, 'password': password, 'role': role})
        ACCOUNTS.add_entry(entry.account_id, entry)
        return redirect(url_for('manage_accounts'))
    return render_template("add_account.html")


@app.route('/manageAccounts', methods=["GET", "POST"])
def manage_accounts():
    if request.method == "POST":
        entry_id = request.form['acc_id']
        return redirect(url_for('edit_account', entry_id = entry_id))
    ACCOUNTS.populate_list()
    account_lst = ACCOUNTS.get_list_json()
    return render_template("manage_accounts.html", account_lst = account_lst)


@app.route('/editAccount', methods=["GET", "POST"])
def edit_account():
    entry_id = int(request.args.get('entry_id'))
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        entry = ACCOUNTS.create_entry_object({'username': username, 'accountID': entry_id, 'password': password, 'role': role})
        ACCOUNTS.update_entry(entry_id, entry)
        return redirect(url_for('manage_accounts'))
    else:
        entry = ACCOUNTS.get_entry_json(entry_id)
        return render_template("/edit_account.html", entry=entry)

@app.route('/deleteAccount')
def delete_account():
    account_id = int(request.args.get('accountId'))
    col = mongo.db['Accounts']
    accounts = account_list.AccountList(col)
    accounts.remove_entry(account_id)
    return jsonify({'code': 'success'})


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if COLLECTION.find_one({'username': request.form['email']}):
            error = 'Choose different username'
        else:
            #capture and send credentials to DB
            entry = ACCOUNTS.create_entry_object({'username': request.form['email'], 'password': request.form['password'], 'role': 'Author'})
            ACCOUNTS.add_entry(entry.account_id, entry)
            return redirect(url_for('home'))
    return render_template("/auth/register.html",error=error, login=True)


@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    allowed_extensions = {'pdf', 'doc', 'docx'}
    ext_mime_type = {'pdf': 'application/pdf', 'doc': 'application/msword',
                     'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
    if request.method == 'POST':
        title= request.form['title']
        topic = request.form['topic']
        version = request.form['version']
        fl = request.files['fileUpload']
        ext = fl.filename.rsplit('.', 1)[1].lower()
        if ext in allowed_extensions:
            mongo.save_file(title, fl, content_type=ext_mime_type[ext])
        else:
            error = 'Invalid File Type'
            return render_template("/upload_file.html", error=error)

        # add code to add file to the db
        return redirect(url_for('home'))
    return render_template("/upload_file.html")


@app.route('/forgot_password')
def forgot_password():
    return render_template("/auth/forgot_password.html")

@app.route('/review_page')
def review_page():
    #retrive from DB
    return render_template("/review_page.html")


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
