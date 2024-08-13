import MySQLdb as db

# db connection
def dbconnection():
    try:
        con = db.connect(host="srv874.hstgr.io", database="u664154894_companytransac", user='u664154894_rajundaviya', password="Raj.Soni@1999")
        cursor = con.cursor()
        return con, cursor
    except db.DatabaseError as e:
        return None, None, f"Database connection failed: {e}"
    
def register(con, cursor, record):
    check_table_query = """
    CREATE TABLE IF NOT EXISTS registrationtb (
        _id INT AUTO_INCREMENT PRIMARY KEY,
        fullname VARCHAR(255) NOT NULL,
        email_id VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS projecttb (
        _id INT AUTO_INCREMENT PRIMARY KEY,
        project_title VARCHAR(255) NOT NULL,
        client_name VARCHAR(255) NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE,
        project_desc VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS transactiontb (
        _id INT AUTO_INCREMENT PRIMARY KEY,
        added_by VARCHAR(255) NOT NULL,
        transaction_date DATE NOT NULL,
        transaction_desc VARCHAR(255) NOT NULL,
        credit VARCHAR(255) NOT NULL,
        debit VARCHAR(255) NOT NULL,
        updated_by VARCHAR(255),
        project_id INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projecttb(_id)
    )
    """
    query = "insert into registrationtb(fullname,email_id,password)values('%s','%s','%s')"
    arg = (record['fullname'],record['email_id'],record['password'])
    try:
        cursor.execute(check_table_query) 
        cursor.execute(query % arg)
        con.commit()
        return True
    except:
        con.rollback()
        return False, 'Insertion problem...'
    finally:
        cursor.close()
        con.close()

def getUserData(con, cursor, data):
    query = "SELECT * FROM registrationtb WHERE email_id=%s"
    arg = (data['email_id'],)
    try:
        cursor.execute(query, arg)
        rec = cursor.fetchone()
        if rec is None:
            return None
        else:
            return rec
    except db.OperationalError as e:
        if e.args[0] == 2006:  # MySQL server has gone away
            # Attempt to reconnect
            con.ping(True)
            cursor = con.cursor()
            con.rollback()
            cursor.execute(query, arg)
            rec = cursor.fetchone()
            return rec
    except db.DatabaseError as e:
        return None, f"Database error: {e}"
    finally:
        cursor.close()
        con.close()

def update_password(con, cursor, data):
    query = 'UPDATE registrationtb SET password=%s WHERE email_id=%s'
    args = (data['password'], data['email_id'])
    try:
        cursor.execute(query, args)
        con.commit()
        return True
    except db.DatabaseError as e:
        con.rollback()
        return False, f"Update problem: {e}"
    finally:
        cursor.close()
        con.close()

def userUpdate(con, cursor, data):
    if 'password' in data:
        query = "UPDATE registrationtb SET fullname=%s, password=%s WHERE _id=%s"
        args = (data['fullname'], data['password'], data['_id'])
        try:
            cursor.execute(query, args)
            con.commit()
            return True
        except db.DatabaseError as e:
            con.rollback()
            return False, f"Update problem: {e}"
        finally:
            cursor.close()
            con.close()
    else:
        query = "UPDATE registrationtb SET fullname=%s WHERE _id=%s"
        args = (data['fullname'], data['_id'])
        try:
            cursor.execute(query, args)
            con.commit()
            return True
        except db.DatabaseError as e:
            con.rollback()
            return False, f"Update problem: {e}"
        finally:
            cursor.close()
            con.close()

def transaction(con, cursor, record):
    query = "insert into transactiontb(added_by,transaction_date,transaction_desc,credit,debit,updated_by,project_id)values('%s','%s','%s','%s','%s','%s','%d')"
    arg = (record['added_by'],record['transaction_date'],record['transaction_desc'],record['credit'],record['debit'],record['updated_by'],record['project_id'])
    try:
        cursor.execute(query % arg)
        con.commit()
        return True
    except:
        con.rollback()
        return False, 'Insertion problem...'
    finally:
        cursor.close()
        con.close()

def getTransactionData(con, cursor):
    query = """
    SELECT * From transactiontb
    JOIN projecttb ON transactiontb.project_id=project_id
    WHERE projecttb._id=project_id
    """
    try:
        cursor.execute(query)
        rec = cursor.fetchall()
        if rec is None or len(rec) == 0:
            return None
        else:
            return rec
    except db.OperationalError as e:
        if e.args[0] == 2006:  # MySQL server has gone away
            con.ping(True)
            cursor = con.cursor()
            con.rollback()
            cursor.execute(query)
            rec = cursor.fetchall()
            return rec
    except db.DatabaseError as e:
        return None, f"Database error: {e}"
    finally:
        cursor.close()
        con.close()

