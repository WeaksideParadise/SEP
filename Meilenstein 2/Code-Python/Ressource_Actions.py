import Database
import Ressource
import Ressource_Management
import Ressource_Search
import requests
import time


class Ressource_Actions:
    def __init__(self, db_connection: Database, ressource_management: Ressource_Management):
        self.db_connection = db_connection
        self.ressource_management = ressource_management

    def is_link_functional(self, link: str) -> bool:
        try:
            # Make a request to the link to check its status
            response = requests.head(link, allow_redirects=True, timeout=5)
            # Check if the status code is in the range of 200-299
            return response.status_code >= 200 and response.status_code < 300
        except requests.RequestException:
            # If there is any request exception, the link is not functional
            return False
        
    # -> Wird von Administrator / Moderator gerufen
    # -> Geht automatisch alle nicht gelöschten Ressourcen durch und prüft Links
    # -> Alle nicht funktionierenden Links werden für Administratoren gesammelt
    # -> Wenn Link nicht funktioniert, wird Ressource unsichtbar gemacht
    # -> Bei Fehler mitten im Ablauf wird Fehler zurückgeworfen
    def check_links(self) -> bool:

        try:
            query = """SELECT * FROM ressources WHERE name != %s"""
            ressources = self.ressource_management.get_ressources_by_query(query, "Deleted")
        except LookupError as e:
            return False
        
        for ressource in ressources:
            if not self.is_link_functional(ressource.link):
                
                link_query = """INSERT INTO invalid_links (ressource_id, invalid_link) VALUES (%s, %s)"""
                
                try:
                    self.db_connection.execute_query(link_query, (ressource.ressource_id, ressource.link))
                except LookupError as e:
                    raise LookupError
                
                ressource.is_published = False
                
                try: 
                    self.ressource_management.save_ressource(ressource)
                except LookupError as e:
                    raise LookupError
        return True

    
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
            ressource = self.ressource_management.get_ressource_by_id(ressource_id)
        except LookupError as e:
            return False
        
        ressource.is_published = True

        try:
            self.ressource_management.save_ressource(ressource)
            return True
        except LookupError as e:
            return False

    def suggest_add_ressource(ressource: Ressource) -> bool:

        return True
    
    # Bonus
    def suggest_change_ressource(ressource_id: int, **kwargs) -> bool:

        return True
    
    #Bonus - kann verbessert werden
    def check_trustworthyness(self, link: str) -> bool:

        # Predefined list of trusted domains
        trusted_domains = [
            "tu-chemnitz.de", 
            "uni-chemnitz.de",
            "chemnitz.de",
            "other-trusted-domain.de"  # Add more trusted domains as necessary
        ]

        # Extract the domain from the link
        try:
            domain = urlparse(link).netloc
        except Exception:
            return False  # Return False if there's an error parsing the link

        # Check if the domain is in the trusted domains list
        if domain in trusted_domains:
            return True

        return False
    
    def report_ressource(self, ressource_id: int, user_id: int, reason: str) -> bool:
        query = """INSERT INTO ressource_reports (ressource_id, user_id, reason) VALUES (%s, %s, %s)"""

        try:
            self.db_connection.execute_query(query, (ressource_id, user_id, reason))
        except LookupError as e:
            return False
        return True
    
    def fetch_reports(self) -> list:
        query = """SELECT * FROM ressource_reports"""

        try:
            result = self.db_connection.execute_query(query, ())
        except LookupError as e:
            return False
        return result
    
    #Bonus
    # -> Likes in Form X#user_id#user_id#........#user_id
    # -> Case unlike mit in Funktion
    def like_ressource(self, ressource_id: int, user_id: int) -> bool:
    
        try:
            ressource = self.ressource_management.get_ressource_by_id(ressource_id)
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

        if self.ressource_management.save_ressource(ressource):
            return True
        
        return False
    
    def add_experience_report(self, ressource_id: int, text: str) -> bool:

        try:
            ressource = self.ressource_management.get_ressource_by_id(ressource_id)
        except LookupError as e:
            raise ValueError("Ressource mit ID exisitiert nicht")
        
        # -> timestamp erstellen
        timestamp = time.strftime("Erstellt am %d.%m.%Y um %H:%M:", time.localtime())

        # -> e_r in DB anlegen
        query = """INSERT INTO experience_reports (text, timestamp) VALUES (%s, %s)"""

        try:
            result = self.db_connection.execute_query(query, (text, timestamp))
        except LookupError as e:
            return False
            
        if "last_row_id" in result[len(result)-1]:
            er_ids = ressource.experience_reports.split("#")
            er_ids.append(str(result[len(result)-1]["last_row_id"]))
            to_save = "#".join(er_ids)
            ressource.experience_reports = to_save
        else:
            raise LookupError("Fehler beim Lesen von last_row_id")
        
        try:
            if self.ressource_management.save_ressource(ressource):
                return True
        except LookupError as e:
            return False
                
        return False