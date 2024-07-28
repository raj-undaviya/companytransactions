import MySQLdb as db
# db connection
def dbconnection():
    try:
        con = db.connect(host="localhost", database="companytransactiondb", user='rajundaviya', password="UcldH1tTM[v2dKG6")
        cursor = con.cursor()
        # print("Successfully connectd.........................")
        return con, cursor
    except db.DatabaseError as e:
        print(f"Database connection failed: {e}")
        return None, None
    
def register(con, cursor, record):
    query = "insert into registrationtb(fullname,email_id,password)values('%s','%s','%s')"
    arg = (record['fullname'],record['email_id'],record['password'])
    try: 
        cursor.execute(query % arg)
        con.commit()
        return True
    except:
        con.rollback()
        print('Insertion problem...')
        return False
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
        print(f"Database error: {e}")
        return None
    finally:
        cursor.close()
        con.close()

def transaction(con, cursor, record):
    query = "insert into transactiontb(added_by,transaction_date,transaction_desc,credit,debit)values('%s','%s','%s','%s','%s')"
    arg = (record['added_by'],record['transaction_date'],record['transaction_desc'],record['credit'],record['debit'])
    try: 
        cursor.execute(query % arg)
        con.commit()
        return True
    except:
        con.rollback()
        print('Insertion problem...')
        return False
    finally:
        cursor.close()
        con.close()

def getTransactionData(con, cursor):
    query = "SELECT * FROM transactiontb"
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
        print(f"Database error: {e}")
        return None
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
        print(f"Database error: {e}")
        return None
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
        print(f"Database error: {e}")
        return None
    finally:
        cursor.close()
        con.close()

# Update transaction data
def updateTransactionData(con, cursor, data):
    query = "UPDATE transactiontb SET transaction_date=%s, transaction_desc=%s, credit=%s, debit=%s WHERE id=%s"
    args = (data['transaction_date'], data['transaction_desc'], data['credit'], data['debit'], data['id'])
    try:
        cursor.execute(query, args)
        con.commit()
        return True
    except db.DatabaseError as e:
        con.rollback()
        print(f"Update problem: {e}")
        return False
    finally:
        cursor.close()
        con.close()

def deleteTransactionData(con, cursor,id):
    query = "DELETE from transactiontb where _id='%d'"
    try:
        cursor.execute(query % id)
        con.commit()
        return True
    except db.OperationalError as e:
        if e.args[0] == 2006:  # MySQL server has gone away
            # Attempt to reconnect
            con.ping(True)
            cursor = con.cursor()
            con.rollback()
            cursor.execute(query, id)
            rec = cursor.fetchone()
            return rec
    except db.DatabaseError as e:
        print(f"Database error: {e}")
        return None
    finally:
        cursor.close()
        con.close()
