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
            Error
        
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None

    # Ausführen SQL-Query, gibt die Ergebnisse als Liste von Dictionaries zurück.
    def execute_query(self, query: str, params: tuple = ()) -> list[dict[str, any]]:
        
        connection = self._connect()
        if connection is None:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
            connection.commit()
            return result
        
        except Error as e:
            print(f"Error while executing to MySQL: {e}")
            raise LookupError
        
        finally:
            cursor.close()
            connection.close()