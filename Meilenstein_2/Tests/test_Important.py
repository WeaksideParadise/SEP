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

    def test_search_ressources_empty_query_Partial(self):
        """Testet, ob eine leere Sucheingabe korrekt verarbeitet wird. Typ oder Fakultät nur jeweils definiert"""
        # Teste eine Suche ohne Eingabe
        results = self.ra.search_ressources('', 'Video' , None)
        assert len(results) < len(self.ra.search_ressources('', None , None))
        # Teste eine Suche ohne Eingabe
        results = self.ra.search_ressources('', None, 'Informatik')
        assert len(results) < len(self.ra.search_ressources('', None , None))

    def test_search_ressources_empty_query_Full(self):
        """Testet, ob eine leere Sucheingabe korrekt verarbeitet wird. (alles definiert)"""   
        # Teste eine Suche ohne Eingabe
        results = self.ra.search_ressources('', 'Video' , 'Informatik')
        assert len(results) < len(self.ra.search_ressources('', None , None))

    def test_search_ressources_partial(self):
        """Testet, ob Fehler bei halboffenen-Legitimen Suchen Fehler auftreten"""
        # Teste eine Suche ohne Eingabe
        results = self.ra.search_ressources('StudiTV', None, None)
        assert len(results) == 1
        # Teste eine Suche ohne Eingabe
        results = self.ra.search_ressources('StudiTV', 'Sonstige' , None)
        assert len(results) == 1
        # Teste eine Suche ohne Eingabe
        results = self.ra.search_ressources('StudiTV', None, 'Informatik')
        assert len(results) == 1
        # Teste eine Suche ohne Eingabe
        results = self.ra.search_ressources('StudiTV', 'Sonstige' , 'Informatik')
        assert len(results) == 1

    
    

