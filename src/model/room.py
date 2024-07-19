from database import connect_to_database, execute_query, fetch_data
from model.reservation import Reservation

class RoomType:
    def __init__(self, room_types_id, name, price, features):
        self.room_types_id = room_types_id
        self.name = name
        self.price = price
        self.features = features

    @staticmethod
    def get_all():
        conn = connect_to_database()
        query = "SELECT * FROM room_types"
        results = fetch_data(conn, query)
        conn.close()
        return [RoomType(**row) for row in results]

    @staticmethod
    def get(room_types_id):
        conn = connect_to_database()
        query = "SELECT * FROM room_types WHERE room_types_id = %s"
        result = fetch_data(conn, query, (room_types_id,))
        conn.close()
        if result:
            return RoomType(**result[0])
        return None

class Room:
    def __init__(self, room_id, room_type_id, room_number, status, location, **kwargs):
        self.room_id = room_id
        self.room_type_id = room_type_id
        self.room_number = room_number
        self.status = status
        self.location = location
        self._room_type = None

    @property
    def room_type(self):
        if self._room_type is None:
            self._room_type = RoomType.get(self.room_type_id)
        return self._room_type

    @property
    def price(self):
        return self.room_type.price if self.room_type else None

    @property
    def features(self):
        return self.room_type.features if self.room_type else None

    @staticmethod
    def create(room_type_id, room_number, status, location):
        conn = connect_to_database()
        query = "INSERT INTO rooms (room_type_id, room_number, status, location) VALUES (%s, %s, %s, %s)"
        values = (room_type_id, room_number, status, location)
        execute_query(conn, query, values)
        conn.close()

    @staticmethod
    def get_available_rooms(check_in_date, check_out_date):
        conn = connect_to_database()
        query = """
        SELECT r.*, rt.name as room_type, rt.price, rt.features 
        FROM rooms r
        JOIN room_types rt ON r.room_type_id = rt.room_types_id
        WHERE r.room_id NOT IN (
            SELECT DISTINCT room_id FROM reservations
            WHERE check_in_date <= %s AND check_out_date >= %s
        )
        """
        values = (check_out_date, check_in_date)
        available_rooms = fetch_data(conn, query, values)
        conn.close()
        return [Room(room_id=room['room_id'], room_type_id=room['room_type_id'], 
                     room_number=room['room_number'], status=room['status'], 
                     location=room['location']) for room in available_rooms]

    @staticmethod
    def get(room_id):
        conn = connect_to_database()
        query = """
        SELECT r.*, rt.name as room_type, rt.price, rt.features 
        FROM rooms r
        JOIN room_types rt ON r.room_type_id = rt.room_types_id
        WHERE r.room_id = %s
        """
        result = fetch_data(conn, query, (room_id,))
        conn.close()
        if result:
            return Room(**result[0])
        return None

    @staticmethod
    def update(room_id, status):
        conn = connect_to_database()
        query = "UPDATE rooms SET status = %s WHERE room_id = %s"
        values = (status, room_id)
        execute_query(conn, query, values)
        conn.close()

    @staticmethod
    def delete(room_id):
        reservations = Reservation.get_reservations_for_room(room_id)
        if reservations:
            for reservation in reservations:
                Reservation.delete(reservation.reservation_id)
        
        conn = connect_to_database()
        query = "DELETE FROM rooms WHERE room_id = %s"
        values = (room_id,)
        execute_query(conn, query, values)
        conn.close()

    @staticmethod
    def get_all():
        conn = connect_to_database()
        query = """
        SELECT r.*, rt.name as room_type, rt.price, rt.features 
        FROM rooms r
        JOIN room_types rt ON r.room_type_id = rt.room_types_id
        """
        results = fetch_data(conn, query)
        conn.close()
        return [Room(room_id=row['room_id'], room_type_id=row['room_type_id'], 
                     room_number=row['room_number'], status=row['status'], 
                     location=row['location']) for row in results]

    @staticmethod
    def search(criteria):
        conn = connect_to_database()
        query = """
        SELECT r.*, rt.name as room_type, rt.price, rt.features 
        FROM rooms r
        JOIN room_types rt ON r.room_type_id = rt.room_types_id
        WHERE rt.name LIKE %s OR r.location LIKE %s OR r.room_number LIKE %s
        """
        search_param = f"%{criteria}%"
        results = fetch_data(conn, query, (search_param, search_param, search_param))
        conn.close()
        return [Room(room_id=row['room_id'], room_type_id=row['room_type_id'], 
                     room_number=row['room_number'], status=row['status'], 
                     location=row['location']) for row in results]
# from database import connect_to_database, execute_query, fetch_data
# from reservations import Reservation

# class RoomType:
#     def __init__(self, room_types_id, name, price, features):
#         self.room_types_id = room_types_id
#         self.name = name
#         self.price = price
#         self.features = features

