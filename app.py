from flask import *
from flask_mail import Mail, Message
import database as db
from werkzeug.security import generate_password_hash, check_password_hash
import math
from flaskwebgui import FlaskUI

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SESSION_COOKIE_EXPIRES'] = None

app.config['MAIL_SERVER'] = 'smtp.hostinger.com'  # Replace with your mail server
app.config['MAIL_PORT'] = 465  # Port for TLS, use 465 for SSL
app.config['MAIL_USERNAME'] = 'no-reply@binaries.org.in'  # Your email address
app.config['MAIL_PASSWORD'] = 'Raj@1708'  # Your email password
app.config['MAIL_USE_TLS'] = False  # Set to False for SSL
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@binaries.org.in'

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form['email_id']
        password = request.form['password']
        data = {
            "email_id": email
        }
        con, cursor = db.dbconnection()
        if con is None or cursor is None:
            return "Database connection failed", 500

        view_data = db.getUserData(con, cursor, data)
        if view_data:
            stored_password = view_data[3]
            if check_password_hash(stored_password, password):
                session['id'] = view_data[0]
                session['fullname'] = view_data[1]
                session['email'] = view_data[2]
                session['password'] = view_data[3]
                msg = Message('Hello from Flask',
                            recipients=[email])
                msg.body = 'This is a test email sent from a Flask application!'
                msg.html = '<b>This is a test email sent from a Flask application!</b>'
                mail.send(msg)
                return redirect('dashboard')
            else:
                return "Incorrect password", 400
        else:
            return "User not found", 400

    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        hashed_password = generate_password_hash(password)
        
        if password != confirm_password:
            return "Passwords do not match", 400
        
        data = {
            "fullname": fullname,
            "email_id": email,
            "password": hashed_password
        }
        con, cursor = db.dbconnection()
        if con is None or cursor is None:
            return "Database connection failed", 500
        
        if db.register(con, cursor, data):
            return redirect('/')
        else:
            return "Registration failed", 500

    return render_template('register.html')

