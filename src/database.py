import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'hotel_reservation_system'
}

def connect_to_database():
    return mysql.connector.connect(**db_config)

def create_database_if_not_exists(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

def create_tables(cursor):

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    contact VARCHAR(20),
    address TEXT,
    email VARCHAR(100)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS room_types (
    room_types_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    price DECIMAL(10, 2) NOT NULL,
    features TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    status ENUM('Available', 'Occupied', 'Maintenance') NOT NULL,
    location ENUM('North Wing', 'South Wing', 'East Wing', 'West Wing', 'Penthouse') NOT NULL,
    room_type_id INT NOT NULL,
    room_number VARCHAR(10) NOT NULL UNIQUE,
    FOREIGN KEY (room_type_id) REFERENCES room_types(room_types_id) ON DELETE CASCADE
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    room_id INT,
    check_in_date DATE,
    check_out_date DATE,
    total_cost DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE CASCADE
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    description TEXT,
    price DECIMAL(10, 2)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bills (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT,
    amount DECIMAL(10, 2),
    date DATE,
    services TEXT,
    FOREIGN KEY (reservation_id) REFERENCES reservations(reservation_id) ON DELETE CASCADE
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS billservice (
    billservice_id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT,
    service_id INT,
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE CASCADE
    )""")

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

def initialize_database():
    
    conn = connect_to_database()
    
    cursor = conn.cursor()
    create_database_if_not_exists(cursor, db_config['database'])
    cursor.execute(f"USE {db_config['database']}")
    create_tables(cursor)
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    initialize_database()