#     @staticmethod
#     def get_all():
#         conn = connect_to_database()
#         query = "SELECT * FROM room_types"
#         results = fetch_data(conn, query)
#         conn.close()
#         return [RoomType(**row) for row in results]

#     @staticmethod
#     def get(room_types_id):
#         conn = connect_to_database()
#         query = "SELECT * FROM room_types WHERE room_types_id = %s"
#         result = fetch_data(conn, query, (room_types_id,))
#         conn.close()
#         if result:
#             return RoomType(**result[0])
#         return None

# class Room:
#     def __init__(self, room_id, room_type_id, room_number, status, location, is_deleted=False, **kwargs):
#         self.room_id = room_id
#         self.room_type_id = room_type_id
#         self.room_number = room_number
#         self.status = status
#         self.location = location
#         self.is_deleted = is_deleted
#         self._room_type = None

#     @property
#     def room_type(self):
#         if self._room_type is None:
#             self._room_type = RoomType.get(self.room_type_id)
#         return self._room_type

#     @property
#     def price(self):
#         return self.room_type.price if self.room_type else None

#     @property
#     def features(self):
#         return self.room_type.features if self.room_type else None

#     @staticmethod
#     def create(room_type_id, room_number, status, location):
#         conn = connect_to_database()
#         query = "INSERT INTO rooms (room_type_id, room_number, status, location) VALUES (%s, %s, %s, %s)"
#         values = (room_type_id, room_number, status, location)
#         execute_query(conn, query, values)
#         conn.close()

#     @staticmethod
#     def get_available_rooms(check_in_date, check_out_date):
#         conn = connect_to_database()
#         query = """
#         SELECT r.*, rt.name as room_type, rt.price, rt.features 
#         FROM rooms r
#         JOIN room_types rt ON r.room_type_id = rt.room_types_id
#         WHERE r.room_id NOT IN (
#             SELECT DISTINCT room_id FROM reservations
#             WHERE check_in_date <= %s AND check_out_date >= %s
#         ) AND r.is_deleted = FALSE
#         """
#         values = (check_out_date, check_in_date)
#         available_rooms = fetch_data(conn, query, values)
#         conn.close()
#         return [Room(room_id=room['room_id'], room_type_id=room['room_type_id'], 
#                      room_number=room['room_number'], status=room['status'], 
#                      location=room['location'], is_deleted=room['is_deleted']) for room in available_rooms]

#     @staticmethod
#     def get(room_id):
#         conn = connect_to_database()
#         query = """
#         SELECT r.*, rt.name as room_type, rt.price, rt.features 
#         FROM rooms r
#         JOIN room_types rt ON r.room_type_id = rt.room_types_id
#         WHERE r.room_id = %s AND r.is_deleted = FALSE
#         """
#         result = fetch_data(conn, query, (room_id,))
#         conn.close()
#         if result:
#             return Room(**result[0])
#         return None

#     @staticmethod
#     def update(room_id, status):
#         conn = connect_to_database()
#         query = "UPDATE rooms SET status = %s WHERE room_id = %s AND is_deleted = FALSE"
#         values = (status, room_id)
#         execute_query(conn, query, values)
#         conn.close()

#     @staticmethod
#     def delete(room_id):
#         conn = connect_to_database()
#         query = "UPDATE rooms SET is_deleted = TRUE WHERE room_id = %s"
#         values = (room_id,)
#         execute_query(conn, query, values)
#         conn.close()

#     @staticmethod
#     def get_all():
#         conn = connect_to_database()
#         query = """
#         SELECT r.*, rt.name as room_type, rt.price, rt.features 
#         FROM rooms r
#         JOIN room_types rt ON r.room_type_id = rt.room_types_id
#         WHERE r.is_deleted = FALSE
#         """
#         results = fetch_data(conn, query)
#         conn.close()
#         return [Room(room_id=row['room_id'], room_type_id=row['room_type_id'], 
#                      room_number=row['room_number'], status=row['status'], 
#                      location=row['location'], is_deleted=row['is_deleted']) for row in results]

#     @staticmethod
#     def search(criteria):
#         conn = connect_to_database()
#         query = """
#         SELECT r.*, rt.name as room_type, rt.price, rt.features 
#         FROM rooms r
#         JOIN room_types rt ON r.room_type_id = rt.room_types_id
#         WHERE rt.name LIKE %s OR r.location LIKE %s OR r.room_number LIKE %s
#         AND is_deleted = FALSE
#         """
#         search_param = f"%{criteria}%"
#         results = fetch_data(conn, query, (search_param, search_param, search_param))
#         conn.close()
#         return [Room(room_id=row['room_id'], room_type_id=row['room_type_id'], 
#                      room_number=row['room_number'], status=row['status'], 
#                      location=row['location'], is_deleted=row['is_deleted']) for row in results]