import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


class Database:
    def __init__(self):
        load_dotenv()
        self.config = {
            'host'    : os.getenv('DB_HOST'),
            'database': os.getenv('DB_DATABASE'),
            'user'    : os.getenv('DB_USERNAME'),
            'password': os.getenv('DB_PASSWORD'),
           #'port'    : 3306
        }

    # Verbindungsaufbau mit Datenbank
    def _connect(self):
        try:
            connection = mysql.connector.connect(**self.config)
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None

    # Ausführen SQL-Query
    def execute_query(self, query: str, params: tuple = ()) -> list[dict[str, any]]:
        """Führt eine SQL-Abfrage aus und gibt die Ergebnisse als Liste von Dictionaries zurück."""
        connection = self._connect()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
