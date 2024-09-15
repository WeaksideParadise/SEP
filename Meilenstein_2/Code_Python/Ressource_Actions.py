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
    """
    Klasse zur Verwaltung von Aktionen im Zusammenhang mit Ressourcen, einschließlich der Überprüfung von Links, 
    Berichterstattung, Abstimmungen und Veröffentlichung.
    """
    def __init__(self, db_connection: Database, ressource_management: Ressource_Management):
        """
        Initialisiert die Ressource_Actions-Klasse mit einer Datenbankverbindung und Ressourcenverwaltung.

        Args:
            db_connection (Database): Datenbankverbindung.
            ressource_management (Ressource_Management): Ressourcenverwaltungsinstanz.
        """
        self.db_connection = db_connection
        self.ressource_management = ressource_management

    def is_link_functional(self, link: str) -> bool:
        """
        Überprüft, ob ein Link funktionsfähig ist, indem eine HTTP OPTIONS-Anfrage gesendet wird.

        Args:
            link (str): Die zu überprüfende URL.

        Returns:
            bool: True, wenn der Link funktionsfähig ist, False, wenn nicht.
        """
        try:
            response = requests.options(link)
            if response.ok:   # alternatively you can use response.status_code == 200
                return True
            else:
                {}#print(f"Failure - API is accessible but sth is not right. Response codde : {response.status_code}")
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            {}#print(f"Failure - Unable to establish connection: {e}.")
        except Exception as e:
            {}#print(f"Failure - Unknown error occurred: {e}.")
        return False

    # -> Wird von Administrator / Moderator gerufen
    # -> Geht automatisch alle nicht gelöschten Ressourcen durch und prüft Links
    # -> Alle nicht funktionierenden Links werden für Administratoren gesammelt
    # -> Wenn Link nicht funktioniert, wird Ressource unsichtbar gemacht
    # -> Bei Fehler mitten im Ablauf wird Fehler zurückgeworfen
    def check_links(self) -> bool:
        """
        Überprüft alle nicht gelöschten Ressourcen auf funktionierende Links, sammelt ungültige Links und markiert 
        die Ressource als nicht veröffentlicht, wenn der Link nicht funktioniert.

        Returns:
            bool: True, wenn der Prozess ohne Fehler abgeschlossen wurde, False, wenn nicht.
        """
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
        """
        Ruft 5 zufällige, nicht gelöschte und veröffentlichte Ressourcen aus der Datenbank ab.

        Returns:
            list[Ressource]: Eine Liste von bis zu 5 zufälligen Ressourcen.
        """
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
        """
        Sucht nach Ressourcen basierend auf der Suchanfrage, dem Ressourcentyp und den Fakultätstags, 
        unter Ausschluss von unveröffentlichten Ressourcen.

        Args:
            search_query (str): Suchbegriff oder -phrase.
            ressource_type_tag (str): Tag, der sich auf den Ressourcentyp bezieht.
            faculty_tag (str): Tag, der sich auf die Fakultät bezieht.

        Returns:
            list: Eine Liste von übereinstimmenden Ressourcen.
        """
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
        """
        Ruft die Details einer bestimmten Ressource anhand ihrer ID ab.

        Args:
            ressource_id (int): Die ID der Ressource.

        Returns:
            list[Ressource]: Eine Liste, die die inspizierte Ressource enthält, oder eine leere Liste, wenn nicht gefunden.
        """
        try:
            ressource = self.ressource_management.get_ressource_by_id(ressource_id)
        except LookupError as e:
            return []
        return [ressource]
    
    # Bonus 
    # noch nicht getestet
    def check_ressource_suggestions(self, ressource: Ressource) -> bool:
        """
        Überprüft, ob es Benutzervorschläge für eine bestimmte Ressource gibt.

        Args:
            ressource (Ressource): Das Ressourcenobjekt.

        Returns:
            bool: True, wenn Vorschläge existieren, False, wenn nicht.
        """
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
        """
        Veröffentlicht eine Ressource, indem das is_published-Flag auf True gesetzt und sie ggf. 
        aus der Liste der ungültigen Links entfernt wird.

        Args:
            ressource_id (int): Die ID der zu veröffentlichenden Ressource.

        Returns:
            bool: True, wenn die Ressource erfolgreich veröffentlicht wurde, False, wenn nicht.
        """
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
        """
        Erlaubt Benutzern, Änderungen an einer Ressource vorzuschlagen, und speichert die Vorschläge in der Datenbank.

        Args:
            ressource_id (int): Die ID der Ressource.
            user_id (int): Die ID des Benutzers, der Änderungen vorschlägt.
            **kwargs: Die vorgeschlagenen Änderungen in Schlüssel-Wert-Paaren (Feld: neuer Wert).

        Returns:
            bool: True, wenn der Vorschlag erfolgreich erfasst wurde, False, wenn nicht.
        """
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
        """
        Überprüft, ob der angegebene Link von einer vertrauenswürdigen Domain stammt.

        Args:
            link (str): Die zu überprüfende URL.

        Returns:
            bool: True, wenn der Link zu einer vertrauenswürdigen Domain gehört, False, wenn nicht.
        """
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
        """
        Ermöglicht Benutzern, eine Ressource mit einem bestimmten Grund zu melden.

        Args:
            ressource_id (int): Die ID der Ressource.
            user_id (int): Die ID des Benutzers, der die Ressource meldet.
            reason (str): Der Grund für die Meldung.

        Returns:
            bool: True, wenn die Meldung erfolgreich erfasst wurde, False, wenn nicht.
        """
        query = """INSERT INTO ressource_reports (ressource_id, user_tag, reason) VALUES (%s, %s, %s)"""

        try:
            user = self.ressource_management.user_management.get_user_by_id(user_id)
            user_tag = str(user_id) + "#" + user.name
            self.db_connection.execute_query(query, (ressource_id, user_tag, reason))
        except LookupError as e:
            return False
        return True
    
    def fetch_invalid_link_reports(self) -> list:
        """
        Ruft alle Berichte über ungültige Links aus der Datenbank ab.

        Returns:
            list: Eine Liste von Datensätzen mit ungültigen Links.
        """
        query = """SELECT * FROM invalid_links"""

        try:
            result = self.db_connection.execute_query(query, ())
        except LookupError as e:
            raise LookupError
        return result
    
    def fetch_ressource_reports(self) -> list:
        """
        Holt alle Ressourcennachberichte, bei denen der Bericht noch nicht geschlossen ist.

        :return: Liste der Ressourcennachberichte.
        :rtype: list
        """
        query = """SELECT * FROM ressource_reports WHERE report_closed = 0"""

        try:
            result = self.db_connection.execute_query(query, ())
        except LookupError as e:
            raise LookupError
        return result
    
    def fetch_deleted_ressources(self) -> list:
        """
        Holt alle gelöschten Ressourcen.

        :return: Liste der gelöschten Ressourcen.
        :rtype: list
        """
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
        """
        Holt alle gelöschten Ressourcen.

        :return: Liste der gelöschten Ressourcen.
        :rtype: list
        """
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
        """
        Füge einen Like oder entferne ihn für eine Ressource, abhängig davon, ob der Benutzer die Ressource bereits geliked hat.

        :param ressource_id: Die ID der Ressource.
        :type ressource_id: int
        :param user_id: Die ID des Benutzers.
        :type user_id: int
        :return: True, wenn die Operation erfolgreich war, ansonsten False.
        :rtype: bool
        """
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
        """
            Fügt einen Erfahrungsbericht zu einer Ressource hinzu.

            :param ressource_id: Die ID der Ressource, zu der der Bericht hinzugefügt werden soll.
            :type ressource_id: int
            :param text: Der Text des Erfahrungsberichts.
            :type text: str
            :return: True, wenn der Bericht erfolgreich hinzugefügt wurde, ansonsten False.
            :rtype: bool
        """
        try:
            query = """UPDATE ressource_reports SET report_closed = 1 WHERE report_id = %s"""
            self.db_connection.execute_query(query, (report_id,))
        except LookupError as e:
            return False
        return True
    
    def revive_ressource(self, ressource_id: int):
        """
        Macht eine gelöschte Ressource wieder aktiv, indem der Löschstatus zurückgesetzt und die Ressource aus der Liste der gelöschten Ressourcen entfernt wird.

        :param ressource_id: Die ID der Ressource, die wiederhergestellt werden soll.
        :type ressource_id: int
        :return: True, wenn die Ressource erfolgreich wiederhergestellt wurde, ansonsten False.
        :rtype: bool
        """
        try:
            ressource_query = """UPDATE ressources SET is_deleted = 0 WHERE ressource_id = %s"""
            self.db_connection.execute_query(ressource_query, (ressource_id,))
            report_query = """DELETE FROM deleted_ressources WHERE ressource_id = %s"""
            self.db_connection.execute_query(report_query, (ressource_id,))
        except LookupError as e:
            return False
        return True
    
    def get_suggestion_for_user(self, user_id: int, ressource_id: int) -> dict[str, any]:
        """
        Holt den Vorschlag für eine Ressource eines Benutzers, falls dieser existiert.

        :param user_id: Die ID des Benutzers.
        :type user_id: int
        :param ressource_id: Die ID der Ressource, für die der Vorschlag geholt werden soll.
        :type ressource_id: int
        :return: Der Vorschlag als Dictionary, falls vorhanden; andernfalls eine leere Liste.
        :rtype: dict[str, any]
        """
        try:
           user = self.ressource_management.user_management.get_user_by_id(user_id)
           if not user:
              return []
        except LookupError as e:
            return []
    
        # Schauen ob Nutzer diese überhaupt hat
        suggestions = user.ressource_suggestions.split("#")
        if str(ressource_id) not in suggestions:
            return []
    
        # Suggestion aus DB holen
        query = """SELECT * FROM ressource_suggestions WHERE ressource_id = %s"""

        try:
            result = self.db_connection.execute_query(query, (ressource_id,))
            return result[0]
        except LookupError as e:
            return []
        
    def remove_suggestions_for_user(self, user_id: int, ressource_id: int) -> bool:
        """
        Entfernt einen Vorschlag für eine Ressource von einem Benutzer.

        :param user_id: Die ID des Benutzers.
        :type user_id: int
        :param ressource_id: Die ID der Ressource, für die der Vorschlag entfernt werden soll.
        :type ressource_id: int
        :return: True, wenn der Vorschlag erfolgreich entfernt wurde, ansonsten False.
        :rtype: bool
        """
        try:
           user = self.ressource_management.user_management.get_user_by_id(user_id)
           if not user:
              return False
        except LookupError as e:
            return False
        
        suggestions = user.ressource_suggestions.split("#")
        suggestions.remove(str(ressource_id))
        user.ressource_suggestions = "#".join(suggestions)

        if not self.ressource_management.user_management.save_user(user):
            return False
        return True

    def vote_for_suggestion(self, user_id: int, ressource_id: int, vote: bool) -> bool:
        """
        Gibt eine Stimme für einen Vorschlag ab oder entfernt die Stimme, falls der Vorschlag bereits geschlossen ist.

        :param user_id: Die ID des Benutzers, der abstimmt.
        :type user_id: int
        :param ressource_id: Die ID der Ressource, für die abgestimmt wird.
        :type ressource_id: int
        :param vote: True für eine Zustimmung, False für eine Ablehnung.
        :type vote: bool
        :return: True, wenn die Abstimmung erfolgreich war, ansonsten False.
        :rtype: bool
        """
        result = self.get_suggestion_for_user(user_id, ressource_id)

        if not result:
            return False
        
        #(am Anfang prüfen ob bereits closed)
        if result["is_closed"]:
            if not self.remove_suggestions_for_user(user_id, ressource_id):
                return False
            return True
        
        users_to_vote = result["users_to_vote"].split("#")
        if str(user_id) not in users_to_vote:
            return False
        else:
            users_to_vote.remove(str(user_id))
            
        # Abstimmen
        vote_accept = int(result["vote_accept"])
        vote_reject = int(result["vote_reject"])
        users_to_vote = "#".join(users_to_vote)

        if vote == True:
            query = """UPDATE ressource_suggestions SET users_to_vote = %s, vote_accept = %s WHERE ressource_id = %s"""
            try:
                vote_accept += 1
                self.db_connection.execute_query(query, (users_to_vote, vote_accept, ressource_id))
            except LookupError as e:
                return False
                
        else:
            query = """UPDATE ressource_suggestions SET users_to_vote = %s, vote_reject = %s WHERE ressource_id = %s"""
            try:
                vote_reject += 1
                self.db_connection.execute_query(query, (users_to_vote, vote_reject, ressource_id))
            except LookupError as e:
                return False
                
        # Prüfen ob Abstimmung fertig ist
        amount_voters = result["amount_voting_users"]
        is_closed = False
        if vote_accept > amount_voters // 2:
            is_closed = True
            vote_result = True
        if vote_reject > amount_voters // 2:
            is_closed = True
            vote_result = False

        if not self.remove_suggestions_for_user(user_id, ressource_id):
            return False

        if is_closed:
            query = """UPDATE ressource_suggestions SET is_closed = %s WHERE ressource_id = %s"""
            try: 
                self.db_connection.execute_query(query, (True, ressource_id))
            except LookupError as e:
                return False
        
        #Ergebnisfolge

            if vote_result:
                self.publish_ressource(result["ressource_id"])
            else:
                self.ressource_management.delete_ressource(result["ressource_id"], -100, "Abstimmung fehlgeschlagen")

        return True

    def fetch_suggestions(self, user_id: int) -> list[Ressource]:
        """
        Holt alle Vorschläge für Ressourcen eines Benutzers.

        :param user_id: Die ID des Benutzers, dessen Vorschläge abgerufen werden sollen.
        :type user_id: int
        :return: Liste der Ressourcen, die als Vorschläge des Benutzers vorhanden sind.
        :rtype: list[Ressource]
        """
        if user_id == -1:
            return []
        
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
    
    def fetch_most_liked_ressources(self) -> list[Ressource]:
        """
        Holt die fünf am meisten gelikten Ressourcen.

        :return: Liste der fünf am meisten gelikten Ressourcen.
        :rtype: list[Ressource]
        """
        query = """SELECT * FROM ressources WHERE is_published = %s and is_deleted = %s"""
        
        ressources = self.ressource_management.get_ressources_by_query(query, [True, False])
        if not ressources:
            return []
        
        sorted_by_likes = sorted(ressources, key= lambda ressource : len(ressource.likes.split("#")), reverse = True)

        return sorted_by_likes[0:5]
    
    def list_likes(self, ressources: list[Ressource]) -> list[int]:
        """
        Gibt die Anzahl der Likes für jede Ressource in der Liste zurück.

        :param ressources: Liste der Ressourcen, für die die Anzahl der Likes ermittelt werden soll.
        :type ressources: list[Ressource]
        :return: Liste der Anzahl der Likes für jede Ressource.
        :rtype: list[int]
        """
        to_return = []
        for ressource in ressources:
            to_return.append(len(ressource.likes.split("#"))-1)

        return to_return
    
    def is_liked_by_user(self, user_id: int, ressources: list[Ressource]) -> list[bool]:
        """
        Überprüft, ob eine Ressource von einem bestimmten Benutzer geliked wurde.

        :param user_id: Die ID des Benutzers.
        :type user_id: int
        :param ressources: Liste der Ressourcen, die überprüft werden sollen.
        :type ressources: list[Ressource]
        :return: Liste von Boolean-Werten, die angeben, ob jede Ressource vom Benutzer geliked wurde.
        :rtype: list[bool]
        """
        to_return = []
        for ressource in ressources:
            if user_id and str(user_id) in ressource.likes.split("#"):
                to_return.append(True)
            else:
                to_return.append(False)

        return to_return
    
    def check_if_already_exists(self, link: str) -> bool:
        """
        Überprüft, ob eine Ressource mit dem angegebenen Link bereits existiert.

        :param link: Der Link der Ressource, die überprüft werden soll.
        :type link: str
        :return: True, wenn die Ressource bereits existiert, ansonsten False.
        :rtype: bool
        """
        query = """SELECT * FROM ressources WHERE link = %s"""

        try:
            result = self.ressource_management.get_ressources_by_query(query, [link])
        except LookupError as e:
            return True

        if result:
            return True
        return False


            