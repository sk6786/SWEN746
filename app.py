from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify
from model.list_pkg.account_list import AccountList
from model.list_pkg.artifact_list import ArtifactList
from model.list_pkg.assignment_list import AssignmentList
from model.list_pkg.template_list import TemplateList
from model.account_pkg.account import Account
from model.account_pkg.author_account import AuthorAccount
from model.account_pkg.pcc_account import PCCAccount
from model.account_pkg.pcm_account import PCMAccount
from model.account_pkg.administrator_account import AdministratorAccount
from controller.artifact_manager import ArtifactManager
from controller.assignment_manager import AssignmentManager
from controller.notification_manager import NotificationManager
from functools import wraps
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
atf_manager = ArtifactManager()
assignment_manager = AssignmentManager()
notification_manager = NotificationManager()

def admin_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_id = int(request.cookies.get('userID'))
        if ACCOUNTS.get_entry(user_id).role == Account.Role.ADMIN:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap


def PCM_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_id = int(request.cookies.get('userID'))
        if ACCOUNTS.get_entry(user_id).role == Account.Role.PCM:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap

def Author_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_id = int(request.cookies.get('userID'))
        if ACCOUNTS.get_entry(user_id).role == Account.Role.AUTHOR:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap

def PCC_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_id = int(request.cookies.get('userID'))
        if ACCOUNTS.get_entry(user_id).role == Account.Role.PCC:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap

def create_account(account_id: int, username: str, password: str, role: str):
    if role == Account.Role.AUTHOR.value:
        return AuthorAccount(account_id, username, password, [])
    elif role == Account.Role.PCM.value:
        return PCMAccount(account_id, username, password, [])
    elif role == Account.Role.PCC.value:
        return PCCAccount(account_id, username, password, [])
    elif role == Account.Role.ADMIN.value:
        return AdministratorAccount(account_id, username, password, [])

@app.route('/')
def main():
    user_id = request.cookies.get('userID')
    if user_id:
        user = COLLECTION.find_one({"accountID": int(user_id)})
        if user:
            if user['role'] == "Admin":
                return redirect(url_for("admin_home"))
            if user['role'] == "PCC":
                return redirect(url_for("PCC_home"))
            if user['role'] == "PCM":
                return redirect(url_for("PCM_home"))
            return render_template('home.html', user=user, notifications = notification_manager.get_all_notifications(int(request.cookies.get('userID'))))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/adminHome', methods=['GET', 'POST'])
@admin_login_required
def admin_home():
    return render_template('admin_home.html',notifications = notification_manager.get_all_notifications(int(request.cookies.get('userID'))))


@app.route('/PCM_home')
@PCM_login_required
def PCM_home():
    return render_template('PCM_home.html', notifications=notification_manager.get_all_notifications(int(request.cookies.get('userID'))))


@app.route('/notification', methods=['GET', 'POST'])
@admin_login_required
def notification():
    if request.method == "POST":
        author = request.form['Author']
        PCC = request.form['PCC']
        PCM = request.form['PCM']
        notification_manager.update_all_deadlines({"Author": author, "PCM": PCM, "PCC": PCC})
        return redirect(url_for('admin_home'))
    notifications = notification_manager.get_all_deadlines()
    return render_template('notification.html', notifications = notifications)


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
@admin_login_required
def add_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        account_id = ACCOUNTS.create_unique_id()
        account = create_account(account_id, username, password, role)
        ACCOUNTS.add_entry(account_id, account)
        return redirect(url_for('manage_accounts'))
    return render_template("add_account.html")


@app.route('/manageAccounts', methods=["GET", "POST"])
@admin_login_required
def manage_accounts():
    if request.method == "POST":
        entry_id = request.form['acc_id']
        return redirect(url_for('edit_account', entry_id = entry_id))
    account_lst = ACCOUNTS.get_list_json()
    return render_template("manage_accounts.html", account_lst = account_lst)


