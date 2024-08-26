from mysql.connector import *

class Database:
    def __init__(self, user: str, password: str, host: str, database: str):
        self.config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database
        }

    def _connect(self):
        # Stellt eine Verbindung zur Datenbank her.
        try:
            connection = mysql.connector.connect(**self.config)
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
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
