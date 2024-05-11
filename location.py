from connect import Connect
import datetime

def create_location(row , column):
    try:
        conn, cursor = Connect()
        cursor.execute("DELETE FROM Location")
        for r in range(1, row +1):
            for c in range(1, column +1):
                cursor.execute("""
                        INSERT INTO Location (row, column, isEmpty)
                        VALUES (?, ?, ?)
                    """, (str(r), str(c), True))
        conn.commit()
        print("Grid initialized successfully.")
    except Exception as e:
        print("Error create stock grid:", e)

def in_location(productid, locationid, created_at):
    try:
        conn, cursor = Connect()
        cursor.execute("SELECT isEmpty FROM Location WHERE locationid = ?", (locationid,))
        result = cursor.fetchone()
        # created_at = datetime.datetime.now()
        if result and result[0] == 1:
            cursor.execute("""
                       UPDATE Location
                       SET isEmpty = ?,
                           productid = ?,
                           created_at = ?
                       WHERE locationid = ?
                   """, (False, productid, created_at, locationid))
            conn.commit()
    except Exception as e:
        print('in_location error', e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def out_location(locationid):
    try:
        conn, cursor = Connect()

        # ตรวจสอบว่าตำแหน่งนั้นไม่ว่างเปล่า
        cursor.execute("SELECT isEmpty FROM Location WHERE locationid = ?", (locationid,))
        result = cursor.fetchone()

        if result and not result[0]:  # เช็คว่า isEmpty เป็น False หรือไม่
            created_at = datetime.datetime.now()  # บันทึกเวลาปัจจุบัน
            cursor.execute("""
                       UPDATE Location
                       SET isEmpty = 1,  
                           productid = NULL,  
                           created_at = ?
                       WHERE locationid = ?
                   """, (created_at, locationid))

            conn.commit()

    except Exception as e:
        print('out_location error', e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def assign_group_to_location(row_start, row_end, col_start, col_end, group_no):
    try:
        conn, cursor = Connect()

        # อัปเดต groupNo สำหรับตำแหน่งที่อยู่ภายในช่วงที่กำหนด
        cursor.execute("""
            UPDATE Location 
            SET groupNo = ? 
            WHERE CAST(row AS INTEGER) BETWEEN ? AND ? 
              AND CAST(column AS INTEGER) BETWEEN ? AND ?
        """, (group_no, row_start, row_end, col_start, col_end))

        conn.commit()
        #print(f"Group {group_no} assigned to locations between rows {row_start}-{row_end} and columns {col_start}-{col_end}.")
    except Exception as e:
        print("Error assigning group to location:", e)
    finally:
        if conn:
            conn.close()


def slog_no_location():
    locations = [
        {'row': 1, 'column': 1, 'no': 1},{'row': 2, 'column': 1, 'no': 1},{'row': 3, 'column': 1, 'no': 1},{'row': 1, 'column': 2, 'no': 1},
        {'row': 2, 'column': 2, 'no': 1},{'row': 3, 'column': 2, 'no': 1},{'row': 1, 'column': 3, 'no': 1},{'row': 2, 'column': 3, 'no': 1},
        {'row': 3, 'column': 3, 'no': 1},{'row': 1, 'column': 4, 'no': 1},{'row': 2, 'column': 4, 'no': 1},{'row': 3, 'column': 4, 'no': 1},
        {'row': 1, 'column': 5, 'no': 1},{'row': 2, 'column': 5, 'no': 1},{'row': 3, 'column': 5, 'no': 1},{'row': 1, 'column': 6, 'no': 1},
        {'row': 2, 'column': 6, 'no': 1},{'row': 3, 'column': 6, 'no': 1},{'row': 1, 'column': 7, 'no': 1},{'row': 2, 'column': 7, 'no': 1},
        {'row': 3, 'column': 7, 'no': 1},{'row': 1, 'column': 8, 'no': 1},{'row': 2, 'column': 8, 'no': 1},{'row': 3, 'column': 8, 'no': 1},
        {'row': 1, 'column': 9, 'no': 1},{'row': 2, 'column': 9, 'no': 1},{'row': 3, 'column': 9, 'no': 1},{'row': 1, 'column': 10, 'no': 1},
        {'row': 2, 'column': 10, 'no': 1},{'row': 3, 'column': 10, 'no': 1},{'row': 1, 'column': 11, 'no': 1},{'row': 2, 'column': 11, 'no': 1},
        {'row': 3, 'column': 11, 'no': 1}, {'row': 1, 'column': 12, 'no': 1},{'row': 2, 'column': 12, 'no': 1},{'row': 3, 'column': 12, 'no': 1},
        {'row': 1, 'column': 13, 'no': 1},{'row': 2, 'column': 13, 'no': 1},{'row': 3, 'column': 13, 'no': 1},{'row': 1, 'column': 14, 'no': 1},
        {'row': 2, 'column': 14, 'no': 1},{'row': 1, 'column': 15, 'no': 1},{'row': 2, 'column': 15, 'no': 1},{'row': 1, 'column': 16, 'no': 1},
        {'row': 2, 'column': 16, 'no': 1},{'row': 1, 'column': 17, 'no': 1},{'row': 2, 'column': 17, 'no': 1},{'row': 1, 'column': 18, 'no': 1},
        {'row': 2, 'column': 18, 'no': 1},{'row': 1, 'column': 19, 'no': 1},{'row': 2, 'column': 19, 'no': 1},{'row': 1, 'column': 20, 'no': 1},
        {'row': 2, 'column': 20, 'no': 1},{'row': 1, 'column': 21, 'no': 1}, {'row': 2, 'column': 21, 'no': 1},{'row': 1, 'column': 22, 'no': 1},
        {'row': 2, 'column': 22, 'no': 1},{'row': 1, 'column': 23, 'no': 1},{'row': 2, 'column': 23, 'no': 1},{'row': 1, 'column': 24, 'no': 1},
        {'row': 2, 'column': 24, 'no': 1},{'row': 1, 'column': 25, 'no': 1},{'row': 2, 'column': 25, 'no': 1},{'row': 1, 'column': 26, 'no': 1},
        {'row': 2, 'column': 26, 'no': 1},{'row': 1, 'column': 27, 'no': 1},{'row': 2, 'column': 27, 'no': 1},{'row': 1, 'column': 28, 'no': 1},
        {'row': 2, 'column': 28, 'no': 1},{'row': 1, 'column': 29, 'no': 1},{'row': 2, 'column': 29, 'no': 1},{'row': 1, 'column': 30, 'no': 1},
        {'row': 2, 'column': 30, 'no': 1},{'row': 1, 'column': 31, 'no': 1},{'row': 2, 'column': 31, 'no': 1},{'row': 1, 'column': 32, 'no': 1},
        {'row': 2, 'column': 32, 'no': 1},{'row': 1, 'column': 33, 'no': 1},{'row': 2, 'column': 33, 'no': 1}, {'row': 3, 'column': 14, 'no': 2},
        {'row': 3, 'column': 15, 'no': 2},{'row': 3, 'column': 16, 'no': 2},{'row': 3, 'column': 17, 'no': 2},{'row': 3, 'column': 18, 'no': 2},
        {'row': 3, 'column': 19, 'no': 2},{'row': 3, 'column': 20, 'no': 2},{'row': 3, 'column': 21, 'no': 2},{'row': 3, 'column': 22, 'no': 2},
        {'row': 3, 'column': 23, 'no': 2},{'row': 3, 'column': 24, 'no': 2}, {'row': 3, 'column': 20, 'no': 2},{'row': 3, 'column': 21, 'no': 2},
        {'row': 3, 'column': 22, 'no': 2},{'row': 3, 'column': 23, 'no': 2},{'row': 3, 'column': 24, 'no': 2}, {'row': 3, 'column': 25, 'no': 2},
        {'row': 3, 'column': 26, 'no': 2},{'row': 3, 'column': 27, 'no': 2},{'row': 3, 'column': 28, 'no': 2},{'row': 3, 'column': 29, 'no': 2},
        {'row': 3, 'column': 30, 'no': 2},{'row': 3, 'column': 31, 'no': 2},{'row': 3, 'column': 32, 'no': 2},{'row': 3, 'column': 33, 'no': 2},

        {'row': 4, 'column': 1, 'no': 2},{'row': 5, 'column': 1, 'no': 2},{'row': 4, 'column': 2, 'no': 2},
        {'row': 5, 'column': 2, 'no': 2},{'row': 4, 'column': 3, 'no': 2},{'row': 5, 'column': 3, 'no': 2},
        {'row': 4, 'column': 4, 'no': 2},{'row': 5, 'column': 4, 'no': 2},{'row': 4, 'column': 5, 'no': 2},
        {'row': 5, 'column': 5, 'no': 2},{'row': 4, 'column': 6, 'no': 2},{'row': 5, 'column': 6, 'no': 2},
        {'row': 4, 'column': 7, 'no': 2},{'row': 5, 'column': 7, 'no': 2}, {'row': 4, 'column': 8, 'no': 2},
        {'row': 5, 'column': 8, 'no': 2},{'row': 4, 'column': 9, 'no': 2},{'row': 4, 'column': 10, 'no': 2},
        {'row': 4, 'column': 11, 'no': 2},{'row': 4, 'column': 12, 'no': 2}, {'row': 4, 'column': 13, 'no': 2},
        {'row': 4, 'column': 14, 'no': 2}, {'row': 4, 'column': 15, 'no': 2},{'row': 4, 'column': 16, 'no': 2},
        {'row': 4, 'column': 17, 'no': 2},{'row': 4, 'column': 18, 'no': 2},{'row': 4, 'column': 19, 'no': 2},
        {'row': 4, 'column': 20, 'no': 2},{'row': 4, 'column': 21, 'no': 2},{'row': 4, 'column': 22, 'no': 2},
        {'row': 4, 'column': 23, 'no': 2},{'row': 4, 'column': 24, 'no': 2},{'row': 4, 'column': 25, 'no': 2},
        {'row': 4, 'column': 26, 'no': 2},{'row': 4, 'column': 27, 'no': 2},{'row': 4, 'column': 28, 'no': 2},
        {'row': 4, 'column': 29, 'no': 2},{'row': 4, 'column': 30, 'no': 2}, {'row': 4, 'column': 31, 'no': 2},
        {'row': 4, 'column': 32, 'no': 2},{'row': 4, 'column': 33, 'no': 2},

        {'row': 5, 'column': 9, 'no': 3},{'row': 5, 'column': 10, 'no': 3},{'row': 5, 'column': 11, 'no': 3},
        {'row': 5, 'column': 12, 'no': 3},{'row': 5, 'column': 13, 'no': 3},{'row': 5, 'column': 14, 'no': 3},
        {'row': 5, 'column': 15, 'no': 3},{'row': 5, 'column': 16, 'no': 3},{'row': 5, 'column': 17, 'no': 3},
        {'row': 5, 'column': 18, 'no': 3},{'row': 5, 'column': 18, 'no': 3},

        {'row': 5, 'column': 19, 'no': 4},{'row': 5, 'column': 20, 'no': 4},{'row': 5, 'column': 21, 'no': 4},
        {'row': 5, 'column': 22, 'no': 4},{'row': 5, 'column': 23, 'no': 4},{'row': 5, 'column': 24, 'no': 4},
        {'row': 5, 'column': 25, 'no': 4},{'row': 5, 'column': 26, 'no': 4},{'row': 5, 'column': 27, 'no': 4},
        {'row': 5, 'column': 28, 'no': 4},

        {'row': 5, 'column': 29, 'no': 5},{'row': 5, 'column': 30, 'no': 5},{'row': 5, 'column': 31, 'no': 5},
        {'row': 5, 'column': 32, 'no': 5},{'row': 5, 'column': 33, 'no': 5},{'row': 5, 'column': 32, 'no': 5},
        {'row': 6, 'column': 1, 'no': 5},{'row': 6, 'column': 2, 'no': 5},{'row': 6, 'column': 3, 'no': 5},
        {'row': 6, 'column': 4, 'no': 5},{'row': 6, 'column': 5, 'no': 5}

    ]

    return locations


def create_no_slog(locations):
    try:
        conn, cursor = Connect()
        if locations:
            for loc in locations:
                # print('row', loc['row'], 'col', loc['column'], 'no', loc['no'])
                try:
                    cursor.execute("""
                        UPDATE Location
                        SET slogNo = ?
                        WHERE row = ? AND column = ?
                    """, (loc['no'], loc['row'], loc['column']))

                except Exception as e:
                    print("Error create_no_slog", e)
        conn.commit()

    except Exception as e:
        print("Error creating or updating locations", e)

    finally:
        conn.close()
