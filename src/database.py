import mysql.connector

def connect_to_database():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "hotel_reservation_system"
    }
    return mysql.connector.connect(**db_config)


def execute_query(conn, query, values=None):
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    cursor.close()


def fetch_data(conn, query, values=None):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, values)
    data = cursor.fetchall()
    cursor.close()
    return data

