from database import connect_to_database, execute_query, fetch_data
from model.reservation import Reservation

class Customer:
    def __init__(self, customer_id, name, contact, address, email):
        self.customer_id = customer_id
        self.name = name
        self.contact = contact
        self.address = address
        self.email = email

    @staticmethod
    def create(name, contact, address, email):
        conn = connect_to_database()
        query = "INSERT INTO customers (name, contact, address, email) VALUES (%s, %s, %s, %s)"
        values = (name, contact, address, email)
        execute_query(conn, query, values)
        conn.close()

    @staticmethod
    def get(customer_id):
        conn = connect_to_database()
        query = "SELECT * FROM customers WHERE customer_id = %s"
        values = (customer_id,)
        customer_data = fetch_data(conn, query, values)
        conn.close()
        if customer_data:
            return Customer(**customer_data[0])
        return None

    @staticmethod
    def update(customer_id, new_name, new_contact, new_address, new_email):
        conn = connect_to_database()
        query = "UPDATE customers SET name = %s, contact = %s, address = %s, email = %s WHERE customer_id = %s"
        values = (new_name, new_contact, new_address, new_email, customer_id)
        execute_query(conn, query, values)
        conn.close()

    @staticmethod
    def delete(customer_id):
        reservations = Reservation.get_reservations_for_customer(customer_id)
        if reservations:
            for reservation in reservations:
                Reservation.delete(reservation.reservation_id)
                
        conn = connect_to_database()
        query = "DELETE FROM customers WHERE customer_id = %s"
        values = (customer_id,)
        execute_query(conn, query, values)
        conn.close()

    @staticmethod
    def get_all():
        conn = connect_to_database()
        query = "SELECT * FROM customers"
        results = fetch_data(conn, query)
        conn.close()
        return [Customer(**row) for row in results]

    @staticmethod
    def search(criteria):
        conn = connect_to_database()
        query = "SELECT * FROM customers WHERE name LIKE %s OR email LIKE %s"
        search_param = f"%{criteria}%"
        results = fetch_data(conn, query, (search_param, search_param))
        conn.close()
        return [Customer(**row) for row in results]