from flask import *
import database as db
from werkzeug.security import generate_password_hash, check_password_hash

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
        print("Credit Amount --------------",creditAmountReport)

        con, cursor = db.dbconnection()
        debitAmountReport = db.debit_amount(con, cursor)
        print("Debit Amount --------------",debitAmountReport)

        total_credit = sum(int(item[4]) for item in creditAmountReport)
        print("credit -----------------",total_credit)
        total_debit = sum(int(item[5]) for item in debitAmountReport)
        print("debit -----------------",total_debit)

        if request.method == 'POST':
                added_by = fullname
                transaction_date = request.form['transaction_date']
                transaction_desc = request.form['transaction_desc']
                credit = request.form.get('credit')
                print("Credit----------------------",credit)
                if credit:
                    data = {
                        "added_by":added_by,
                        "transaction_date":transaction_date,
                        "transaction_desc":transaction_desc,
                        "credit":credit,
                        "debit":"-"
                    }
                debit = request.form.get('debit')
                print("Debit----------------------",debit)
                if debit:
                    data = {
                        "added_by":added_by,
                        "transaction_date":transaction_date,
                        "transaction_desc":transaction_desc,
                        "credit":"-",
                        "debit":debit
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

    return render_template('dashboard.html', data=data, transaction_data=transaction_data, total_credit=total_credit, total_debit=total_debit)

@app.route('/update#<int:id>', methods=['POST'])
def update():
    con, cursor = db.dbconnection()
    if not con or not cursor:
        return jsonify({'success': False, 'message': 'Database connection failed'})

    data = {
        'id': request.form['id'],
        'transaction_date': request.form['transaction_date'],
        'transaction_desc': request.form['transaction_desc'],
        'credit': request.form['credit'],
        'debit': request.form['debit']
    }

    success = db.updateTransactionData(con, cursor, data)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    con, cursor = db.dbconnection()
    delete_data = db.deleteTransactionData(con, cursor, id)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)