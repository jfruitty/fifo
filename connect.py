import sqlite3

def Connect(PATH="inventroy.db"):
    conn = None
    try:
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        #print("Connected ...")
        return conn, cursor
    except sqlite3.Error as e:
        print("Error connecting:", e)
        if conn:
            conn.close()
        return None, None

