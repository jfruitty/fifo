from connect import Connect

def create_table_users():
    try:
        conn, cursor = Connect()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                userid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except Exception as e:
        print("Error creating table Users:", e)
    finally:
        conn.close()

def create_table_products():
    try:
        conn, cursor = Connect()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                productid INTEGER PRIMARY KEY AUTOINCREMENT,
                productname TEXT NOT NULL,
                productno TEXT NOT NULL,
                productqty INTEGER NOT NULL,
                productunit TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
    except Exception as e:
        print("Error creating table Products:", e)
    finally:
        conn.close()

def create_table_location():
    try:
        conn, cursor = Connect()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Location (
                locationid INTEGER PRIMARY KEY AUTOINCREMENT,
                row TEXT DEFAULT NULL,
                column TEXT DEFAULT NULL,
                isEmpty BOOL DEFAULT NULL,
                groupNo TEXT DEFAULT NULL,
                slogNo TEXT DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                productid INTEGER,
                FOREIGN KEY (productid) REFERENCES Products(productid)
            )
        """)
        conn.commit()  # Commit changes to the database
    except Exception as e:
        print("Error creating table Location:", e)
    finally:
        conn.close()


def create_inoder():
    try:
        conn, cursor = Connect()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Inorders (
                orderid INTEGER PRIMARY KEY AUTOINCREMENT,
                inout TEXT NOT NULL,
                userid INTEGER,
                productid INTEGER,
                orderqty INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (productid) REFERENCES Products(productid)
                FOREIGN KEY (userid) REFERENCES Users(userid)
            )
        """)
        conn.commit()  # Commit changes to the database
    except Exception as e:
        print("Error creating table Location:", e)
    finally:
        conn.close()

