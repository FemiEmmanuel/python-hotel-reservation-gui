from database import connect_to_database, execute_query, fetch_data

class Service:
    def __init__(self, service_id, name, description, price):
        self.service_id = service_id
        self.name = name
        self.description = description
        self.price = price

    @staticmethod
    def create(name, description, price):
        conn = connect_to_database()
        query = "INSERT INTO services (name, description, price) VALUES (%s, %s, %s)"
        values = (name, description, price)
        execute_query(conn, query, values)
        conn.close()

    @staticmethod
    def get(service_id):
        conn = connect_to_database()
        query = "SELECT * FROM services WHERE service_id = %s"
        result = fetch_data(conn, query, (service_id,))
        conn.close()
        if result:
            return Service(**result[0])
        return None

    @staticmethod
    def get_name_to_id_map():
        conn = connect_to_database()
        query = "SELECT service_id, name FROM services"
        results = fetch_data(conn, query)
        conn.close()
        return {row['name']: row['service_id'] for row in results}


    @staticmethod
    def update(service_id, name, description, price):
        conn = connect_to_database()
        query = """UPDATE services SET name = %s, description = %s, 
                   price = %s WHERE service_id = %s"""
        values = (name, description, price, service_id)
        execute_query(conn, query, values)
        conn.close()

    @staticmethod
    def delete(service_id):
        conn = connect_to_database()
        query = "DELETE FROM services WHERE service_id = %s"
        execute_query(conn, query, (service_id,))
        conn.close()

    #Returns a list containing all services
    @staticmethod
    def get_all():
        conn = connect_to_database()
        query = "SELECT * FROM services"
        results = fetch_data(conn, query)
        conn.close()
        return [Service(**row) for row in results]

    @staticmethod
    def search(criteria):
        conn = connect_to_database()
        query = "SELECT * FROM services WHERE name LIKE %s OR description LIKE %s"
        search_param = f"%{criteria}%"
        results = fetch_data(conn, query, (search_param, search_param))
        conn.close()
        return [Service(**row) for row in results]