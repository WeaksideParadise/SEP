from Code_Python.Database import Database
from Code_Python.User     import User
import hashlib

class User_Management:
    def __init__(self, db_connection: Database):
        self.db_connection = db_connection


    # ------------------------------------------------- Database-Funnctions ------------------------------------------------- #
    # -> Gibt einen User anhand seiner ID zurück
    # -> ID ist Primärschlüssel, jeder Nutze hat einzigartige ID
    def get_user_by_id(self, user_id) -> User:

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
    def get_user_by_name(self, name) -> User:

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
    def get_users_by_query(self, query: str, *args) -> list:

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
        
        # -> Neuen Nutzer anlegen, alle nicht aufgezählten Variablen werden automatisch von DB angelegt
        if user.user_id == -1:
            query = """INSERT INTO users (name, hashed_password) 
                       VALUES (%s, %s)"""
            
            try:
                result = self.db_connection.execute_query(query, (user.name, user.hashed_password))
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
    
        user = User(-1, False, name, hashed_password, False, False, "X")
        return self.save_user(user)
    
    # -> Löscht User, in dem bestimmte Attribute auf feste Werte setzt
    # -> User bleibt in Datenbank vorhanden, das dient bestimmten Funktionalitäten
    # -> ID darf nicht geändert werden!
    def delete_user(self, user_id: int) -> bool:
        
        try:
            user = self.get_user_by_id(user_id)
        except LookupError as e:
            return False
        
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
        
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
        except LookupError as e:
            return False
        
        user.is_administrator = False
        user.is_moderator     = False

        return self.save_user(user)

    # ------------------------------------------------- Login_System ------------------------------------------------- #
    # -> prüft, ob Nutzer vorhanden ist
    # -> vergleicht Passwort und setzt Variablen
    def login_user(self, username: str, password: str) -> bool:

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
    
    
