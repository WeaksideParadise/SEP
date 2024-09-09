from Code_Python.User                 import User
from Code_Python.Ressource_Search     import Ressource_Search
from Code_Python.Database             import Database
from Code_Python.Ressource            import Ressource
from Code_Python.Ressource_Management import Ressource_Management
import requests
import time
import random
from urllib.parse import urlparse

class Ressource_Actions:
    def __init__(self, db_connection: Database, ressource_management: Ressource_Management):
        self.db_connection = db_connection
        self.ressource_management = ressource_management

    def is_link_functional(self, link: str) -> bool:
        """Controls if a Link gives an Error when trying to reach it."""
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
            query = """SELECT * FROM ressources WHERE is_deleted != %s"""
            ressources = self.ressource_management.get_ressources_by_query(query, [1])
        except LookupError as e:
            return False
        
        for ressource in ressources:
            if not self.is_link_functional(ressource.link):

                check_query = """SELECT * FROM invalid_links WHERE ressource_id = %s"""

                try:
                    result = self.db_connection.execute_query(check_query, (ressource.ressource_id,))
                    if result:
                        continue
                except LookupError as e:
                    return False
                
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
    
    def fetch_5_random_ressources(self) -> list[Ressource]:
        
        try:
            result = self.ressource_management.get_ressources_by_query("SELECT * FROM ressources WHERE is_deleted = %s", [0])
        except LookupError as e:
            raise LookupError
        
        validated_results = []

        for ressource in result:
            if not ressource.is_deleted and ressource.is_published:
                validated_results.append(ressource)
        
        if len(validated_results) <= 5:
            return validated_results
    
        return random.sample(validated_results, 5)

    
    def search_ressources(self, search_query: str, ressource_type_tag: str, faculty_tag: str) -> list:
        
        rs = Ressource_Search(self.db_connection, self.ressource_management, search_query, faculty_tag, ressource_type_tag, None, None)
        
        try:
            rs.search_ressource()
            results = rs.result
            
            for i in range(len(results) - 1, -1, -1):  # Loop from the end of the list to the beginning
                if not results[i].is_published:  # If the result is not published
                    results.pop(i)  # Remove the element          

            return results
        except LookupError as e:
            raise LookupError
        
    def inspect_ressource(self, ressource_id: int,) -> list[Ressource]:

        try:
            ressource = self.ressource_management.get_ressource_by_id(ressource_id)
        except LookupError as e:
            return []
        return [ressource]
    
    # Bonus 
    # noch nicht getestet
    def check_ressource_suggestions(self, ressource: Ressource) -> bool:
        query = """SELECT suggestions FROM users WHERE ressource_suggestions LIKE %s"""
        try:
            # The % around the ressource_id is used to match any string that contains the ressource_id
            result = self.db_connection.execute_query(query, f"%{ressource.ressource_id}%")
            if result:
                return True
            else:
                return False
        except LookupError as e:
            return False
    
    def publish_ressource(self, ressource_id: int ) -> bool:

        try:
            ressource = self.ressource_management.get_ressource_by_id(ressource_id)
        except LookupError as e:
            return False
        
        ressource.is_published = True

        try:
            self.ressource_management.save_ressource(ressource)
        except LookupError as e:
            return False
        
        try:
            query = """DELETE FROM invalid_links WHERE ressource_id = %s"""
            self.db_connection.execute_query(query, (ressource_id,))
            return True
        except LookupError as e:
            return False


    # Bonus
    def suggest_change_ressource(self, ressource_id: int, user_id: int, **kwargs) -> bool:
        # Convert kwargs into a string format, for example: "field_name:value#field_name:value..."
        suggestions = "#".join([f"{key}:{value}" for key, value in kwargs.items()])
        
        query = """SELECT suggestions FROM ressource_suggestions WHERE user_id = %s"""
        try:
            result = self.db_connection.execute_query(query, (user_id,))
            if not result:
                return False
            existing_suggestions = result[0]['suggestions']
            
            if not existing_suggestions:
                new_suggestions = f"{ressource_id}:{suggestions}"
            else:
                new_suggestions = f"{existing_suggestions}#{ressource_id}:{suggestions}"
            
            update_query = """UPDATE ressource_suggestions SET ressource_suggestions = %s WHERE user_id = %s"""
            self.db_connection.execute_query(update_query, (new_suggestions, user_id))
            return True
        except LookupError as e:
            return False

    
    #Bonus - kann verbessert werden
    def check_trustworthyness(self, link: str) -> bool:

        # Predefined list of trusted domains
        trusted_domains = [
            "tu-chemnitz.de", 
            "uni-chemnitz.de",
            "chemnitz.de"  # Add more trusted domains as necessary
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
        query = """INSERT INTO ressource_reports (ressource_id, user_tag, reason) VALUES (%s, %s, %s)"""

        try:
            user = self.ressource_management.user_management.get_user_by_id(user_id)
            user_tag = str(user_id) + "#" + user.name
            self.db_connection.execute_query(query, (ressource_id, user_tag, reason))
        except LookupError as e:
            return False
        return True
    
    def fetch_invalid_link_reports(self) -> list:
        query = """SELECT * FROM invalid_links"""

        try:
            result = self.db_connection.execute_query(query, ())
        except LookupError as e:
            raise LookupError
        return result
    
    def fetch_ressource_reports(self) -> list:
        query = """SELECT * FROM ressource_reports WHERE report_closed = 0"""

        try:
            result = self.db_connection.execute_query(query, ())
        except LookupError as e:
            raise LookupError
        return result
    
    def fetch_deleted_ressources(self) -> list:
        query = """SELECT * FROM deleted_ressources"""

        try:
            result = self.db_connection.execute_query(query, ())
        except LookupError as e:
            raise LookupError
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
            likes.append(str(user_id))
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
    
    def delete_report(self, report_id: int):

        try:
            query = """UPDATE ressource_reports SET report_closed = 1 WHERE report_id = %s"""
            self.db_connection.execute_query(query, (report_id,))
        except LookupError as e:
            return False
        return True
    
    def revive_ressource(self, ressource_id: int):

        try:
            ressource_query = """UPDATE ressources SET is_deleted = 0 WHERE ressource_id = %s"""
            self.db_connection.execute_query(ressource_query, (ressource_id,))
            report_query = """DELETE FROM deleted_ressources WHERE ressource_id = %s"""
            self.db_connection.execute_query(report_query, (ressource_id,))
        except LookupError as e:
            return False
        return True
    
    def vote_for_suggestion(self, user_id: int, ressource_id: int, vote: bool) -> bool:
        try:
           user = self.ressource_management.user_management.get_user_by_id(user_id)
           if not user:
              return False
        except LookupError as e:
            return False
    
        # Schauen ob Nutzer diese überhaupt hat
        suggestions = user.ressource_suggestions.split("#")
        if str(ressource_id) not in suggestions:
            return False
    
        # Suggestion aus DB holen
        query = """SELECT FROM ressource_suggestions WHERE ressource_id = %s"""

        try:
            result = self.db_connection.execute_query(query, (ressource_id,))
        except LookupError as e:
            return False
        
        users_to_vote = result[0]["users_to_vote"].split("#")
        if str(user_id) not in users_to_vote:
            return False
        else:
            users_to_vote.remove(user_id)
            
        # Abstimmen
        vote_accept = int(result[0]["vote_accept"])
        vote_reject = int(result[0]["vote_reject"])
        users_to_vote = "#".join(users_to_vote)
        if vote == True:
            query = """UPDATE ressource_suggestions SET users_to_vote = %s, vote_accept = %s WHERE ressource_id = %s)"""
            try:
                vote_accept += 1
                self.db_connection.execute_query(query, vote_accept, ressource_id)
            except LookupError as e:
                return False
                
        else:
            query = """UPDATE ressource_suggestions SET users_to_vote = %s, vote_reject = %s WHERE ressource_id = %s)"""
            try:
                vote_reject += 1
                self.db_connection.execute_query(query, vote_reject, ressource_id)
            except LookupError as e:
                return False
                
        # Prüfen ob Abstimmung fertig ist
        amount_voters = result[0]["amount_voting_users"]
        if vote_accept > amount_voters // 2:
            is_closed = True
            vote_result = True
        if vote_reject > amount_voters // 2:
            is_closed = True
            vote_result = False

        if is_closed:
            query = """UPDATE ressource_suggestions SET is_closed =%s WHERE ressource_id = %s"""
            try: 
                self.db_connection.execute_query(query, (True, ressource_id))
            except LookupError as e:
                return False
        else:
            return True
                
        # Abstimmung bei restlichen Nutzer entfernen TODO (am Anfang prüfen ob bereits closed)

        #Ergebnisfolge

        if vote_result:
            self.publish_ressource(result[0]["ressource_id"])
        else:
            self.ressource_management.delete_ressource(result[0]["ressource_id"], "Abstimmung fehlgeschlagen")

        return True

    def fetch_suggestions(self, user_id: int) -> list[Ressource]:
        try:
            user = self.ressource_management.user_management.get_user_by_id(user_id)
            if not user:
                raise LookupError
        except LookupError as e:
            raise LookupError
        
        suggestions = str(user.ressource_suggestions).split("#")

        suggestions_to_return = []

        for i in range(1, len(suggestions)):
            try:
                ressource = self.ressource_management.get_ressource_by_id(int(suggestions[i]))
                if not ressource:
                    raise LookupError
            except LookupError as e:
                raise LookupError
            suggestions_to_return.append(ressource)
        
        return suggestions_to_return
            