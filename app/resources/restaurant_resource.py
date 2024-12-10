import os
import pymysql
import logging
from app.models.restaurant import Restaurant
from dotenv import load_dotenv
import requests

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RestaurantResource:

    def __init__(self, config):
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME'),
            'port': int(os.getenv('DB_PORT', 3306))
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

    def insert_viewed_restaurants(self, user_id: int, restaurant_code: int):
        query = "INSERT INTO Viewed_Restaurants (user_id, restaurant_code) VALUES (%s, %s)"
        connection = self.get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id, restaurant_code))
                connection.commit()
        except Exception as e:  # Properly handle the exception here
            logger.error(f"Error inserting viewed restaurant: {e}")
            raise
        finally:
            connection.close()

    def remove_viewed_restaurants(self, user_id: int, restaurant_code: int):
        query = "DELETE FROM Viewed_Restaurants WHERE user_id = %s AND restaurant_code = %s"
        connection = self.get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id, restaurant_code))
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

    def get_restaurant_rating(self, restaurant_code: int):
        # Step 1: Fetch place_id from the Restaurant table
        print(f"Fetching place_id for restaurant_code: {restaurant_code}")
        query = "SELECT place_id FROM Restaurant WHERE restaurant_code = %s"
        connection = self.get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (restaurant_code,))
                result = cursor.fetchone()
                if not result:
                    print("No place_id found for the given restaurant_code")
                    return None  # Return None if no place_id found
                place_id = result[0]
                print(f"Found place_id: {place_id}")
        finally:
            print("Closing database connection...")
            connection.close()

        # Step 2: Use the place_id to call the Google Places API
        google_api_key = os.environ.get('GOOGLE_API_KEY')
        google_api_url = f"https://maps.googleapis.com/maps/api/place/details/json"
        full_url = f"{google_api_url}?place_id={place_id}&fields=rating&key={google_api_key}"

        try:
            response = requests.get(full_url)
            response.raise_for_status()  # Raise an error for unsuccessful requests
            data = response.json()
            print(f"Google API response: {data}")  # Debug: Print API response data

            # Check if rating is present in the response
            if "result" in data and "rating" in data["result"]:
                return data["result"]["rating"]
            else:
                print("No rating available for this place_id")
                return None
        except requests.RequestException as e:
            print(f"Error fetching rating from Google Places API: {e}")
            return None