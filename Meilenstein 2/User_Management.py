import Database
import User

class User_Management:
    def __init__(self, db_connection: object):
        self.db_connection = db_connection

    def get_user_by_id(self, user_id) -> object:

        query = "SELECT * FROM users WHERE user_id = %s"
        result = self.db_connection.execute_query(query, user_id)
        
        if result:
            user = User(result["user_id"], 
                        result["is_logged_in"], 
                        result["name"],
                        result["hashed_password"],
                        result["is_administrator"])
            return user
                        
        return None
    
    # Name sollte eindeutig sein, da bei der Registrierung auf bereits existernden Namen geprüft wird
    def get_user_by_name(self, name) -> object:

        query = "SELECT * FROM users WHERE name = %s"
        result = self.db_connection.execute_query(query, (name))
        
        if result:
            user = User(result["user_id"], 
                        result["is_logged_in"], 
                        result["name"],
                        result["hashed_password"],
                        result["is_administrator"])
            return user
                        
        return None
    
    # Speichert eine Ressource in der Datenbank (UPDATE)
    def save_user(self, user: object) -> bool:
        if user.get_user_id() == -1:
            query = "INSERT INTO resources (ressource_id, name, is_published, description, link, created_by, faculty, ressource_type, opening hours) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            result = self.db_connection.execute_query(query, (self.name, self.is_published, self.description, self.link, self.created_by, self.faculty, self.ressource_type, self.opening_hours, self.ressource_id))
        else:
            query = "UPDATE resources SET name = %s, is_published = %s, description = %s, link = %s, created_by = %s, faculty = %s, ressource_type= %s, opening_hours = %s WHERE id =%s"
            result = self.db_connection.execute_query(query, (self.name, self.is_published, self.description, self.link, self.created_by, self.faculty, self.ressource_type, self.opening_hours, self.ressource_id))
        if result:
            return True
        return False
    
    def add_user(self, name: str, hashed_password: str) -> bool:
        # Wird von Registrierungsfunktion aufgerufen
    
        user = User(-1, False, name, hashed_password, False)
        saved: bool = self.save_user(user)

        if not saved:
            return False

        return True
    
    def register_user(self, name, suggested_password) -> bool:
        if self.get_user_by_name(name):
            raise ValueError("Benutzername exisitiert bereits")
        
        if len(suggested_password) < 4:
            raise ValueError("Password zu kurz")
        
        if self.add_user(name, hash(suggested_password)):
            return True
        return False

    # Speichert Änderungen an einer Ressource
    def change_ressource(self, ressource_id: int, **kwargs) -> bool:
        return False
    
    def login_user(self, name, password) -> bool:
        user = self.get_user_by_name(name)
        if not user:
            raise ValueError("Es existiert kein Konto mit dem Namen oder das Passwort ist falsch")

        
        if user.get_hashed_password() != hash(password):
            raise ValueError("Es existiert kein Konto mit dem Namen oder das Passwort ist falsch")
            
        user.set_is_logged_in(True)
        self.save_user(user)
        return True
                