@app.route('/forgot-password', methods=['GET','POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        data = {
            "email_id":email
        }
        con, cursor = db.dbconnection()
        user_data = db.getUserData(con, cursor, data)
        if user_data:
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if password == confirm_password:
                hashed_password = generate_password_hash(password)
                pass_data = {
                    'email_id':email,
                    'password':hashed_password
                }
                con, cursor = db.dbconnection()
                update_password = db.update_password(con, cursor, pass_data)
                return redirect('/')
            else:
                return "Password Does Not Match", 404
        else:
            return "User Not Found Register First", 404
    return render_template('forgot_password.html')

@app.route('/dashboard/user-update', methods=['POST'])
def user_update():
    if request.method == 'POST':
        user_id = session.get('id')
        fullname = request.form['fullname']
        current_password = request.form['currentPassword']
        check_password = session.get('password')
        new_password = request.form['password']
        confirm_password = request.form['confirmPassword']
        if new_password != '' and confirm_password != '':
            if check_password_hash(check_password, current_password):
                if new_password == confirm_password:
                    secured_password = generate_password_hash(new_password)
                    data = {
                        '_id':user_id,
                        'fullname':fullname,
                        'password':secured_password
                    }
                    session['id'] = user_id
                    session['fullname'] = fullname
                    session['password'] = secured_password
                    con, cursor = db.dbconnection()
                    update_data = db.userUpdate(con, cursor, data)
                    return redirect('/dashboard')
                else:
                    return "Given Password does not match", 500
            else:
                return "Current Password is incorrect", 500
        else:
            data = {
                '_id':user_id,
                'fullname':fullname,
            }
            session['id'] = user_id
            session['fullname'] = fullname
            con, cursor = db.dbconnection()
            update_data = db.userUpdate(con, cursor, data)
            return redirect('/dashboard')
        
    return redirect('/dashboard')

@app.route('/dashboard/project-report/user-update', methods=['POST'])
def user_detail_update():
    if request.method == 'POST':
        user_id = session.get('id')
        fullname = request.form['fullname']
        current_password = request.form['currentPassword']
        check_password = session.get('password')
        new_password = request.form['password']
        confirm_password = request.form['confirmPassword']
        if new_password != '' and confirm_password != '':
            if check_password_hash(check_password, current_password):
                if new_password == confirm_password:
                    secured_password = generate_password_hash(new_password)
                    data = {
                        '_id':user_id,
                        'fullname':fullname,
                        'password':secured_password
                    }
                    session['id'] = user_id
                    session['fullname'] = fullname
                    session['password'] = secured_password
                    con, cursor = db.dbconnection()
                    update_data = db.userUpdate(con, cursor, data)
                    return redirect('/dashboard/project-rreport')
                else:
                    return "Given Password does not match", 500
            else:
                return "Current Password is incorrect", 500
        else:
            data = {
                '_id':user_id,
                'fullname':fullname,
            }
            session['id'] = user_id
            session['fullname'] = fullname
            con, cursor = db.dbconnection()
            update_data = db.userUpdate(con, cursor, data)
            return redirect('/dashboard/project-report')
        
    return redirect('/dashboard/project-report')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if session:
        fullname = session.get('fullname')
        email = session.get('email')
        data = {
            "fullname":fullname,
            "email":email
        }
        con, cursor = db.dbconnection()
        project_data = db.getProjectData(con, cursor)

        con, cursor = db.dbconnection()
        creditAmountReport = db.credit_amount(con, cursor)
        
        con, cursor = db.dbconnection()
        debitAmountReport = db.debit_amount(con, cursor)

        total_credit = sum(int(item[4].replace(',','')) for item in creditAmountReport)
        c_amount = f"{total_credit:,}"
        total_debit = sum(int(item[5].replace(',','')) for item in debitAmountReport)
        d_amount = f"{total_debit:,}"

        current_balance = total_credit - total_debit
        c_balance = f"{current_balance:,}"

        if request.method == 'POST':
            added_by = fullname
            transaction_date = request.form['transaction_date']
            transaction_desc = request.form['transaction_desc']
            project_id = int(request.form['project_title'])
            if 'credit' in request.form:
                credit = int(request.form['credit'])
                cre = f"{credit:,}" if credit is not None else "-"
                data = {
                    "added_by":added_by,
                    "transaction_date":transaction_date,
                    "transaction_desc":transaction_desc,
                    "credit":cre,
                    "debit":"-",
                    "updated_by":"-",
                    "project_id":project_id
                }
            elif 'debit' in request.form:
                debit = int(request.form['debit'])
                deb = f"{debit:,}" if debit is not None else "-"
                data = {
                    "added_by":added_by,
                    "transaction_date":transaction_date,
                    "transaction_desc":transaction_desc,
                    "credit":"-",
                    "debit":deb,
                    "updated_by":"-",
                    "project_id":project_id
                }
            con, cursor = db.dbconnection()
            if con is None or cursor is None:
                return "Database connection failed", 500
            
            if db.transaction(con, cursor, data):
                return redirect('dashboard')
            else:
                return "Data not added due to error", 500
                
        con, cursor = db.dbconnection()
        trn_data = db.getTransactionData(con,cursor)
        if trn_data is None:
            return render_template('dashboard.html', data=data, project_data=project_data)
        else:
            transaction_data = list(trn_data)
            page = request.args.get('page', 1, type=int)
            per_page = 10  # Number of items per page
            total_transactions = len(transaction_data)
            total_pages = math.ceil(total_transactions / per_page)

            start = (page - 1) * per_page
            end = start + per_page
            transactions_to_display = transaction_data[start:end]
            return render_template('dashboard.html',
                                   project_data=project_data,
                                   data=data,
                                   total_transactions=total_transactions,
                                   transaction_data=transactions_to_display,
                                   per_page=per_page,
                                   total_pages=total_pages,
                                   current_page=page,
                                   c_amount=c_amount,
                                   d_amount=d_amount,
                                   c_balance=c_balance
                                )
    else:
        return redirect('/')

    return render_template('dashboard.html')

@app.route('/dashboard/update', methods=['POST'])
def update_transaction():
    user = session.get('fullname')
    transaction_id = request.form['id']
    transaction_date = request.form['update_transaction_date']
    transaction_desc = request.form['update_transaction_desc']
    if 'Credit' in request.form and 'Credit' != '':
        credit = int(request.form['Credit'])
        cre = f"{credit:,}" if credit is not None else "-"
        data = {
            "_id":transaction_id,
            "transaction_date":transaction_date,
            "transaction_desc":transaction_desc,
            "credit":cre,
            "debit":"-",
            "updated_by":user
        }
    elif 'Debit' in request.form and 'Debit' != '':
        debit = int(request.form['Debit'])
        deb = f"{debit:,}" if debit is not None else "-"
        data = {
            "_id":transaction_id,
            "transaction_date":transaction_date,
            "transaction_desc":transaction_desc,
            "credit":"-",
            "debit":deb,
            "updated_by":user
        }
    con, cursor = db.dbconnection()
    update_data = db.updateTransactionData(con, cursor, data)

    return redirect('/dashboard')

@app.route('/dashboard/delete', methods=['GET', 'POST'])
def delete():
    transaction_id = request.form['id']
    _id = int(transaction_id)
    data = {
        "_id":_id
    }
    con, cursor = db.dbconnection()
    delete_data = db.deleteTransactionData(con, cursor, data)
    return redirect('/dashboard')

@app.route('/dashboard/add-project', methods=['GET','POST'])
def add_project():
    if session:
        if request.method == 'POST':
            project_title = request.form['project_title']
            client_name = request.form['client_name']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            project_desc = request.form['project_desc']
            if end_date < start_date:
                flash("End Date cannot earlier than start date.")
            else:
                data = {
                    "project_title":project_title,
                    "client_name":client_name,
                    "start_date":start_date,
                    "end_date":end_date,
                    "project_desc":project_desc
                }

                con, cursor = db.dbconnection()
                project_data = db.projects(con, cursor, data)
    else:
        return redirect('/')
    
    return redirect('/dashboard')

@app.route('/dashboard/project-report')
def project_report():
    if session:
        data = {
            "fullname":session.get('fullname'),
            "email":session.get('email')
        }
        con, cursor = db.dbconnection()
        projectData = db.getProjectData(con, cursor)
        project_data = list(projectData)
        page = request.args.get('page', 1, type=int)
        per_page = 10  # Number of items per page
        total_projects = len(project_data)
        total_pages = math.ceil(total_projects / per_page)

        start = (page - 1) * per_page
        end = start + per_page
        projects_to_display = project_data[start:end]

    return render_template('project_report.html',
                           project_data=projectData,
                           data=data,
                           total_projects=total_projects,
                           transaction_data=projects_to_display,
                           per_page=per_page,
                           total_pages=total_pages,
                           current_page=page)

@app.route('/dashboard/project-report/update', methods=['POST'])
def update_project_data():
    if request.method == 'POST':
            project_id = request.form['id']
            project_title = request.form['project_title']
            client_name = request.form['client_name']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            project_desc = request.form['project_desc']

            data = {
                "_id":project_id,
                "project_title":project_title,
                "client_name":client_name,
                "start_date":start_date,
                "end_date":end_date,
                "project_desc":project_desc
            }

            con, cursor = db.dbconnection()
            project_data = db.updateProjectData(con, cursor, data)

    return redirect('/dashboard/project-report')

@app.route('/dashboard/project-report/delete', methods=['GET', 'POST'])
def delete_project():
    project_id = request.form['id']
    _id = int(project_id)
    data = {
        "_id":_id
    }
    con, cursor = db.dbconnection()
    delete_data = db.deleteProjectData(con, cursor, data)
    return redirect('/dashboard/project-report')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    # app.run(debug=True)
    FlaskUI(app=app, server="flask").run()