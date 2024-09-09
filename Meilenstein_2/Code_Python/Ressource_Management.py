from Code_Python.Database        import Database
from Code_Python.Ressource       import Ressource
from Code_Python.User_Management import User_Management
from Code_Python.User            import User
import random

class Ressource_Management:
    """
    Eine Klasse zur Verwaltung von Ressourcen und deren Interaktion mit der Datenbank.
    Diese Klasse ermöglicht es, Ressourcen zu erstellen, zu ändern, zu löschen und abzufragen.
    """
    def __init__(self, db_connection: Database, user_management: User_Management):
        """
        Initialisiert das Ressource_Management mit einer Datenbankverbindung und einem User-Management-System.

        :param db_connection: Eine Instanz der Database-Klasse zur Interaktion mit der Datenbank.
        :param user_management: Eine Instanz der User_Management-Klasse zur Verwaltung von Benutzern.
        """
        self.db_connection = db_connection
        self.user_management = user_management

    # ------------------------------------------------- Database-Functions ------------------------------------------------- #

    def get_ressource_by_id(self, ressource_id: int) -> Ressource:
        """
        Ruft eine Ressource anhand ihrer ID aus der Datenbank ab.

        :param ressource_id: Die ID der Ressource, die abgerufen werden soll.
        :return: Eine Ressource-Instanz oder None, wenn die Ressource nicht gefunden wurde.
        :raises ValueError: Wenn die Ressource-ID kleiner als 1 ist.
        """
        
        query  = """SELECT * FROM ressources WHERE ressource_id = %s"""
        result = self.db_connection.execute_query(query, (ressource_id,))
        
        if result:
            ressource = Ressource(result[0]["ressource_id"], 
                                  result[0]["name"],      
                                  result[0]["is_published"], 
                                  result[0]["is_deleted"],
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
    
    def get_ressources_by_query(self, query: str, args: list) -> list:
        """
        Führt eine benutzerdefinierte Abfrage aus, um eine Liste von Ressourcen zurückzugeben.

        :param query: Die SQL-Abfrage, die auf die Ressourcen angewendet werden soll.
        :param args: Eine Liste von Argumenten für die SQL-Abfrage.
        :return: Eine Liste von Ressource-Instanzen, die der Abfrage entsprechen.
        :raises LookupError: Wenn ein Fehler bei der Abfrage auftritt.
        """
        t = ()
        for element in args:
            t += (element,)

        try: 
            result = self.db_connection.execute_query(query, t)
        except LookupError as e:
            raise LookupError
        
        ressources = []
        if not result:
            return[]
        for element in result:
            ressource = Ressource(element["ressource_id"], 
                                  element["name"],      
                                  element["is_published"], 
                                  element["is_deleted"],
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
        """
        Speichert eine Ressource in der Datenbank (fügt sie ein oder aktualisiert sie, je nach ID).

        :param ressource: Ein Ressource-Objekt, das gespeichert werden soll.
        :return: True, wenn die Ressource erfolgreich gespeichert wurde, False andernfalls.
        """
        if ressource.ressource_id == -1:
            query = """INSERT INTO ressources (name, is_published, is_deleted, description, link, created_by, faculty, ressource_type, 
                                   opening_hours, likes, experience_reports, ressource_tags) 
                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            t  = (ressource.name, ressource.is_published, ressource.is_deleted, ressource.description, ressource.link, ressource.created_by, ressource.faculty)
            t += (ressource.ressource_type, ressource.opening_hours, ressource.likes, ressource.experience_reports, ressource.ressource_tags)

            try:
                result = self.db_connection.execute_query(query, t)
            except LookupError as e:
                return False
            
        else:
            query = """UPDATE ressources SET name               = %s, 
                                             is_published       = %s, 
                                             is_deleted         = %s,
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
            
            t  = (ressource.name, ressource.is_published, ressource.is_deleted, ressource.description, ressource.link, ressource.created_by, ressource.faculty)
            t += (ressource.ressource_type, ressource.opening_hours, ressource.likes, ressource.experience_reports, ressource.ressource_tags)

            try:
                result = self.db_connection.execute_query(query, t + (ressource.ressource_id,))
            except LookupError as e:
                return False
        
        if not result:      # -> Weil UPDATE
            return True
        return False

    #   ------------------------------------------------- Ressource_Manegement ------------------------------------------------- #  

    # Zum Anlegen einer Ressource
    def add_ressource(self, user_id: int, name: str, description: str, link: str, faculty: str, ressource_type: str, opening_hours: str) -> bool:
        """
        Fügt eine neue Ressource hinzu. Wenn der Ersteller ein Administrator ist, wird die Ressource direkt veröffentlicht.
        Andernfalls wird ein Vorschlag erstellt.

        :param user_id: Die ID des Benutzers, der die Ressource erstellt.
        :param name: Der Name der Ressource.
        :param description: Die Beschreibung der Ressource.
        :param link: Der Link zur Ressource.
        :param faculty: Die Fakultät, der die Ressource zugeordnet ist.
        :param ressource_type: Der Typ der Ressource.
        :param opening_hours: Die Öffnungszeiten der Ressource.
        :return: True, wenn die Ressource erfolgreich hinzugefügt wurde, False andernfalls.
        """
        # -> Wenn der Anleger ein Admin ist, wird Ressource automatisch veröffentlicht
        # -> Wenn der Anleger kein Admin ist, wird Vorschlag erstellt
        is_published = False

        try:
            user = self.user_management.get_user_by_id(user_id)
            if not user:
                return False
        except LookupError as e:
            return False
        
        if user.is_administrator:
            is_published = True

        # -> Userkürzel
        created_by = user.name + "#" + str(user_id)

        # -> Ressource anlegen und in DB speichern
        ressource = Ressource(-1, name, is_published, False, description, link, created_by, faculty, ressource_type, opening_hours, "X", "X", "X")
        
        if not self.save_ressource(ressource):
            return False

        # -> Vorschlag erstellen
        #if not is_published:
        #    query = """SELECT LAST_INSERT_ID()"""
        #    result = self.db_connection.execute_query(query)
        #    ressource_id = result[0]['LAST_INSERT_ID()']
#
        #    if not self.suggest_add_ressource(ressource_id, user_id):
        #        return False
        return True
    
    def change_ressource(self, ressource_id: int, **kwargs) -> bool:
        """
        Ändert eine Ressource basierend auf übergebenen Keyword-Argumenten (kwargs).

        :param ressource_id: Die ID der Ressource, die geändert werden soll.
        :param kwargs: Die Felder und deren neue Werte, die aktualisiert werden sollen.
        :return: True, wenn die Änderung erfolgreich war, False andernfalls.
        """
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
    
    def delete_ressource(self, ressource_id: int, user_id: int, reason: str) -> bool:
        """
        Löscht eine Ressource durch Setzen der is_deleted-Flag und speichert die Löschaktion in der Tabelle deleted_ressources.

        :param ressource_id: Die ID der Ressource, die gelöscht werden soll.
        :param user_id: Die ID des Benutzers, der die Ressource löscht.
        :param reason: Der Grund für die Löschung.
        :return: True, wenn die Ressource erfolgreich gelöscht wurde, False andernfalls.
        """
        try: 
            ressource = self.get_ressource_by_id(int(ressource_id))
        except LookupError as e:
            return False

        ressource.is_deleted = True
        ressource.is_published = False

        query = """INSERT INTO deleted_ressources (ressource_id, user_id, reason) VALUES (%s , %s, %s)"""
        try:
            result = self.db_connection.execute_query(query, (ressource_id, user_id, reason))
        except LookupError as e:
            return False
        
        try:
            self.save_ressource(ressource)
            return True
        except LookupError as e:
            return False
        
    def suggest_add_ressource(self, ressource_id: int, user_id: int) -> bool:

        # Checken ob Umfrage für die Ressource exisitiert
        query = """SELECT * FROM ressource_suggestions WHERE ressource_id = %s"""
        try:
            result = self.db_connection.execute_query(query, (ressource_id,))
            if result:
                return False
        except LookupError as e:
            return False

        # Neue Umfrage erstellen -> Nutzer zum Befragen finden (nicht DELETED, nicht Ersteller)
        user_query = """SELECT * FROM users WHERE user_id != %s AND name != %s"""
        try:
            users = self.user_management.get_users_by_query(user_query, user_id, "Deleted")
            if not users:
                return False
        except LookupError as e:
            return False
        
        # Zufällig Nutzer auswählen
        user_amount = 11

        if(len(users)) < 11:
            user_amount = len(users)
            if user_amount % 2 == 0:
                if not user_amount == 1:
                    user_amount -= 1
                    

        random_users = random.sample(users, user_amount)

        # Vorschlag bei Nutzer hinzufügen
        for user in random_users:
            suggestions = user.ressource_suggestions.split("#")
            suggestions.append(str(ressource_id))
            user.ressource_suggestions = "#".join(suggestions)
        
        # Nutzer wieder speichern
        for user in random_users:
            if not self.user_management.save_user(user):
                return False
            
        # Vorschlag in ressource_suggestions hinzufügen
        user_ids = []
        for user in random_users:
            user_ids.append(str(user.user_id))
        users_to_vote = "#".join(user_ids)

        query = """INSERT INTO ressource_suggestions (ressource_id, amount_voting_users, users_to_vote, vote_accept, vote_reject, is_closed) VALUES (%s, %s, %s, %s, %s, %s)"""
        try:
            self.db_connection.execute_query(query, (ressource_id, len(random_users), users_to_vote, 0, 0, 0))
            return True
        except LookupError as e:
            return False
        
        
        

        


                
        
    
    
