from database import connect_to_database, execute_query, fetch_data
from model.bill import Bill

class Reservation:
    def __init__(self, reservation_id, customer_id, room_id, check_in_date, check_out_date, total_cost):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.room_id = room_id
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.total_cost = total_cost

    @staticmethod
    def create(customer_id, room_id, check_in_date, check_out_date, total_cost):
        conn = connect_to_database()
        query = """INSERT INTO reservations (customer_id, room_id, check_in_date, check_out_date, total_cost)
                    VALUES (%s, %s, %s, %s, %s)"""
        values = (customer_id, room_id, check_in_date, check_out_date, total_cost)
        execute_query(conn, query, values)
        conn.close()

    @staticmethod
    def get_reservation_details(reservation_id):
        conn = connect_to_database()
        query = """
        SELECT r.*, c.name as customer_name, rm.room_number, rt.name as room_type
        FROM reservations r
        JOIN customers c ON r.customer_id = c.customer_id
        JOIN rooms rm ON r.room_id = rm.room_id
        JOIN room_types rt ON rm.room_type_id = rt.room_type_id
        WHERE r.reservation_id = %s
        """
        result = fetch_data(conn, query, (reservation_id,))
        conn.close()
        if result:
            return result[0]
        return None

    @staticmethod
    def get(reservation_id):
        conn = connect_to_database()
        query = "SELECT * FROM reservations WHERE reservation_id = %s"
        result = fetch_data(conn, query, (reservation_id,))
        conn.close()
        if result:
            return Reservation(**result[0])
        return None
     
    @staticmethod
    def update(reservation_id, customer_id, room_id, check_in_date, check_out_date, total_cost):
        conn = connect_to_database()
        query = """UPDATE reservations SET customer_id = %s, room_id = %s, check_in_date = %s,
                    check_out_date = %s, total_cost = %s WHERE reservation_id = %s"""
        values = (customer_id, room_id, check_in_date, check_out_date, total_cost, reservation_id)
        execute_query(conn, query, values)
        conn.close()

    @staticmethod
    def delete(reservation_id):
        bill = Bill.get_by_reservation(reservation_id)
        if bill:
            Bill.delete(bill.bill_id)

        conn = connect_to_database()
        query = "DELETE FROM reservations WHERE reservation_id = %s"
        execute_query(conn, query, (reservation_id,))
        conn.close()

    @staticmethod
    def get_reservations_for_room(room_id):
        conn = connect_to_database()
        query = "SELECT * FROM reservations WHERE room_id = %s"
        results = fetch_data(conn, query, (room_id,))
        conn.close()

        reservations = [Reservation(**result) for result in results]
        return reservations
    
    @staticmethod
    def get_reservations_for_customer(customer_id):
        conn = connect_to_database()
        query = "SELECT * FROM reservations WHERE customer_id = %s"
        results = fetch_data(conn, query, (customer_id,))
        conn.close()

        reservations = [Reservation(**result) for result in results]
        return reservations
    
    @staticmethod
    def get_all_reservation_details():
        conn = connect_to_database()
        query = """
        SELECT r.*, c.name as customer_name, rm.room_number, rt.name as room_type
        FROM reservations r
        JOIN customers c ON r.customer_id = c.customer_id
        JOIN rooms rm ON r.room_id = rm.room_id
        JOIN room_types rt ON rm.room_type_id = rt.room_type_id
        """
        results = fetch_data(conn, query)
        conn.close()
        return results
    
    @staticmethod
    def check_overlapping_reservations(room_id, check_in_date, check_out_date, exclude_reservation_id=None):
        conn = connect_to_database()
        query = """
        SELECT * FROM reservations 
        WHERE room_id = %s 
        AND ((check_in_date <= %s AND check_out_date >= %s)
        OR (check_in_date <= %s AND check_out_date >= %s)
        OR (check_in_date >= %s AND check_out_date <= %s))
        """
        params = [room_id, check_in_date, check_in_date, check_out_date, check_out_date, check_in_date, check_out_date]
        
        if exclude_reservation_id:
            query += " AND reservation_id != %s"
            params.append(exclude_reservation_id)
        
        results = fetch_data(conn, query, tuple(params))
        conn.close()
        return results

    @staticmethod
    def search(criteria):
        conn = connect_to_database()
        query = """
        SELECT r.*, c.name as customer_name, rm.room_number, rt.name as room_type
        FROM reservations r
        JOIN customers c ON r.customer_id = c.customer_id
        JOIN rooms rm ON r.room_id = rm.room_id
        JOIN room_types rt ON rm.room_type_id = rt.room_type_id
        WHERE c.name LIKE %s 
        OR r.check_in_date LIKE %s
        OR r.check_out_date LIKE %s
        OR rm.room_number LIKE %s
        """
        search_param = f"%{criteria}%"
        results = fetch_data(conn, query, (search_param, search_param, search_param, search_param))
        conn.close()
        return results

