import Database
import User
import hashlib

class User_Management:
    def __init__(self, db_connection: Database):
        self.db_connection = db_connection


    # ------------------------------------------------- Database based functions ------------------------------------------------- #
    def get_user_by_id(self, user_id) -> User:

        query = """SELECT * FROM users WHERE user_id = %s"""
        
        try:
            result = self.db_connection.execute_query(query, user_id)
        except LookupError as e:
            raise LookupError
        
        if result:
            user = User(result[0]["user_id"], 
                        result[0]["is_logged_in"], 
                        result[0]["name"],
                        result[0]["hashed_password"],
                        result[0]["is_administrator"],
                        result[0]["is_moderator"])
            return user
                        
        return None
    
    def get_user_by_name(self, name) -> User:

        query = """SELECT * FROM users WHERE name = %s"""
        
        try:
            result = self.db_connection.execute_query(query, (name))
        except LookupError as e:
            raise LookupError
        
        if result:
            user = User(result[0]["user_id"], 
                        result[0]["is_logged_in"], 
                        result[0]["name"],
                        result[0]["hashed_password"],
                        result[0]["is_administrator"],
                        result[0]["is_moderator"])
            return user
                        
        return None
    
    # Query muss gültiger Form entsprechen, Argumente nach Query müssen Reihenfolge in Query entsprechen
    def get_users_by_query(self, query: str, *args) -> list:

        t = ()
        for element in args:
            t += (element)

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
                        element["is_moderator"])
            users.append(user)
        
        return users

    # Speichert einen User in der Datenbank
    def save_user(self, user: User) -> bool:
        
        # -> Neuen Nutzer anlegen, alle nicht aufgezählten Variablen werden automatisch von DB angelegt
        if user.get_user_id() == -1:
            query = """INSERT INTO users (name, hashed_password) 
                       VALUES (%s, %s)"""
            
            try:
                result = self.db_connection.execute_query(query, (user.name, user.hashed_password))
            except LookupError as e:
                return False
            
        # -> Bereits vorhandenen Nutzer wieder in DB speichern
        else:
            query = """UPDATE resources SET user_id = %s,
                                            is_logged_in = %s,
                                            name = %s, 
                                            link = %s, 
                                            created_by = %s, 
                                            faculty = %s, 
                                            ressource_type= %s, 
                                            opening_hours = %s 
                                            WHERE id = %s"""
            
            try:
                result = self.db_connection.execute_query(query, (self.name, self.is_published, self.description, self.link, self.created_by, self.faculty, self.ressource_type, self.opening_hours, self.ressource_id))
            except LookupError as e:
                return False
        
        return True
    
    # ------------------------------------------------- User_Management ------------------------------------------------- #
    def add_user(self, name: str, hashed_password: str) -> bool:
        # Wird von Registrierungsfunktion aufgerufen
    
        user = User(-1, False, name, hashed_password, False, False)
        
        if self.save_user(self, user):
            return True

        return False
    
    # ------------------------- TODO ------------------------------
    # Delete in der Form, dass außer die user_id, alle Werte auf einen Standartwert gesetzt werden
    # -> User laden, alle Attribute bis auf user_id auf -1 / None / etc.
    # -> User speichern
    def delete_user(self, user_id: int) -> bool:

        return True
    
    # Registrierungsfunktion, wird von UI gerufen
    def register_user(self, name, suggested_password) -> bool:
        
        try:
            if self.get_user_by_name(name):
                raise ValueError("Benutzername exisitiert bereits")         # Requirement E1/BM.3 erfüllt - keine doppelten Benutzernamen
        except LookupError as e:
            return False
            
        if len(suggested_password) < 4:
            raise ValueError("Password zu kurz")
        
        md5_hash = hashlib.md5()
        md5_hash.update(suggested_password.encode('utf-8'))
        if self.add_user(name, hash_value = md5_hash.hexdigest()):
            return True
        
        return False

    def promote_user_to_Admin(self, user_id: str) -> bool:
        
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
        except LookupError as e:
            return False
        
        user.set_is_administrator(True)

        try:
            self.save_user(user)
        except LookupError as e:
            return False
        
        return True

    def promote_user_to_Moderator(self, user_id: str) -> bool:

        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
        except LookupError as e:
            return False
        
        user.set_is_moderator(True)

        try:
            self.save_user(user)
        except LookupError as e:
            return False
        
        return True


    def demote_user(self, user_id: str) -> bool:
        
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
        except LookupError as e:
            return False
        
        user.set_is_administrator(False)
        user.set_is_moderator(False)

        try:
            self.save_user(user)
        except LookupError as e:
            return False
        
        return True

    # ------------------------------------------------- Login_System ------------------------------------------------- #
    def login_user(self, username: str, password: str) -> bool:

        try:
            user = self.get_user_by_name(username)
            if not user:
                return False
        except LookupError as e:
            return False
        
        md5_hash = hashlib.md5()
        md5_hash.update(password.encode('utf-8'))
        if md5_hash.hexdigest() == user.get_hashed_password:
            user.set_is_logged_in(True)

        try:
            self.save_user(user)
        except LookupError as e:
            return False
        
        return user.get_is_logged_in()
    
    def loggout_user(self, user_id: int) -> bool:
                
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
        except LookupError as e:
            return False
        
        user.set_is_logged_in(False)

        try:
            self.save_user(user)
        except LookupError as e:
            return False
        
        return not user.get_is_logged_in()
    
    
