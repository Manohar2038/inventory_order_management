import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, host='localhost', database='algorithmic_inventory', user='root', password='Tvk@2026'):
        """Initialize the database connection parameters."""
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        """Establish and return a connection to the database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None

    def close_connection(self):
        """Safely close the connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()

db = DatabaseManager(password='Tvk@2026')
conn = db.connect()
print("Checking the connection...")