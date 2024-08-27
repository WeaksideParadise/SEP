import Database
import Ressource
import User_Management

class Ressource_Management:
    def __init__(self, db_connection: Database, user_management: User_Management):
        self.db_connection = db_connection
        self.user_management = user_management

    # ------------------------------------------------- Database based functions ------------------------------------------------- #

    def get_ressource_by_id(self, ressource_id) -> object:

        query = "SELECT * FROM ressources WHERE id = %s"
        result= self.db_connection.execute_query(query, ressource_id)
        
        if result:
            ressource = Ressource(result["ressource_id"], 
                                  result["name"],      
                                  result["is_published"], 
                                  result["description"],
                                  result["link"], 
                                  result["created_by"],
                                  result["faculty"],
                                  result["ressource_type"],
                                  result["opening_hours"])
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
            ressource = Ressource(result["ressource_id"], 
                                  result["name"],      
                                  result["is_published"], 
                                  result["description"],
                                  result["link"], 
                                  result["created_by"],
                                  result["faculty"],
                                  result["ressource_type"],
                                  result["opening_hours"])
            ressources.append(ressource)
        
        return ressources
    
    # Speichert eine Ressource in der Datenbank (UPDATE)
    def save_ressource(self, ressource: object) -> bool:
        if ressource.get_ressource_id() == -1:
            query = """INSERT INTO resources (ressource_id, name, is_published, description, link, created_by, faculty, ressource_type, opening hours) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            result = self.db_connection.execute_query(query, (self.name, self.is_published, self.description, self.link, self.created_by, self.faculty, self.ressource_type, self.opening_hours, self.ressource_id))
        else:
            query = """UPDATE resources SET name = %s, 
                                            is_published = %s, 
                                            description = %s, 
                                            link = %s, 
                                            created_by = %s, 
                                            faculty = %s, 
                                            ressource_type= %s, 
                                            opening_hours = %s 
                                            WHERE id =%s"""
            # TODO: Bonusanforderungen (Attribute) hinzufügen
            
            result = self.db_connection.execute_query(query, (self.name, self.is_published, self.description, self.link, self.created_by, self.faculty, self.ressource_type, self.opening_hours, self.ressource_id))
        if result:
            return True
        return False

    # Zum Anlegen einer Ressource
    def add_ressource(self, user_id: int, name: str, description: str, link: str, faculty: str, ressource_type: str, opening_hours: str) -> bool:

        # Wenn der Anleger ein Admin ist, wird Ressource automatisch veröffentlicht
        # Wenn der Anleger kein Admin ist, wird Vorschlag erstellt
        is_published = False
        if(self.user_management.is_administrator(user_id)):
            is_published = True

        created_by = self.user_management.get_user_identifier(user_id)

        ressource = Ressource(-1, name, is_published, description, link, created_by, faculty, ressource_type, opening_hours)
        #ressource_id = .........

        saved: bool = self.save_ressource(ressource)

        if not saved:
            return False

        if not is_published:
            saved = self.create_poll("Add", ressource_id)
            if not saved:
                return False
        
        return True
    
    # --------------------- TODO ------------------------- 
    
    def change_ressource(self, ressource_id: int, **kwargs) -> bool:

        return True
    
    def is_link_funcitonal(self, ressource_id: int, link: str) -> bool:

        return True
    
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

    

        
    
