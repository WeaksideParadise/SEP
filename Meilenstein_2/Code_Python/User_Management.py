from Code_Python.Database import Database
from Code_Python.User     import User
import hashlib

class User_Management:
    """
    Diese Klasse verwaltet Benutzeroperationen, einschließlich Benutzererstellung, -speicherung, -abfrage und -authentifizierung.
    Sie enthält Methoden zum Hinzufügen, Löschen und Ändern von Benutzern sowie für die Anmeldung und Abmeldung.
    """
    def __init__(self, db_connection: Database):
        """
        Initialisiert die User_Management-Klasse mit einer Datenbankverbindung.

        :param db_connection: Eine Instanz der Database-Klasse zur Interaktion mit der Datenbank.
        :type db_connection: Database
        """
        self.db_connection = db_connection


    # ------------------------------------------------- Database-Funnctions ------------------------------------------------- #
    # -> Gibt einen User anhand seiner ID zurück
    # -> ID ist Primärschlüssel, jeder Nutze hat einzigartige ID
    def get_user_by_id(self, user_id: int) -> User:
        """
        Gibt einen Benutzer anhand seiner ID zurück.

        :param user_id: Die ID des Benutzers.
        :type user_id: int
        :return: Der Benutzer mit der angegebenen ID oder None, wenn kein Benutzer gefunden wurde.
        :rtype: User
        """
        query = """SELECT * FROM users WHERE user_id = %s"""
        
        try:
            result = self.db_connection.execute_query(query, (user_id,))
        except LookupError as e:
            raise LookupError
        
        if result:
            user = User(result[0]["user_id"], 
                        result[0]["is_logged_in"], 
                        result[0]["name"],
                        result[0]["hashed_password"],
                        result[0]["is_administrator"],
                        result[0]["is_moderator"],
                        result[0]["ressource_suggestions"])
            return user
                        
        return None
    
    # -> Gibt einen User anhand seines Namens zurück
    # -> Name ist Sekundärschlüssel (ausgenommen "Deleted"), jeder Nutze hat einzigartigen Namen
    # -> "Deleted" Nutzer darf nicht über diese Funktion aus DB geladen werden
    def get_user_by_name(self, name: int) -> User:
        """
        Gibt einen Benutzer anhand seines Namens zurück.

        :param name: Der Name des Benutzers.
        :type name: str
        :return: Der Benutzer mit dem angegebenen Namen oder None, wenn kein Benutzer gefunden wurde.
        :rtype: User
        :raises ValueError: Wenn der Name "Deleted" ist.
        """
        if name == "Deleted":
            raise ValueError("'Deleted'-Nutzer nicht mit dieser Funktion laden")

        query = """SELECT * FROM users WHERE name = %s"""
        
        try:
            result = self.db_connection.execute_query(query, (name,))
        except LookupError as e:
            raise LookupError
        
        user = None

        if result:
            user = User(result[0]["user_id"], 
                        result[0]["is_logged_in"], 
                        result[0]["name"],
                        result[0]["hashed_password"],
                        result[0]["is_administrator"],
                        result[0]["is_moderator"],
                        result[0]["ressource_suggestions"])
                        
        return user
    
    # -> Query muss gültiger Form entsprechen, Argumente nach Query müssen Reihenfolge in Query entsprechen
    # -> Wird nur von Funktionen gerufen, bei denen Entwickler sicheren Funktionsruf bestimmen
    def get_users_by_query(self, query: str, *args) -> list[User]:
        """
        Gibt eine Liste von Benutzern basierend auf einer benutzerdefinierten SQL-Abfrage zurück.

        :param query: Die SQL-Abfrage zur Auswahl von Benutzern.
        :type query: str
        :param args: Die Argumente für die SQL-Abfrage.
        :return: Eine Liste von Benutzern, die der Abfrage entsprechen.
        :rtype: list[User]
        """
        t = ()
        for element in args:
            t += (element,)

        try: 
            result = self.db_connection.execute_query(query, t)
        except LookupError as e:
            raise LookupError
        
        users = []

        for element in result:
            user = User(element["user_id"], 
                        element["is_logged_in"], 
                        element["name"],
                        element["hashed_password"],
                        element["is_administrator"],
                        element["is_moderator"],
                        element["ressource_suggestions"])
            users.append(user)
        
        return users

    # -> Speichert einen User in der Datenbank
    def save_user(self, user: User) -> bool:
        """
        Speichert einen Benutzer in der Datenbank.

        :param user: Der Benutzer, der gespeichert werden soll.
        :type user: User
        :return: True, wenn der Benutzer erfolgreich gespeichert wurde, andernfalls False.
        :rtype: bool
        """
        # -> Neuen Nutzer anlegen, alle nicht aufgezählten Variablen werden automatisch von DB angelegt
        if user.user_id == -1:
            query = """INSERT INTO users (name, hashed_password, ressource_suggestions) 
                       VALUES (%s, %s, %s)"""
            
            try:
                result = self.db_connection.execute_query(query, (user.name, user.hashed_password, "X"))
            except LookupError as e:
                return False
            
        # -> Bereits vorhandenen Nutzer wieder in DB speichern
        else:
            query = """UPDATE users SET is_logged_in           = %s,
                                        name                   = %s, 
                                        hashed_password        = %s, 
                                        is_administrator       = %s, 
                                        is_moderator           = %s,
                                        ressource_suggestions  = %s 
                                        WHERE user_id          = %s"""
            try:
                result = self.db_connection.execute_query(query, (user.is_logged_in, user.name, user.hashed_password, user.is_administrator, user.is_moderator, user.ressource_suggestions, user.user_id))
            except LookupError as e:
                return False
        
        return True
    
    # ------------------------------------------------- User_Management ------------------------------------------------- #
    # -> Wird von Registrierungsfunktion aufgerufen
    # -> dient der reinen Anlegung eines Nutzer
    # -> NUR über register_user() rufen, NICHT direkt
    def add_user(self, name: str, hashed_password: str) -> bool:
        """
        Fügt einen neuen Benutzer zur Datenbank hinzu.

        :param name: Der Name des neuen Benutzers.
        :type name: str
        :param hashed_password: Das gehashte Passwort des neuen Benutzers.
        :type hashed_password: str
        :return: True, wenn der Benutzer erfolgreich hinzugefügt wurde, andernfalls False.
        :rtype: bool
        """
        user = User(-1, False, name, hashed_password, False, False, "X")
        return self.save_user(user)
    
    # -> Löscht User, in dem bestimmte Attribute auf feste Werte setzt
    # -> User bleibt in Datenbank vorhanden, das dient bestimmten Funktionalitäten
    # -> ID darf nicht geändert werden!
    def delete_user(self, user_id: int) -> bool:
        """
        Löscht einen Benutzer, indem bestimmte Attribute auf feste Werte gesetzt werden.

        :param user_id: Die ID des zu löschenden Benutzers.
        :type user_id: int
        :return: True, wenn der Benutzer erfolgreich gelöscht wurde, andernfalls False.
        :rtype: bool
        :raises ValueError: Wenn der Benutzer Administratorrechte hat.
        """
        try:
            user = self.get_user_by_id(user_id)
        except LookupError as e:
            return False
        
        if user.is_administrator:
            raise ValueError
        
        user.is_logged_in = None
        user.name = "Deleted"
        user.hashed_password = None
        user.is_administrator = False
        user.is_moderator = False
        user.ressource_suggestions = None
           
        return self.save_user(user)
    
    # -> Registrierungsfunktion, wird von UI gerufen
    # -> Prüft, ob Name bereits vorhanden ist
    # -> Prüft, ob Passwort kürzer als 4 Zeichen ist
    # -> Hasht Passwort (MD5)
    def register_user(self, name, suggested_password) -> bool:
        """
        Registriert einen neuen Benutzer, indem Name und Passwort überprüft und in der Datenbank gespeichert werden.

        :param name: Der Name des neuen Benutzers.
        :type name: str
        :param suggested_password: Das Passwort des neuen Benutzers.
        :type suggested_password: str
        :return: True, wenn der Benutzer erfolgreich registriert wurde, andernfalls False.
        :rtype: bool
        :raises NameError: Wenn der Name bereits existiert.
        :raises ValueError: Wenn das Passwort kürzer als 4 Zeichen ist.
        """
        try:
            if self.get_user_by_name(name):
                raise NameError("Benutzername exisitiert bereits")         # Requirement E1/BM.3 erfüllt - keine doppelten Benutzernamen
        except LookupError as e:
            return False
            
        if len(suggested_password) < 4:
            raise ValueError("Password zu kurz")
        
        md5_hash = hashlib.md5()
        md5_hash.update(suggested_password.encode('utf-8'))
        hash_value = md5_hash.hexdigest()
        
        return self.add_user(name, hash_value)
        
    # -> Gibt Nutzer Administratorrechte
    # -> Wird von UI gerufen
    # -> Wer Adminrechte wie vergibt, wird noch geklärt --- TODO
    def promote_user_to_Admin(self, user_id: int) -> bool:
        """
        Vergibt Administratorrechte an einen Benutzer.

        :param user_id: Die ID des Benutzers, der zum Administrator befördert werden soll.
        :type user_id: int
        :return: True, wenn der Benutzer erfolgreich zum Administrator befördert wurde, andernfalls False.
        :rtype: bool
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
        except LookupError as e:
            return False
        
        user.is_administrator = True

        return self.save_user(user)

    # -> Gibt Nutzer Moderatorrechte
    # -> Wird von UI gerufen
    # -> UI prüft, ob der Moderatorrechte erteilende Benutzer Administratorrechte hat  
    def promote_user_to_Moderator(self, user_id: str) -> bool:
        """
        Vergibt Moderatorrechte an einen Benutzer.

        :param user_id: Die ID des Benutzers, der zum Moderator befördert werden soll.
        :type user_id: int
        :return: True, wenn der Benutzer erfolgreich zum Moderator befördert wurde, andernfalls False.
        :rtype: bool
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
        except LookupError as e:
            return False
        
        user.is_moderator = True

        return self.save_user(user)

    # -> Entfernt Nutzer Moderatorrechte UND Administratorrechte
    # -> Wird von UI gerufen
    # -> UI prüft, ob der Rechte entziehende Benutzer Administratorrechte hat 
    def demote_user(self, user_id: str) -> bool:
        """
        Entfernt Moderator- und Administratorrechte von einem Benutzer.

        :param user_id: Die ID des Benutzers, dem die Rechte entzogen werden sollen.
        :type user_id: int
        :return: True, wenn die Rechte erfolgreich entfernt wurden, andernfalls False.
        :rtype: bool
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
        except LookupError as e:
            return False
        
        user.is_moderator     = False

        return self.save_user(user)

    # ------------------------------------------------- Login_System ------------------------------------------------- #
    # -> prüft, ob Nutzer vorhanden ist
    # -> vergleicht Passwort und setzt Variablen
    def login_user(self, username: str, password: str) -> bool:
        """
        Meldet einen Benutzer an, indem das Passwort überprüft und die Anmeldeinformationen aktualisiert werden.

        :param username: Der Name des Benutzers.
        :type username: str
        :param password: Das Passwort des Benutzers.
        :type password: str
        :return: True, wenn der Benutzer erfolgreich angemeldet wurde, andernfalls False.
        :rtype: bool
        :raises LookupError: Wenn der Benutzer nicht gefunden werden kann.
        """
        try:
            user = self.get_user_by_name(username)
            if not user:
                return False
        except LookupError as e:
            raise LookupError
        
        md5_hash = hashlib.md5()
        md5_hash.update(password.encode('utf-8'))

        if md5_hash.hexdigest() == user.hashed_password:
            user.is_logged_in = True

        
        if not self.save_user(user):
            raise LookupError
        
        return user.is_logged_in
    
    # -> loggt Nutzer aus
    def logout_user(self, user_id: int) -> bool:
        """
        Meldet einen Benutzer ab, indem die Anmeldeinformationen aktualisiert werden.

        :param user_id: Die ID des Benutzers, der sich abmelden möchte.
        :type user_id: int
        :return: True, wenn der Benutzer erfolgreich abgemeldet wurde, andernfalls False.
        :rtype: bool
        """  
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
        except LookupError as e:
            return False
        
        user.is_logged_in = False

        if not self.save_user(user):
            return False
        
        return not user.is_logged_in
    
    def sort_users_by_role(self, users: list[User]) -> list[User]:
        """
        Sortiert eine Liste von Benutzern nach ihren Rollen: Administratoren, Moderatoren und normale Benutzer.

        :param users: Die Liste der Benutzer, die sortiert werden sollen.
        :type users: list[User]
        :return: Eine Liste von Benutzern, sortiert nach ihren Rollen.
        :rtype: list[User]
        """
        to_return = []

        #Admins
        for user in users:
            if user.is_administrator:
                to_return.append(user)

        #Mods
        for user in users:
            if not user.is_administrator and user.is_moderator:
                to_return.append(user)  

        #Users
        for user in users:
            if not user.is_administrator and not user.is_moderator:
                to_return.append(user)
    
        return to_return
