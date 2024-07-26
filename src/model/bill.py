from database import connect_to_database, execute_query, fetch_data
from model.service import Service

class Bill:
    def __init__(self, bill_id, reservation_id, amount, date, services=None):
        self.bill_id = bill_id
        self.reservation_id = reservation_id
        self.amount = amount
        self.date = date
        self.services = services or []

    # Add a bill
    @staticmethod
    def create(reservation_id, amount, date, services):
        conn = connect_to_database()
        query = """INSERT INTO bills (reservation_id, amount, date) 
                   VALUES (%s, %s, %s)"""
        values = (reservation_id, amount, date)
        execute_query(conn, query, values)

        bill_id = fetch_data(conn, "SELECT LAST_INSERT_ID()")[0]['LAST_INSERT_ID()']

        for service_id in services:
            query = "INSERT INTO billservice (bill_id, service_id) VALUES (%s, %s)"
            execute_query(conn, query, (bill_id, service_id))

        conn.close()

    # Retrieve a bill by id
    @staticmethod
    def get(bill_id):
        conn = connect_to_database()
        query = "SELECT * FROM bills WHERE bill_id = %s"
        result = fetch_data(conn, query, (bill_id,))
        if result:
            bill = Bill(**result[0])
            query = """SELECT s.* FROM services s
                       JOIN billservice bs ON s.service_id = bs.service_id
                       WHERE bs.bill_id = %s"""
            services = fetch_data(conn, query, (bill_id,))
            bill.services = services
            conn.close()
            return bill
        conn.close()
        return None
    

    # Retrieves all details of a bill. 
    @staticmethod
    def get_bill_details(bill_id):
        conn = connect_to_database()
        query = """
        SELECT b.*, r.check_in_date, r.check_out_date, c.name as customer_name, c.customer_id
        FROM bills b
        JOIN reservations r ON b.reservation_id = r.reservation_id
        JOIN customers c ON r.customer_id = c.customer_id
        WHERE b.bill_id = %s
        """
        result = fetch_data(conn, query, (bill_id,))
        
        if not result:
            conn.close()
            return None

        bill_details = result[0]
        
        query = """
        SELECT s.*
        FROM services s
        JOIN billservice bs ON s.service_id = bs.service_id
        WHERE bs.bill_id = %s
        """
        services = fetch_data(conn, query, (bill_id,))
        
        bill_details['services'] = services
        
        conn.close()
        return bill_details

    # Retrieves all bills with all details
    @staticmethod
    def get_all_bill_details():
        conn = connect_to_database()
        query = """
        SELECT b.*, r.check_in_date, r.check_out_date, c.name as customer_name, c.customer_id
        FROM bills b
        JOIN reservations r ON b.reservation_id = r.reservation_id
        JOIN customers c ON r.customer_id = c.customer_id
        """
        results = fetch_data(conn, query)
        
        bills = []
        for bill in results:
            query = """
            SELECT s.*
            FROM services s
            JOIN billservice bs ON s.service_id = bs.service_id
            WHERE bs.bill_id = %s
            """
            services = fetch_data(conn, query, (bill['bill_id'],))
            bill['services'] = services
            bills.append(bill)
        
        conn.close()
        return bills

    #Updates a bill
    @staticmethod
    def update(bill_id, reservation_id, amount, date, services):
        conn = connect_to_database()
        query = """UPDATE bills SET reservation_id = %s, amount = %s, 
                   date = %s WHERE bill_id = %s"""
        values = (reservation_id, amount, date, bill_id)
        execute_query(conn, query, values)

        execute_query(conn, "DELETE FROM billservice WHERE bill_id = %s", (bill_id,))
        for service_id in services:
            query = "INSERT INTO billservice (bill_id, service_id) VALUES (%s, %s)"
            execute_query(conn, query, (bill_id, service_id))

        conn.close()

    # Delete a bill
    @staticmethod
    def delete(bill_id):
        conn = connect_to_database()
        execute_query(conn, "DELETE FROM billservice WHERE bill_id = %s", (bill_id,))
        execute_query(conn, "DELETE FROM bills WHERE bill_id = %s", (bill_id,))
        conn.close()

    # Retrieves all bills
    @staticmethod
    def get_all():
        conn = connect_to_database()
        query = "SELECT * FROM bills"
        results = fetch_data(conn, query)
        bills = []
        for row in results:
            bill = Bill(**row)
            query = """SELECT s.* FROM services s
                       JOIN billservice bs ON s.service_id = bs.service_id
                       WHERE bs.bill_id = %s"""
            services = fetch_data(conn, query, (bill.bill_id,))
            bill.services = services
            bills.append(bill)
        conn.close()
        return bills
    
    # Retrieve a bill by reservation id
    @staticmethod
    def get_by_reservation(reservation_id):
        conn = connect_to_database()
        query = "SELECT * FROM bills WHERE reservation_id = %s"
        result = fetch_data(conn, query, (reservation_id,))
        conn.close()
        if result:
            return Bill(**result[0])
        return None
    
    # Retrieves all services associated with a bill
    @staticmethod
    def get_services_for_bill(bill_id):
        conn = connect_to_database()
        query = """SELECT s.* FROM services s
                   JOIN billservice bs ON s.service_id = bs.service_id
                   WHERE bs.bill_id = %s"""
        results = fetch_data(conn, query, (bill_id,))
        conn.close()

        services = [Service(**result) for result in results]
        return services
    
    # Search for a bill and all its details
    @staticmethod
    def search(criteria):
        conn = connect_to_database()
        query = """SELECT b.* FROM bills b
                   JOIN reservations r ON b.reservation_id = r.reservation_id
                   JOIN customers c ON r.customer_id = c.customer_id
                   WHERE c.name LIKE %s OR b.date LIKE %s"""
        search_param = f"%{criteria}%"
        results = fetch_data(conn, query, (search_param, search_param))
        bills = []
        for row in results:
            bill = Bill(**row)
            query = """SELECT s.* FROM services s
                       JOIN billservice bs ON s.service_id = bs.service_id
                       WHERE bs.bill_id = %s"""
            services = fetch_data(conn, query, (bill.bill_id,))
            bill.services = services
            bills.append(bill)
        conn.close()
        return bills