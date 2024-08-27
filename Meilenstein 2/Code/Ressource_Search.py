import Database
import Ressource

class Ressource_Search:
    def __init__(self, db_connection: Database, query: str, faculty_tag: str, ressource_type_tag: str, opening_hours_tag: str, user_tags: list[str], result: list[Ressource] ):
        self.db_connection = db_connection
        self.query = None
        self.faculty_tag = None
        self.ressource_type_tag = None
        self.opening_hours_tag = None
        self.user_tags = None                      # Bonus
        self.result = None

    # ------------------ TODO -------------------
    
    # Getter und Setter

    def filter_ressource_tags(self) -> list[Ressource]:

        return []
    
    def search_query(self) -> list[Ressource]:

        return []
    
    def search_ressource(self) -> list[Ressource]:


