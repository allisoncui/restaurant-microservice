import pymysql
import logging
from app.models.restaurant import Restaurant

# Configure logging
logging.basicConfig(level=logging.INFO)

class RestaurantResource:

    def __init__(self, config):
        self.db_config = {
            'host': config.get("host", "availability-database.cb821k94flru.us-east-1.rds.amazonaws.com"),
            'user': config.get("user", "root"),
            'password': config.get("password", "dbuserdbuser"),
            'database': config.get("database", "availability"),
            'port': config.get("port", 3306)
        }

    def get_db_connection(self):
        return pymysql.connect(**self.db_config)

    def get_user_id(self, username: str):
        query = "SELECT user_id FROM Profile WHERE username = %s"
        connection = self.get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                return result[0] if result else None
        finally:
            connection.close()

    def get_restaurants(self):
        query = "SELECT restaurant_code, name FROM Restaurant"
        connection = self.get_db_connection()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_viewed_restaurants(self, user_id: int):
        query = """
        SELECT r.restaurant_code, r.name
        FROM Viewed_Restaurants vr
        JOIN Restaurant r ON vr.restaurant_code = r.restaurant_code
        WHERE vr.user_id = %s
        """
        connection = self.get_db_connection()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchall()
        finally:
            connection.close()

    def insert_viewed_restaurants(self, user_id: int, restaurant_codes: list):
        query = "INSERT INTO Viewed_Restaurants (user_id, restaurant_code) VALUES (%s, %s)"
        connection = self.get_db_connection()
        try:
            with connection.cursor() as cursor:
                for code in restaurant_codes:
                    cursor.execute(query, (user_id, code))
                connection.commit()
        finally:
            connection.close()

    def remove_viewed_restaurants(self, user_id: int, restaurant_codes: list):
        query = "DELETE FROM Viewed_Restaurants WHERE user_id = %s AND restaurant_code = %s"
        connection = self.get_db_connection()
        try:
            with connection.cursor() as cursor:
                for code in restaurant_codes:
                    cursor.execute(query, (user_id, code))
                connection.commit()
        finally:
            connection.close()


    def get_by_key(self, restaurant_code: str) -> Restaurant:
        """Retrieve restaurant by the restaurant code key."""
        query = "SELECT * FROM Restaurant WHERE restaurant_code = %s"

        connection = self.get_db_connection()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, (restaurant_code,))
                result = cursor.fetchone()
                if result:
                    return Restaurant(**result)  # Return a Restaurant model
                else:
                    return None
        finally:
            connection.close()

    