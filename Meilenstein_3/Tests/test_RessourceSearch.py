import unittest
from unittest.mock import MagicMock
from Code_Python.Database import Database
from Code_Python.Ressource_Management import Ressource_Management
from Code_Python.Ressource_Search import Ressource_Search
from Code_Python.Ressource import Ressource

class TestRessourceSearch(unittest.TestCase):

    def setUp(self):
        # Mock-Datenbank und Ressource_Management Objekte erstellen
        self.mock_db = MagicMock(Database)
        self.mock_rm = MagicMock(Ressource_Management)

        # Beispiel-Ressourcenobjekt
        self.test_ressource = Ressource(
            ressource_id=1,
            name="TestRessource",
            faculty="Informatik",
            ressource_type="Buch",
            opening_hours="08:00-18:00"
        )

        # Beispiel-Suchobjekt erstellen
        self.ressource_search = Ressource_Search(
            db_connection=self.mock_db,
            rm=self.mock_rm,
            query="Test",
            faculty_tag="Informatik",
            ressource_type_tag="Buch",
            opening_hours_tag="08:00-18:00",
            user_tags=["tag1", "tag2"]
        )

    def test_getters(self):
        # Testet die Getter-Methoden
        self.assertEqual(self.ressource_search.query, "Test")
        self.assertEqual(self.ressource_search.faculty_tag, "Informatik")
        self.assertEqual(self.ressource_search.ressource_type_tag, "Buch")
        self.assertEqual(self.ressource_search.opening_hours_tag, "08:00-18:00")
        self.assertEqual(self.ressource_search.user_tags, ["tag1", "tag2"])
        self.assertEqual(self.ressource_search.result, [])

    def test_setters(self):
        # Testet die Setter-Methoden
        self.ressource_search.query = "NewQuery"
        self.assertEqual(self.ressource_search.query, "NewQuery")
        
        self.ressource_search.faculty_tag = "Mathematik"
        self.assertEqual(self.ressource_search.faculty_tag, "Mathematik")
        
        self.ressource_search.ressource_type_tag = "Artikel"
        self.assertEqual(self.ressource_search.ressource_type_tag, "Artikel")
        
        self.ressource_search.opening_hours_tag = "09:00-17:00"
        self.assertEqual(self.ressource_search.opening_hours_tag, "09:00-17:00")
        
        self.ressource_search.user_tags = ["tag3"]
        self.assertEqual(self.ressource_search.user_tags, ["tag3"])
        
        new_result = [self.test_ressource]
        self.ressource_search.result = new_result
        self.assertEqual(self.ressource_search.result, new_result)

    def test_filter_ressource_tags(self):
        # Testet die Filterung der Ressource-Tags
        expected = [["ressource_type = %s", "faculty = %s"], ["Buch", "Informatik"]]
        result = self.ressource_search._filter_ressource_tags()
        self.assertEqual(result, expected)

    def test_filter_ressource_tags_no_tags(self):
        # Testet das Verhalten, wenn keine Tags gesetzt sind
        self.ressource_search.faculty_tag = ""
        self.ressource_search.ressource_type_tag = ""
        expected = [[], []]
        result = self.ressource_search._filter_ressource_tags()
        self.assertEqual(result, expected)

    def test_search_query(self):
        # Testet die Suche nach der Ressource
        initial_filter = [["ressource_type = %s", "faculty = %s"], ["Buch", "Informatik"]]
        result = self.ressource_search._search_query(initial_filter)
        expected = [["ressource_type = %s", "faculty = %s", "name LIKE %s"], ["Buch", "Informatik", "%Test%"]]
        self.assertEqual(result, expected)

    def test_search_ressource_success(self):
        # Testet die vollständige Suchfunktion, wenn Ressourcen erfolgreich gefunden wurden
        self.mock_rm.get_ressources_by_query.return_value = [self.test_ressource]

        self.ressource_search.search_ressource()
        self.assertEqual(self.ressource_search.result, [self.test_ressource])

        # Überprüft, ob die Methode `get_ressources_by_query` aufgerufen wurde
        self.mock_rm.get_ressources_by_query.assert_called_once()

    def test_search_ressource_no_results(self):
        # Testet die Suchfunktion, wenn keine Ressourcen gefunden werden
        self.mock_rm.get_ressources_by_query.return_value = []

        self.ressource_search.search_ressource()
        self.assertEqual(self.ressource_search.result, [])

    def test_search_ressource_failure(self):
        # Testet die Suchfunktion, wenn eine Ausnahme auftritt
        self.mock_rm.get_ressources_by_query.side_effect = LookupError

        with self.assertRaises(LookupError):
            self.ressource_search.search_ressource()

if __name__ == '__main__':
    unittest.main()
