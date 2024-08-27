import Database
import Ressource
import User_Management
import requests

class Ressource_Management:
    def __init__(self, db_connection: Database, user_management: User_Management):
        self.db_connection = db_connection
        self.user_management = user_management

    # ------------------------------------------------- Database based functions ------------------------------------------------- #

    def get_ressource_by_id(self, ressource_id) -> Ressource:

        if ressource_id < 1:
            raise ValueError("ID ist kleiner 1")
        
        query  = """SELECT * FROM ressources WHERE id = %s"""
        result = self.db_connection.execute_query(query, (ressource_id,))
        
        if result:
            ressource = Ressource(result[0]["ressource_id"], 
                                  result[0]["name"],      
                                  result[0]["is_published"], 
                                  result[0]["description"],
                                  result[0]["link"], 
                                  result[0]["created_by"],
                                  result[0]["faculty"],
                                  result[0]["ressource_type"],
                                  result[0]["opening_hours"],
                                  result[0]["likes"],
                                  result[0]["experience_reports"],
                                  result[0]["ressource_tags"])
            return ressource
        return None
    
    def get_ressources_by_query(self, query: str, *args) -> list:

        t = ()
        for element in args:
            t += (element)

        try: 
            result = self.db_connection.execute_query(query, t)
        except LookupError as e:
            raise LookupError
        
        ressources = []

        for element in result:
            ressource = Ressource(element["ressource_id"], 
                                  element["name"],      
                                  element["is_published"], 
                                  element["description"],
                                  element["link"], 
                                  element["created_by"],
                                  element["faculty"],
                                  element["ressource_type"],
                                  element["opening_hours"],
                                  element["likes"],
                                  element["experience_reports"],
                                  element["ressource_tags"])
            ressources.append(ressource)
        
        return ressources
    
    # Speichert eine Ressource in der Datenbank (UPDATE)
    def save_ressource(self, ressource: object) -> bool:
        if ressource.ressource_id == -1:
            query = """INSERT INTO resources (name, is_published, description, link, created_by, faculty, ressource_type, 
                                   opening hours, likes, experience_reports, ressource_tags) 
                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            t  = (ressource.name, ressource.is_published, ressource.description, ressource.link, ressource.created_by, ressource.faculty)
            t += (ressource.ressource_type, ressource.opening_hours, ressource.likes, ressource.experience_reports, ressource.ressource_tags)

            result = self.db_connection.execute_query(query, t)
        else:
            query = """UPDATE resources SET name               = %s, 
                                            is_published       = %s, 
                                            description        = %s, 
                                            link               = %s, 
                                            created_by         = %s, 
                                            faculty            = %s, 
                                            ressource_type     = %s, 
                                            opening_hours      = %s,
                                            likes              = %s,
                                            experience_reports = %s,
                                            ressource_tags     = %s 
                                            WHERE id           = %s"""
            
            t  = (ressource.name, ressource.is_published, ressource.description, ressource.link, ressource.created_by, ressource.faculty)
            t += (ressource.ressource_type, ressource.opening_hours, ressource.likes, ressource.experience_reports, ressource.ressource_tags)

            result = self.db_connection.execute_query(query, t + (self.ressource_id,))

        if result:
            return True
        return False

    # Zum Anlegen einer Ressource
    def add_ressource(self, user_id: int, name: str, description: str, link: str, faculty: str, ressource_type: str, opening_hours: str) -> bool:

        # -> Wenn der Anleger ein Admin ist, wird Ressource automatisch veröffentlicht
        # -> Wenn der Anleger kein Admin ist, wird Vorschlag erstellt
        is_published = False
        user = self.user_management.get_user_by_id(user_id)
        if user and user.is_administrator:
            is_published = True

        # -> Userkürzel
        created_by = user.name + "#" + user.user_id

        # -> Ressource anlegen und in DB speichern
        ressource = Ressource(-1, name, is_published, description, link, created_by, faculty, ressource_type, opening_hours)
        saved= self.save_ressource(ressource)

        if not saved:
            return False

        # -> Vorschlag erstellen
        if not is_published:
            saved = self.suggest_add_ressource(ressource)
            if not saved:
                return False
        
        return True
    
    # --------------------- TODO ------------------------- 
    # ab hier muss noch getestet werden, obs wirklich funktioniert
    def change_ressource(self, ressource_id: int, **kwargs) -> bool:
        # Ensure the resource ID is valid
        if ressource_id < 0:
            return False

        # Dynamically create the SQL query based on kwargs
        set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(ressource_id)

        query = f"UPDATE ressources SET {set_clause} WHERE id = %s"

        # Execute the query
        try:
            result = self.db_connection.execute_query(query, tuple(values))
            return result is not None
        except LookupError as e:
            return False

    def is_link_functional(self, ressource_id: int, link: str) -> bool:
        try:
            # Make a request to the link to check its status
            response = requests.head(link, allow_redirects=True, timeout=5)
            # Check if the status code is in the range of 200-299
            return response.status_code >= 200 and response.status_code < 300
        except requests.RequestException:
            # If there is any request exception, the link is not functional
            return False
    
    # Bonus
    def check_ressource_suggestions(ressource: Ressource) -> bool:

        return True
    
    def publish_ressource(ressource_id:int ) -> bool:

        return True
    
    def suggest_add_ressource(ressource: Ressource) -> bool:

        return True
    
    # Bonus
    def suggest_change_ressource(ressource_id: int, **kwargs) -> bool:

        return True
    
    def delete_ressource(ressource_id: int) -> bool:

        return True
    
    #Bonus
    def check_trustworthyness(link: str) -> bool:

        return True
    
    def report_ressource(ressource_id: int) -> bool:

        return True
    
        return True

        
    
