from flask import *
import database as db
from werkzeug.security import generate_password_hash, check_password_hash
import math

app = Flask(__name__)
app.secret_key = "qwertyuiop@134567890"
app.config['SESSION_COOKIE_EXPIRES'] = None

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
        print(view_data)
        if view_data:
            stored_password = view_data[3]
            if check_password_hash(stored_password, password):
                session['fullname'] = view_data[1]
                session['email'] = view_data[2]
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

@app.route('/dashboard', methods = ['GET','POST'])
def dashboard():
    if session:
        fullname = session.get("fullname")
        data = {
            "fullname":fullname
        }
        con, cursor = db.dbconnection()
        transaction_data = db.getTransactionData(con, cursor)

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
                if 'credit' in request.form:
                    credit = int(request.form['credit'])
                    cre = f"{credit:,}" if credit is not None else "-"
                    data = {
                        "added_by":added_by,
                        "transaction_date":transaction_date,
                        "transaction_desc":transaction_desc,
                        "credit":cre,
                        "debit":"-",
                        "updated_by":"-"
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
                        "updated_by":"-"
                    }
                con, cursor = db.dbconnection()
                if con is None or cursor is None:
                    return "Database connection failed", 500
                
                if db.transaction(con, cursor, data):
                    return redirect('dashboard')
                else:
                    return "Data not added due to error", 500
    else:
        return redirect('/')           

    return render_template('dashboard.html',
                           data=data,
                           transaction_data=transaction_data,
                           c_amount=c_amount,
                           d_amount=d_amount,
                           c_balance=c_balance)

@app.route('/update', methods=['POST'])
def update_transaction():
    user = session.get('fullname')
    print(request.form)
    transaction_id = request.form['id']
    transaction_date = request.form['update_transaction_date']
    transaction_desc = request.form['update_transaction_desc']
    if 'Credit' in request.form:
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
    elif 'Debit' in request.form:
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

    return redirect('dashboard')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    transaction_id = request.form['id']
    _id = int(transaction_id)
    data = {
        "_id":_id
    }
    con, cursor = db.dbconnection()
    delete_data = db.deleteTransactionData(con, cursor, data)
    return redirect('/dashboard')

@app.route('/transactions')
def transactions():
    fullname = session.get('fullname')
    data = {
        "fullname":fullname
    }
    con, cursor = db.dbconnection()
    trn_data = db.getTransactionData(con,cursor)
    transaction_data = list(trn_data)

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

    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of items per page
    total_transactions = len(transaction_data)
    print(total_transactions)
    total_pages = math.ceil(total_transactions / per_page)

    start = (page - 1) * per_page
    end = start + per_page
    transactions_to_display = transaction_data[start:end]

    return render_template(
        'transactions.html',
        total_transactions=total_transactions,
        data=data,
        transaction_data=transactions_to_display,
        per_page=per_page,
        total_pages=total_pages,
        current_page=page,
        c_amount=c_amount,
        d_amount=d_amount,
        c_balance=c_balance
        )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)