def credit_amount(con,cursor):
    query = "SELECT * FROM transactiontb WHERE credit!='-'"
    try:
        cursor.execute(query)
        rec = cursor.fetchall()
        if rec is None:
            return None
        else:
            return rec
    except db.OperationalError as e:
        if e.args[0] == 2006:  # MySQL server has gone away
            # Attempt to reconnect
            con.ping(True)
            cursor = con.cursor()
            con.rollback()
            cursor.execute(query)
            rec = cursor.fetchone()
            return rec
    except db.DatabaseError as e:
        return None, f"Database error: {e}"
    finally:
        cursor.close()
        con.close()

def debit_amount(con,cursor):
    query = "SELECT * FROM transactiontb WHERE debit!='-'"
    try:
        cursor.execute(query)
        rec = cursor.fetchall()
        if rec is None:
            return None
        else:
            return rec
    except db.OperationalError as e:
        if e.args[0] == 2006:  # MySQL server has gone away
            # Attempt to reconnect
            con.ping(True)
            cursor = con.cursor()
            con.rollback()
            cursor.execute(query)
            rec = cursor.fetchone()
            return rec
    except db.DatabaseError as e:
        return None, f"Database error: {e}"
    finally:
        cursor.close()
        con.close()

# Update transaction data
def updateTransactionData(con, cursor, data):
    query = "UPDATE transactiontb SET transaction_date=%s, transaction_desc=%s, credit=%s, debit=%s, updated_by=%s WHERE _id=%s"
    args = (data['transaction_date'], data['transaction_desc'],data['credit'], data['debit'], data['updated_by'],data['_id'])
    try:
        cursor.execute(query, args)
        con.commit()
        return True
    except db.DatabaseError as e:
        con.rollback()
        return False, f"Update problem: {e}"
    finally:
        cursor.close()
        con.close()

def deleteTransactionData(con, cursor,data):
    query = "DELETE from transactiontb where _id='%d'"
    arg = (data['_id'])
    try:
        cursor.execute(query % arg)
        con.commit()
        return True
    except db.OperationalError as e:
        if e.args[0] == 2006:  # MySQL server has gone away
            # Attempt to reconnect
            con.ping(True)
            cursor = con.cursor()
            con.rollback()
            cursor.execute(query, arg)
            rec = cursor.fetchone()
            return rec
    except db.DatabaseError as e:
        return None, f"Database error: {e}"
    finally:
        cursor.close()
        con.close()

def projects(con, cursor, record):
    query = "insert into projecttb(project_title,client_name,start_date,end_date,project_desc)values('%s','%s','%s','%s','%s')"
    arg = (record['project_title'],record['client_name'],record['start_date'],record['end_date'],record['project_desc'])
    try: 
        cursor.execute(query % arg)
        con.commit()
        return True
    except:
        con.rollback()
        return False, 'Insertion problem...'
    finally:
        cursor.close()
        con.close()

def getProjectData(con, cursor):
    query = "SELECT * FROM projecttb"
    try:
        cursor.execute(query)
        rec = cursor.fetchall()
        if rec is None:
            return None
        else:
            return rec
    except db.OperationalError as e:
        if e.args[0] == 2006:  # MySQL server has gone away
            # Attempt to reconnect
            con.ping(True)
            cursor = con.cursor()
            con.rollback()
            cursor.execute(query)
            rec = cursor.fetchone()
            return rec
    except db.DatabaseError as e:
        return None, f"Database error: {e}"
    finally:
        cursor.close()
        con.close()

def updateProjectData(con, cursor, data):
    query = "UPDATE projecttb SET project_title=%s, client_name=%s, start_date=%s, end_date=%s, project_desc=%s WHERE _id=%s"
    args = (data['project_title'], data['client_name'],data['start_date'], data['end_date'], data['project_desc'],data['_id'])
    try:
        cursor.execute(query, args)
        con.commit()
        return True
    except db.DatabaseError as e:
        con.rollback()
        return False, f"Update problem: {e}"
    finally:
        cursor.close()
        con.close()

def deleteProjectData(con, cursor,data):
    query = "DELETE from projecttb where _id='%d'"
    arg = (data['_id'])
    try:
        cursor.execute(query % arg)
        con.commit()
        return True
    except db.OperationalError as e:
        if e.args[0] == 2006:  # MySQL server has gone away
            # Attempt to reconnect
            con.ping(True)
            cursor = con.cursor()
            con.rollback()
            cursor.execute(query, arg)
            rec = cursor.fetchone()
            return rec
    except db.DatabaseError as e:
        return None, f"Database error: {e}"
    finally:
        cursor.close()
        con.close()