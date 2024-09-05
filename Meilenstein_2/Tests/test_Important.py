import unittest
from unittest.mock import MagicMock, patch
from Tests import test_RessourceActions

import Code_Python.Database 
import Code_Python.User_Management
import Code_Python.Ressource_Management
import Code_Python.Ressource_Actions
import Code_Python.User_Interface
from Code_Python.Ressource import Ressource


class test_Important(unittest.TestCase):
    #wichtige tests, auf dem tatsächlichen code ausgeführt/manuell kontrolliert
    def test_RessourceActions(self):
        rm = test_RessourceActions.test_RessourceActions()
        rm.setUp()
        rm.test_check_trustworthyness_trusted()
        rm.test_check_trustworthyness_untrusted()
        rm.test_is_link_functional_success()
        rm.test_is_link_functional_failure()
        #todo: test search method ( especially mit keine sucheingabe / nur fakultät

    def setUp(self):
        """Set up database, user management, and resource management for tests."""       
        self.db = Code_Python.Database.Database()
        #print("Connected")

        self.um = Code_Python.User_Management.User_Management(self.db)
        self.rm = Code_Python.Ressource_Management.Ressource_Management(self.db, self.um)
        self.ra = Code_Python.Ressource_Actions.Ressource_Actions(self.db, self.rm)

    def test_search_ressources_success(self):
        """Testet eine erfolgreiche Ressourcensuche mit veröffentlichten Ressourcen."""
        # Eine tatsächliche Suche mit gültigen Parametern ausführen
        results = self.ra.search_ressources('StudiTV', 'Bericht', 'Informatik')

        # Überprüfen, ob Ergebnisse zurückgegeben werden
        self.assertIsInstance(results, list)
        for ressource in results:
            self.assertIsInstance(ressource, Ressource)
            self.assertTrue(ressource.is_published)

    def test_search_ressources_excludes_unpublished(self):
        """Testet, ob nicht veröffentlichte Ressourcen herausgefiltert werden."""
        # Führe eine Suche durch, die sowohl veröffentlichte als auch nicht veröffentlichte Ressourcen enthält
        results = self.ra.search_ressources('query_with_unpublished_results', 'type_tag', 'faculty_tag')

        # Überprüfe, dass nur veröffentlichte Ressourcen zurückgegeben werden
        for ressource in results:
            self.assertTrue(ressource.is_published, f"Unveröffentlichte Ressource gefunden: {ressource}")

    def test_search_ressources_empty_query(self):
        """Testet, ob eine leere Sucheingabe korrekt verarbeitet wird."""
        # Teste eine Suche ohne Eingabe
        results = self.ra.search_ressources('', None, None)
        # Teste eine Suche ohne Eingabe
        results = self.ra.search_ressources('', 'Video' , None)
        # Teste eine Suche ohne Eingabe
        results = self.ra.search_ressources('', None, 'Informatik')
        # Teste eine Suche ohne Eingabe
        results = self.ra.search_ressources('', 'Video' , 'Informatik')

    def test_search_ressources_lookup_error(self):
        """Testet, ob bei einer fehlerhaften Suche der richtige Fehler geworfen wird."""
        # Versuche, mit einer ungültigen Fakultät zu suchen, um einen Fehler zu provozieren
        with self.assertRaises(LookupError):
            self.ra.search_ressources('invalid_query', 'invalid_type', 'invalid_faculty')