@app.route('/editAccount', methods=["GET", "POST"])
@admin_login_required
def edit_account():
    entry_id = int(request.args.get('entry_id'))
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        new_account = create_account(entry_id, username, password, role)
        ACCOUNTS.update_entry(entry_id, new_account)
        return redirect(url_for('manage_accounts'))
    else:
        entry = ACCOUNTS.get_entry_json(entry_id)
        return render_template("/edit_account.html", entry=entry)


@app.route('/deleteAccount')
@admin_login_required
def delete_account():
    account_id = int(request.args.get('accountId'))
    ACCOUNTS.remove_entry(account_id)
    return jsonify({'code': 'success'})


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if COLLECTION.find_one({'username': request.form['email']}):
            error = 'Choose different username'
        else:
            #capture and send credentials to DB
            account_id = ACCOUNTS.create_unique_id()
            account = create_account(account_id, request.form['email'], request.form['password'], Account.Role.AUTHOR.value)
            ACCOUNTS.add_entry(account_id, account)
            response = redirect(url_for('home'))
            response.set_cookie('userID', str(account_id))
            return response
    return render_template("/auth/register.html",error=error, login=True)

@app.route('/uploadfile', methods=['GET', 'POST'])
@Author_login_required
def upload_file():
    allowed_extensions = {'pdf', 'doc', 'docx'}
    ext_mime_type = {'pdf': 'application/pdf', 'doc': 'application/msword',
                     'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
    if request.method == 'POST':
        author_id = int(request.cookies.get('userID'))
        title = request.form['title']
        topic = request.form['topic']
        fl = request.files['fileUpload']
        authors = request.form['authors']
        version = '0'
        artifact_name = fl.filename
        ext = artifact_name.rsplit('.', 1)[1].lower()
        if ext in allowed_extensions:
            mongo.save_file(title+version, fl, content_type=ext_mime_type[ext])
            paper_id = atf_manager.create_paper(author_id, artifact_name, title, authors, version, topic)
            assignment_manager.create_assignment(paper_id, author_id)
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
@PCM_login_required
def review_page():
    #retrive from DB
    return render_template("/review_page.html")


@app.route('/assign_page')
@PCC_login_required
def assign_page():
    #retrive from DB
    return render_template("/assign_page.html")


@app.route('/rate_paper')
@PCC_login_required
def rate_paper():
    return render_template("/rate_paper.html")

@app.route('/PCC_home')
@PCC_login_required
def PCC_home():
    # retrive from DB
    return render_template("/PCC_home.html", notifications = notification_manager.get_all_notifications(int(request.cookies.get('userID'))))


@app.route('/volunteer')
@PCM_login_required
def volunteer():
    #retrive from DB
    papers = assignment_manager.get_volunteerable_papers()
    return render_template("/volunteer.html", data=papers)


@app.route('/volunteerPaper')
@PCM_login_required
def volunteer_paper():
    paper_id = int(request.args.get("paperID"))
    user_id = int(request.cookies.get('userID'))
    author_id = int(request.args.get("authorID"))
    assignment_manager.volunteer_paper(user_id, paper_id)
    return jsonify({'code':"success"})

@app.route('/resubmit', methods=['GET', 'POST'])
@Author_login_required
def resubmit():
    allowed_extensions = {'pdf', 'doc', 'docx'}
    ext_mime_type = {'pdf': 'application/pdf', 'doc': 'application/msword',
                     'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
    author_id = int(request.cookies.get('userID'))
    if request.method == 'POST':
        paper_id = request.form['paperID']
        title = request.form['title']
        fl = request.files['fileUpload']
        version = request.form['version']
        artifact_name = fl.filename
        ext = artifact_name.rsplit('.', 1)[1].lower()

        if ext in allowed_extensions:
            atf_manager.resubmit_paper(int(paper_id))
            version = str(int(version) + 1)
            mongo.save_file(title+version, fl, content_type=ext_mime_type[ext])
        else:
            error = 'Invalid File Type'
            return render_template("/resubmit.html", error=error)
    return render_template("/resubmit.html", files=atf_manager.get_author_paper(author_id))




if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run()
