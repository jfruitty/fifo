import eel
from user import login_user
from connect import Connect
from models import create_table_users, create_table_products,create_table_location,create_inoder
from location import create_location,in_location, out_location, assign_group_to_location,slog_no_location, create_no_slog
from groupLocation import gropNo
import datetime
from flask import make_response , session
from flask import Flask
import time

#init and setup
eel.init('templates')
create_table_users()
create_table_products()
create_table_location()
create_inoder()
#create_location(row=16, column=33)
#gropNo()
#create_no_slog(slog_no_location())




@eel.expose
def login(email, password):
    user = login_user(email, password)
    if user:
        return {"status": "success", "message": "Login successful", "userid":user[0] }
    else:
        return {"status": "failure", "message": "Login failed"}


@eel.expose
def register_user(username, password):
    try:
        conn, cursor = Connect()
        # Check if the username already exists
        cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        if cursor.fetchone():
            return {'status': False, 'message': 'Username already exists.'}

        # Insert new user if username is not found
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return {'status': True, 'message': 'User registered successfully.'}
    except Exception as e:
        print("Error registering user:", e)
        return {'status': False, 'message': 'Registration failed due to an error.'}
    finally:
        conn.close()

@eel.expose
def get_userid():
    return session.get('userid')


@eel.expose
def fetch_location_data():
    locations = []
    try:
        conn, cursor = Connect()
        cursor.execute("SELECT row, column, isEmpty, groupNo, locationid, productid, created_at FROM Location ORDER BY row, column")
        locations = [dict(row=row, column=column, isEmpty=isEmpty,groupNo=groupNo, locationid=locationid, productid=productid, created_at=created_at) for row, column, isEmpty, groupNo, locationid, productid, created_at in cursor.fetchall()]
    except Exception as e:
        print("Error fetching location data:", e)
    finally:
        if conn:
            conn.close()
    #print(locations)
    return locations



@eel.expose
def fetch_product_data():
    product = []
    try:
        conn, cursor = Connect()
        cursor.execute("""
            SELECT * FROM Products
        """)
        product = [dict(productid=productid, productname=productname, productno=productno,productqty=productqty,productunit=productunit, created_at=created_at) for productid, productname, productno,productqty,productunit, created_at in cursor.fetchall()]
    except Exception as e:
        print("Error fetch_product_data:",e)
    finally:
        if conn:
            conn.close()
    return product

@eel.expose
def add_product(productname, productno, productqty, productunit):
    try:
        conn, cursor = Connect()
        cursor.execute("SELECT productid FROM Products WHERE productno = ?", (productno,))
        if cursor.fetchone():
            return "Product number already exists."

        cursor.execute("""
            INSERT INTO Products (productname, productno, productqty, productunit)
            VALUES (?, ?, ?, ?)
        """, (productname, productno, productqty, productunit))
        conn.commit()
        return "Product added successfully."
    except Exception as e:
        print(f"Error adding product: {e}")
        return f"Failed to add product: {e}"
    finally:
        conn.close()

@eel.expose
def update_product_details(productid, productname, productno, productqty, productunit):
    try:
        conn, cursor = Connect()
        cursor.execute("""
            UPDATE Products
            SET productname = ?, productno = ?, productqty = ?, productunit = ?
            WHERE productid = ?
        """, (productname, productno, productqty, productunit, productid))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating product details: {e}")
        return False
    finally:
        conn.close()


@eel.expose
def addProductToLocations(selectedProductId, selectedLocationId):
    try:
        # ลูปผ่านรายการของตำแหน่งที่เลือก
        for locid in selectedLocationId:
            created_at = datetime.datetime.now()  # บันทึกเวลาปัจจุบัน
            in_location(selectedProductId, locid, created_at)
            time.sleep(0.1)
    except Exception as e:
        print("Error addProductToLocations:", e)
        return False
    finally:
        print("ADDING PRODUCT SUCC")  # แสดงข้อความเมื่อเสร็จสิ้นการทำงาน
    return True


@eel.expose
def pickProductToLocations(selectedLocationIds):
    try:
        for locid in selectedLocationIds:
            out_location(locid)
    except Exception as e:
        print("Error pickProductToLocations", e)
        return False
    finally:
        print("PICK PRODUCT SUCC")
    return True


@eel.expose
def get_oldest_product(count_old, productid):
    # if count_old and productid:
    locations = fetch_location_data()
    product_selet = []
    # กรองเฉพาะสินค้าที่มี `created_at` และไม่ว่าง
    valid_products = [loc for loc in locations if loc['created_at'] and not loc['isEmpty']]
    if not valid_products:
        print("No valid products found.")
        return []

    # เรียงตาม `created_at` จากน้อยไปมาก
    valid_products.sort(key=lambda x: (x['created_at']))
    print(valid_products)
    # กรองเฉพาะสินค้าที่มี `productid` ที่ส่งมา
    product_selet = [prob for prob in valid_products if prob['productid'] == productid]
    print(product_selet)
    return product_selet[:count_old]


