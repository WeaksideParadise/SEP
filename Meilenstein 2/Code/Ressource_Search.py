import Database
import Ressource_Management

class Ressource_Search:
    def __init__(self, db_connection: Database, rm: Ressource_Management, query: str, faculty_tag: str, ressource_type_tag: str, opening_hours_tag: str, user_tags: list[str], result: list):
        self._db_connection = db_connection
        self.rm = rm
        self._query = query
        self._faculty_tag = faculty_tag
        self._ressource_type_tag = ressource_type_tag
        self._opening_hours_tag = opening_hours_tag      # Nach Opening Hours wird vorerst nicht gefiltert
        self._user_tags = user_tags                      # Bonus
        self._result = []

    # Getter
    
    @property
    def query(self) -> str:
        return self._query
    
    @property
    def faculty_tag(self) -> str:
        return self._faculty_tag
    
    @property
    def ressource_type_tag(self) -> str:
        return self._ressource_type_tag
    
    @property
    def opening_hours_tag(self) -> str:
        return self._opening_hours_tag
    
    @property
    def user_tags(self) -> str:
        return self._user_tags
    
    @property
    def result(self) -> str:
        return self._result
    
    # Setter

    @query.setter
    def query(self, query: str):
        self._query = query
    
    @faculty_tag.setter
    def faculty_tag(self, faculty_tag: str):
        self._faculty_tag = faculty_tag
    
    @ressource_type_tag.setter
    def ressource_type_tag(self, ressource_type_tag: str):
        self._ressource_type_tag = ressource_type_tag
        
    @opening_hours_tag.setter
    def opening_hours_tag(self, opening_hours_tag: str):
        self._opening_hours_tag = opening_hours_tag

    @user_tags.setter
    def user_tags(self, user_tags: str):
        self._user_tags = user_tags
    
    # Methoden

    # -> Filtert faculty_tag
    # -> Filtert ressource_type_tag
    def _filter_ressource_tags(self) -> list[str]:

        to_return = [""]

        if(self.ressource_type_tag):
            to_return.append(f"ressource_type = '{self.ressource_type_tag}'")
        if(self.faculty_tag):
            to_return.append(f"faculty = '{self.faculty_tag}'")

        return to_return

    # -> Fügt eine Suchanfrage für den Ressourcennamen hinzu
    def _search_query(self, to_return: list[str]) -> list[str]:
        
        to_return.append(f"name LIKE = '{self.query}'")
        return to_return
    
    def search_ressource(self) -> list:

        to_search = self._filter_ressource_tags()
        to_search = self._search_query(to_search)
        to_search_query = "AND ".join(to_search)

        query = """SELECT * FROM ressources WHERE """
        query += to_search_query

        try:
            result = self.rm.get_ressource_by_query(query, ())
            return result
        except LookupError as e:
            raise LookupError

