import Database
import Ressource
import User_Management
import Ressource_Search
import requests
import time

class Ressource_Management:
    def __init__(self, db_connection: Database, user_management: User_Management):
        self.db_connection = db_connection
        self.user_management = user_management

    # ------------------------------------------------- Database based functions ------------------------------------------------- #

    def get_ressource_by_id(self, ressource_id) -> Ressource:

        if ressource_id < 1:
            raise ValueError("ID ist kleiner 1")
        
        query  = """SELECT * FROM ressources WHERE ressource_id = %s"""
        result = self.db_connection.execute_query(query, (ressource_id,))
        
        if result:
            ressource = Ressource.Ressource(result[0]["ressource_id"], 
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
            t += (element,)

        try: 
            result = self.db_connection.execute_query(query, t)
        except LookupError as e:
            raise LookupError
        
        ressources = []

        for element in result:
            ressource = Ressource.Ressource(element["ressource_id"], 
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
            query = """INSERT INTO ressources (name, is_published, description, link, created_by, faculty, ressource_type, 
                                   opening_hours, likes, experience_reports, ressource_tags) 
                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            t  = (ressource.name, ressource.is_published, ressource.description, ressource.link, ressource.created_by, ressource.faculty)
            t += (ressource.ressource_type, ressource.opening_hours, ressource.likes, ressource.experience_reports, ressource.ressource_tags)

            try:
                result = self.db_connection.execute_query(query, t)
            except LookupError as e:
                return False
            
        else:
            query = """UPDATE ressources SET name               = %s, 
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
                                             WHERE ressource_id = %s"""
            
            t  = (ressource.name, ressource.is_published, ressource.description, ressource.link, ressource.created_by, ressource.faculty)
            t += (ressource.ressource_type, ressource.opening_hours, ressource.likes, ressource.experience_reports, ressource.ressource_tags)

            try:
                result = self.db_connection.execute_query(query, t + (self.ressource_id,))
            except LookupError as e:
                return False

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
        created_by = user.name + "#" + str(user.user_id)

        # -> Ressource anlegen und in DB speichern
        ressource = Ressource.Ressource(-1, name, is_published, description, link, created_by, faculty, ressource_type, opening_hours, "X#", "X#", "X#")
        saved = self.save_ressource(ressource)

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

        query = f"UPDATE ressources SET {set_clause} WHERE ressource_id = %s"

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
    
    def search_ressources(self, search_query: str, ressource_type_tag: str, faculty_tag: str) -> list:
        
        rs = Ressource_Search.Ressource_Search(self.db_connection, self, search_query, faculty_tag, ressource_type_tag, None, None)
        
        try:
            result = rs.search_ressource()
            return result
        except LookupError as e:
            raise LookupError

    # Bonus
    def check_ressource_suggestions(ressource: Ressource) -> bool:

        return True
    
    def publish_ressource(self, ressource_id: int ) -> bool:

        try:
            ressource = self.get_ressource_by_id(ressource_id)
        except LookupError as e:
            return False
        
        ressource.is_published = True

        try:
            self.save_ressource(ressource)
            return True
        except LookupError as e:
            return False

    def suggest_add_ressource(ressource: Ressource) -> bool:

        return True
    
    # Bonus
    def suggest_change_ressource(ressource_id: int, **kwargs) -> bool:

        return True
    
    def delete_ressource(self, ressource_id: int) -> bool:

        try: 
            ressource = self.get_ressource_by_id(ressource_id)
        except LookupError as e:
            return False

        ressource.name = "Deleted"
        ressource.is_published = False
        ressource.link = None

        try:
            self.save_ressource(ressource)
            return True
        except LookupError as e:
            return False
    
    #Bonus
    def check_trustworthyness(self, link: str) -> bool:

        

        return True
    
    def report_ressource(self, ressource_id: int) -> bool:

        return True
    
    #Bonus
    # -> Likes in Form X#user_id#user_id#........#user_id
    # -> Case unlike mit in Funktion
    def like_ressource(self, ressource_id: int, user_id: int) -> bool:
    
        try:
            ressource = self.get_ressource_by_id(ressource_id)
            if not ressource:
                return False
        except LookupError as e:
            return False
        
        likes = ressource.likes.split("#")
        
        if str(user_id) in likes:
            likes.remove(str(user_id))
            to_save = "#".join(likes)

        else:
            likes.add(str(user_id))
            to_save = "#".join(likes)

        ressource.likes = to_save

        if self.save_ressource(ressource):
            return True
        
        return False
    
    def add_experience_report(self, ressource_id: int, text: str) -> bool:

        try:
            ressource = self.get_ressource_by_id(ressource_id)
        except LookupError as e:
            raise ValueError("Ressource mit ID exisitiert nicht")
        
        # -> timestamp erstellen
        timestamp = time.strftime("Erstellt am %d.%m.%Y um %H:%M:", time.localtime())

        # -> e_r in DB anlegen
        query = """INSERT INTO experience_reports (text, timestamp) VALUES %s, %s"""

        try:
            result = self.db_connection.execute_query(query, (text, timestamp))
        except LookupError as e:
            return False
            
        if "last_row_id" in result[len(result)] - 1:
            er_ids = ressource.experience_reports.split("#")
            er_ids.append(result[len(result)-1]["last_row_id"])
            "#".join(ressource.experience_reports)
        else:
            raise LookupError("Fehler beim Lesen von last_row_id")
        
        try:
            if self.save_ressource(ressource):
                return True
        except LookupError as e:
            return False
                
        return False
    
