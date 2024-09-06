import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


class Database:
    """
    Eine Klasse zur Verwaltung der Verbindung zu einer MySQL-Datenbank und zum Ausführen von SQL-Abfragen.
    Lädt die Umgebungsvariablen für die Datenbankkonfiguration aus einer .env-Datei.
    """

    def __init__(self):
        """
        Initialisiert die Datenbankkonfiguration durch Laden der Verbindungsdaten aus der .env-Datei und
        stellt die Verbindung zur Datenbank her.
        """
        load_dotenv()
        
        self.config = {
            'host'    : os.getenv('DB_HOST'),
            'database': os.getenv('DB_DATABASE'),
            'user'    : os.getenv('DB_USERNAME'),
            'password': os.getenv('DB_PASSWORD'),
           # 'port'   : 3306  # Optionaler Port kann hier hinzugefügt werden
        }

        self._connect()

    def _connect(self):
        """
        Stellt eine Verbindung zur MySQL-Datenbank her und gibt die Verbindungsinstanz zurück.
        Im Falle eines Verbindungsfehlers wird eine Fehlermeldung ausgegeben.

        :return: Eine Verbindung zur MySQL-Datenbank, wenn erfolgreich, andernfalls None.
        """
        try:
            connection = mysql.connector.connect(**self.config)
            if connection.is_connected():
                return connection
            Error  # Falls der Verbindungsaufbau fehlschlägt
        
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None

    def execute_query(self, query: str, params: tuple = ()) -> list[dict[str, any]]:
        """
        Führt eine SQL-Abfrage aus und gibt die Ergebnisse als Liste von Dictionaries zurück.

        :param query: Die SQL-Abfrage, die ausgeführt werden soll.
        :param params: Ein optionales Tuple mit den Parametern für die SQL-Abfrage.
        :return: Eine Liste von Ergebnissen als Dictionaries, oder None bei einem Verbindungsfehler.
        :raises LookupError: Wenn ein Fehler bei der Abfrageausführung auftritt.
        """
        connection = self._connect()
        if connection is None:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
            
            # Falls eine letzte Zeilen-ID vorhanden ist, wird diese dem Ergebnis hinzugefügt
            if cursor.lastrowid:
                result.append({"last_row_id": cursor.lastrowid})

            connection.commit()  # Änderungen in der Datenbank bestätigen
            return result
        
        except Error as e:
            print(f"Error while executing query in MySQL: {e}")
            raise LookupError
        
        finally:
            # Cursor und Verbindung werden geschlossen, um Ressourcen freizugeben
            cursor.close()
            connection.close()