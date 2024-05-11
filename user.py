from connect import Connect

def login_user(username, password):
    user = None
    try:
        conn, cursor = Connect()
        cursor.execute("""
            SELECT * FROM Users
            WHERE username=? AND password=?
        """, (username, password))
        user = cursor.fetchone() # จะได้ผลลัพธ์เป็น tuple หรือ None
    except Exception as e:
        print("Error Login", e)
    finally:
        if conn:
            conn.close()
    return user