@eel.expose
def auto_adding_location_product(productid, count):
    locations = slog_no_location()

    try:
        conn, cursor = Connect()
        cursor.execute("SELECT productid, productno FROM Products WHERE productid = ?", (productid,))
        product = cursor.fetchone()

        if not product:
            raise Exception(f"No product found with ID {productid}")

        product_id, product_no = product

        filtered_locations = [loc for loc in locations if loc['no'] == int(product_no)]
        if count > len(filtered_locations):
            print(f"Warning: Not enough filtered locations available to handle {count}. Proceeding with available.")
            count = len(filtered_locations)

        placed_count = 0

        for loc in filtered_locations:
            if placed_count >= count:
                break

            # Check if the location is empty
            cursor.execute("SELECT isEmpty FROM Location WHERE row = ? AND column = ? AND slogNo = ?",
                           (loc['row'], loc['column'], product_no))
            is_empty = cursor.fetchone()

            if not is_empty or is_empty[0] == 1:
                created_at = datetime.datetime.now()  # ตั้งเวลาปัจจุบัน
                cursor.execute("""
                    UPDATE Location 
                    SET productid = ?, isEmpty = 0, created_at = ?
                    WHERE row = ? AND column = ? AND slogNo = ?
                """, (product_id, created_at, loc['row'], loc['column'], product_no))

                placed_count += 1
                time.sleep(0.01)

        conn.commit()
        return True

    except Exception as e:
        print("Error auto_adding_location_product", e)

    finally:
        conn.close()

@eel.expose
def mark_location_adding(productid, count):
    locations = slog_no_location()  # Ensure this returns correct location data
    try:
        conn, cursor = Connect()  # Establish database connection
        cursor.execute("SELECT productid, productno FROM Products WHERE productid = ?", (productid,))
        product = cursor.fetchone()

        if not product:
            raise Exception(f"No product found with ID {productid}")

        product_id, product_no = product  # Unpack fetched product information

        # กรองเฉพาะตำแหน่งที่ตรงกับสินค้า
        filtered_locations = [loc for loc in locations if loc['no'] == int(product_no)]

        # เช็คว่ามีตำแหน่งเพียงพอหรือไม่
        if count > len(filtered_locations):
            print(f"Warning: Not enough filtered locations available. Proceeding with available.")
            count = len(filtered_locations)

        # เลือก `locationid` ของตำแหน่งที่ผ่านการกรองและส่งให้ JavaScript
        location_ids = []
        placed_count = 0
        for loc in filtered_locations:
            if placed_count >= count:
                break

            # ตรวจสอบว่าตำแหน่งนี้ว่างหรือไม่
            cursor.execute("SELECT locationid, isEmpty FROM Location WHERE row = ? AND column = ? AND slogNo = ?",
                           (loc['row'], loc['column'], product_no))
            locid, is_empty = cursor.fetchone()

            if is_empty:
                location_ids.append(locid)
                placed_count += 1

        return location_ids

    except Exception as e:
        print("Error mark_location_adding:", e)
        return []

    finally:
        conn.close()

@eel.expose
def addProductToInorders(selectedProductId, selectedLocationIds, userid):
    try:
        conn, cursor = Connect()
        # ดึงข้อมูลผลิตภัณฑ์จากฐานข้อมูล
        cursor.execute("SELECT productname FROM Products WHERE productid = ?", (selectedProductId,))
        product_info = cursor.fetchone()
        #เช็คว่าสินค้าที่ส่งมา มีในระบบไหม
        if not product_info:
            raise Exception(f"No product found with ID {selectedProductId}")

        # บันทึกประวัติการเพิ่มสินค้าในตาราง Inorders
        cursor.execute("""
            INSERT INTO Inorders (inout, userid, productid, orderqty)
            VALUES (?, ?, ?, ?)
        """, ("in", userid, selectedProductId, len(selectedLocationIds)))

        conn.commit()
        print("ADDING PRODUCT SUCCESS")
        return True

    except Exception as e:
        print("Error addProductToLocations:", e)
        return False

    finally:
        conn.close()

@eel.expose
def pickProductToInorders(selectedProductId, selectedLocationIds, userid):
    try:
        print(selectedProductId, selectedLocationIds)
        conn, cursor = Connect()
        cursor.execute("SELECT productname FROM Products WHERE productid = ?", (selectedProductId,))
        product_info = cursor.fetchone()

        if not product_info:
            raise Exception(f"No product found with ID {selectedProductId}")

        cursor.execute("""
            INSERT INTO Inorders (inout, userid, productid, orderqty)
            VALUES (?, ?, ?, ?)
        """, ("out", userid, selectedProductId, len(selectedLocationIds)))

        conn.commit()
        print("Order record success!")
        return True

    except Exception as e:
        print("Error recording order:", e)
        return False
    finally:
        conn.close()


@eel.expose
def fetch_order_in_history():
    orders = []
    try:
        conn, cursor = Connect()
        cursor.execute("""
            SELECT o.orderid, o.inout, u.username, p.productname, o.orderqty, o.created_at 
            FROM Inorders o
            LEFT JOIN Users u ON o.userid = u.userid
            LEFT JOIN Products p ON o.productid = p.productid
            WHERE o.inout = 'in'
            ORDER BY o.created_at DESC
        """)
        orders = cursor.fetchall()
    except Exception as e:
        print("Error fetching order history:", e)
    finally:
        conn.close()
    return orders


@eel.expose
def fetch_order_out_history():
    orders = []
    try:
        conn, cursor = Connect()
        cursor.execute("""
            SELECT o.orderid, o.inout, u.username, p.productname, o.orderqty, o.created_at 
            FROM Inorders o
            LEFT JOIN Users u ON o.userid = u.userid
            LEFT JOIN Products p ON o.productid = p.productid
            WHERE o.inout = 'out'
            ORDER BY o.created_at DESC
        """)
        orders = cursor.fetchall()
    except Exception as e:
        print("Error fetching order history:", e)
    finally:
        conn.close()
    return orders





#eel.start('order_in_history.html')
#eel.start('locationStock.html')
eel.start('login.html')
