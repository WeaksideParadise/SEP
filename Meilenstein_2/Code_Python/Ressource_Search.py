from Code_Python.Database import Database
from Code_Python.Ressource_Management import Ressource_Management
from Code_Python.Ressource import Ressource

class Ressource_Search:
    """
    Diese Klasse ermöglicht das Suchen nach Ressourcen basierend auf verschiedenen Filterkriterien
    wie Fakultät, Ressourcentyp und Benutzertags. Sie integriert eine Datenbankverbindung und ein
    Ressourcen-Management-System zur Durchführung der Suchabfragen.
    """
    
    def __init__(self, db_connection: Database, rm: Ressource_Management, query: str, faculty_tag: str, ressource_type_tag: str, opening_hours_tag: str, user_tags: list[str]):
        """
        Initialisiert eine Ressource_Search-Instanz mit der Datenbankverbindung und den Suchparametern.
        
        :param db_connection: Verbindung zur Datenbank.
        :param rm: Ressource_Management-Instanz zur Verwaltung von Ressourcen.
        :param query: Suchbegriff für die Ressourcensuche.
        :param faculty_tag: Fakultätstag zum Filtern von Ressourcen.
        :param ressource_type_tag: Ressourcentyp-Tag zum Filtern von Ressourcen.
        :param opening_hours_tag: Öffnungszeiten-Tag, derzeit nicht aktiv.
        :param user_tags: Liste von Tags, die Benutzerspezifisch sind (Bonus-Funktion).
        """
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
        """
        Gibt den aktuellen Suchbegriff zurück.
        
        :return: Der Suchbegriff als String.
        """
        return self._query
    
    @property
    def faculty_tag(self) -> str:
        """
        Gibt das aktuelle Fakultätstag zurück.
        
        :return: Das Fakultätstag als String.
        """
        return self._faculty_tag
    
    @property
    def ressource_type_tag(self) -> str:
        """
        Gibt das aktuelle Ressourcentyp-Tag zurück.
        
        :return: Das Ressourcentyp-Tag als String.
        """
        return self._ressource_type_tag
    
    @property
    def opening_hours_tag(self) -> str:
        """
        Gibt das aktuelle Öffnungszeiten-Tag zurück.
        
        :return: Das Öffnungszeiten-Tag als String.
        """
        return self._opening_hours_tag
    
    @property
    def user_tags(self) -> str:
        """
        Gibt die aktuellen Benutzertags zurück.
        
        :return: Die Benutzertags als Liste von Strings.
        """
        return self._user_tags
    
    @property
    def result(self) -> list[Ressource]:
        """
        Gibt die Ergebnisliste der Ressourcensuche zurück.
        
        :return: Liste von Ressourcen.
        """
        return self._result
    
    # Setter

    @query.setter
    def query(self, query: str):
        """
        Setzt den Suchbegriff.
        
        :param query: Der neue Suchbegriff als String.
        """
        self._query = query
    
    @faculty_tag.setter
    def faculty_tag(self, faculty_tag: str):
        """
        Setzt das Fakultätstag.
        
        :param faculty_tag: Das neue Fakultätstag als String.
        """
        self._faculty_tag = faculty_tag
    
    @ressource_type_tag.setter
    def ressource_type_tag(self, ressource_type_tag: str):
        """
        Setzt das Ressourcentyp-Tag.
        
        :param ressource_type_tag: Der neue Ressourcentyp als String.
        """
        self._ressource_type_tag = ressource_type_tag
        
    @opening_hours_tag.setter
    def opening_hours_tag(self, opening_hours_tag: str):
        """
        Setzt das Öffnungszeiten-Tag.
        
        :param opening_hours_tag: Das neue Öffnungszeiten-Tag als String.
        """
        self._opening_hours_tag = opening_hours_tag

    @user_tags.setter
    def user_tags(self, user_tags: str):
        """
        Setzt die Benutzertags.
        
        :param user_tags: Die neuen Benutzertags als Liste von Strings.
        """
        self._user_tags = user_tags

    @result.setter
    def result(self, result: list[Ressource]):
        """
        Setzt die Ergebnisliste der Ressourcensuche.
        
        :param result: Die neue Ergebnisliste als Liste von Ressourcen.
        """
        self._result = result
    
    # Methoden

    def _filter_ressource_tags(self) -> list[list[str]]:
        """
        Filtert Ressourcen basierend auf den Tags für Ressourcentyp und Fakultät.
        
        :return: Eine Liste von zwei Listen. Die erste enthält SQL-Bedingungen, die zweite die zugehörigen Parameter.
        """
        to_return = [[],[]]

        if(self.ressource_type_tag):
            to_return[0].append(f"ressource_type = %s")
            to_return[1].append(self.ressource_type_tag)
        if(self.faculty_tag):
            to_return[0].append(f"faculty = %s")
            to_return[1].append(self.faculty_tag)

        return to_return

    def _search_query(self, to_return: list[list[str]]) -> list[list[str]]:
        """
        Fügt eine SQL-Bedingung für die Suche nach dem Ressourcen-Namen hinzu.
        
        :param to_return: Eine Liste von zwei Listen, die SQL-Bedingungen und Parameter enthalten.
        :return: Aktualisierte Liste mit einer Bedingung für die Namenssuche.
        """
        to_return[0].append(f"name LIKE %s")
        to_return[1].append(f"%{self.query}%")
        return to_return
    
    def search_ressource(self) -> list:
        """
        Führt die Suche nach Ressourcen durch und gibt die Ergebnisse zurück.
        
        :return: Eine Liste von Ressourcen, die den Suchkriterien entsprechen.
        :raises LookupError: Wenn ein Fehler bei der Ressourcenabfrage auftritt.
        """
        to_search = self._filter_ressource_tags()
        to_search = self._search_query(to_search)

        query = """SELECT * FROM ressources"""

        if to_search[0]:
            query = """SELECT * FROM ressources WHERE """
            if len(to_search[0]) == 1:
                query += to_search[0][0]
            else:
                to_search_query = " AND ".join(to_search[0])
                query += to_search_query

        try:
            result = self.rm.get_ressources_by_query(query, to_search[1])
            self.result = result
        except LookupError as e:
            raise LookupError
