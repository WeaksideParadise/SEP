import unittest
from unittest.mock import MagicMock, patch
from Code_Python.Ressource_Search import Ressource_Search
from Code_Python.Database import Database
from Code_Python.Ressource import Ressource
from Code_Python.Ressource_Management import Ressource_Management
from Code_Python.Ressource_Actions import Ressource_Actions

class test_RessourceActions(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock(Database)
        self.mock_rm = MagicMock(Ressource_Management)
        self.ressource_actions = Ressource_Actions(self.mock_db, self.mock_rm)

    def test_is_link_functional_success(self):
        with patch('requests.head') as mock_head:
            mock_head.return_value.status_code = 200
            self.assertTrue(self.ressource_actions.is_link_functional("http://example.com"))

    def test_is_link_functional_failure(self):
        with patch('requests.head') as mock_head:
            mock_head.return_value.status_code = 404
            self.assertFalse(self.ressource_actions.is_link_functional("http://example.com"))

    def test_is_link_functional_exception(self):
        with patch('requests.head', side_effect=requests.RequestException):
            self.assertFalse(self.ressource_actions.is_link_functional("http://example.com"))

    def test_check_links_success(self):
        ressource = MagicMock(Ressource)
        ressource.link = "http://example.com"
        ressource.ressource_id = 1
        ressource.is_published = True
        
        self.mock_rm.get_ressources_by_query.return_value = [ressource]
        with patch.object(self.ressource_actions, 'is_link_functional', return_value=False):
            self.assertTrue(self.ressource_actions.check_links())
            self.mock_db.execute_query.assert_called_once()
            self.mock_rm.save_ressource.assert_called_once()

    def test_check_links_failure(self):
        self.mock_rm.get_ressources_by_query.side_effect = LookupError
        self.assertFalse(self.ressource_actions.check_links())

    def test_fetch_5_random_ressources_less_than_5(self):
        ressource = MagicMock(Ressource)
        self.mock_rm.get_ressources_by_query.return_value = [ressource]
        result = self.ressource_actions.fetch_5_random_ressources()
        self.assertEqual(result, [ressource])

    def test_fetch_5_random_ressources_more_than_5(self):
        ressources = [MagicMock(Ressource) for _ in range(10)]
        self.mock_rm.get_ressources_by_query.return_value = ressources
        with patch('random.randint', side_effect=[0, 1, 2, 3, 4]):
            result = self.ressource_actions.fetch_5_random_ressources()
            self.assertEqual(len(result), 10)

    def test_search_ressources_success(self):
        ressource = MagicMock(Ressource)
        ressource.is_published = True
        with patch.object(Ressource_Search, 'search_ressource') as mock_search_ressource:
            mock_search_ressource.return_value = [ressource]
            results = self.ressource_actions.search_ressources("query", "type", "faculty")
            self.assertEqual(results, [ressource])

    def test_search_ressources_failure(self):
        with patch.object(Ressource_Search, 'search_ressource', side_effect=LookupError):
            with self.assertRaises(LookupError):
                self.ressource_actions.search_ressources("query", "type", "faculty")

    def test_inspect_ressource_success(self):
        ressource = MagicMock(Ressource)
        ressource.is_published = True
        self.mock_rm.get_ressource_by_id.return_value = ressource
        result = self.ressource_actions.inspect_ressource(1)
        self.assertEqual(result, [ressource])

    def test_inspect_ressource_failure(self):
        self.mock_rm.get_ressource_by_id.side_effect = LookupError
        result = self.ressource_actions.inspect_ressource(1)
        self.assertEqual(result, [])

    def test_check_ressource_suggestions_found(self):
        ressource = MagicMock(Ressource)
        ressource.ressource_id = 1
        self.mock_db.execute_query.return_value = [{'suggestions': '1'}]
        self.assertTrue(self.ressource_actions.check_ressource_suggestions(ressource))

    def test_check_ressource_suggestions_not_found(self):
        ressource = MagicMock(Ressource)
        ressource.ressource_id = 1
        self.mock_db.execute_query.return_value = []
        self.assertFalse(self.ressource_actions.check_ressource_suggestions(ressource))

    def test_publish_ressource_success(self):
        ressource = MagicMock(Ressource)
        self.mock_rm.get_ressource_by_id.return_value = ressource
        ressource.is_published = False
        self.mock_rm.save_ressource.return_value = True
        self.assertTrue(self.ressource_actions.publish_ressource(1))

    def test_publish_ressource_failure(self):
        self.mock_rm.get_ressource_by_id.side_effect = LookupError
        self.assertFalse(self.ressource_actions.publish_ressource(1))

    def test_suggest_add_ressource_success(self):
        ressource = MagicMock(Ressource)
        ressource.ressource_id = 1
        self.mock_db.execute_query.return_value = [{'suggestions': '1'}]
        self.assertTrue(self.ressource_actions.suggest_add_ressource(ressource, 1))

    def test_suggest_add_ressource_failure(self):
        ressource = MagicMock(Ressource)
        ressource.ressource_id = 1
        self.mock_db.execute_query.side_effect = LookupError
        self.assertFalse(self.ressource_actions.suggest_add_ressource(ressource, 1))

    def test_suggest_change_ressource_success(self):
        self.mock_db.execute_query.return_value = [{'suggestions': '1'}]
        self.assertTrue(self.ressource_actions.suggest_change_ressource(1, 1, field='value'))

    def test_suggest_change_ressource_failure(self):
        self.mock_db.execute_query.side_effect = LookupError
        self.assertFalse(self.ressource_actions.suggest_change_ressource(1, 1, field='value'))

    def test_check_trustworthyness_trusted(self):
        with patch('urllib.parse.urlparse') as mock_urlparse:
            mock_urlparse.return_value.netloc = "tu-chemnitz.de"
            self.assertTrue(self.ressource_actions.check_trustworthyness("http://tu-chemnitz.de"))

    def test_check_trustworthyness_untrusted(self):
        with patch('urllib.parse.urlparse') as mock_urlparse:
            mock_urlparse.return_value.netloc = "untrusted.com"
            self.assertFalse(self.ressource_actions.check_trustworthyness("http://untrusted.com"))

    def test_report_ressource_success(self):
        self.mock_db.execute_query.return_value = True
        self.assertTrue(self.ressource_actions.report_ressource(1, 1, "reason"))

    def test_report_ressource_failure(self):
        self.mock_db.execute_query.side_effect = LookupError
        self.assertFalse(self.ressource_actions.report_ressource(1, 1, "reason"))

    def test_fetch_reports_success(self):
        self.mock_db.execute_query.return_value = [{'report_id': 1}]
        result = self.ressource_actions.fetch_reports()
        self.assertEqual(result, [{'report_id': 1}])

    def test_fetch_reports_failure(self):
        self.mock_db.execute_query.side_effect = LookupError
        with self.assertRaises(LookupError):
            self.ressource_actions.fetch_reports()

    def test_like_ressource_like(self):
        ressource = MagicMock(Ressource)
        ressource.likes = ""
        self.mock_rm.get_ressource_by_id.return_value = ressource
        self.mock_rm.save_ressource.return_value = True
        self.assertTrue(self.ressource_actions.like_ressource(1, 1))
        self.assertEqual(ressource.likes, "1")

    def test_like_ressource_unlike(self):
        ressource = MagicMock(Ressource)
        ressource.likes = "1"
        self.mock_rm.get_ressource_by_id.return_value = ressource
        self.mock_rm.save_ressource.return_value = True
        self.assertTrue(self.ressource_actions.like_ressource(1, 1))
        self.assertEqual(ressource.likes, "")

    def test_like_ressource_failure(self):
        self.mock_rm.get_ressource_by_id.side_effect = LookupError
        self.assertFalse(self.ressource_actions.like_ressource(1, 1))

    def test_add_experience_report_success(self):
        # Arrange
        ressource = MagicMock(Ressource)
        ressource.experience_reports = ""
        self.mock_rm.get_ressource_by_id.return_value = ressource
        self.mock_db.execute_query.return_value = [{'last_row_id': 1}]
        self.mock_rm.save_ressource.return_value = True

        # Act
        result = self.ressource_actions.add_experience_report(1, "test report")

        # Assert
        self.assertTrue(result)
        self.assertIn("1", ressource.experience_reports)
        self.mock_rm.get_ressource_by_id.assert_called_once_with(1)
        self.mock_db.execute_query.assert_called_once_with("INSERT INTO experience_reports (text, timestamp) VALUES (%s, %s)", ("test report", unittest.mock.ANY))
        self.mock_rm.save_ressource.assert_called_once_with(ressource)

    def test_add_experience_report_failure(self):
        # Testfall: Ressource nicht gefunden
        self.mock_rm.get_ressource_by_id.side_effect = LookupError
        with self.assertRaises(ValueError):
            self.ressource_actions.add_experience_report(1, "test report")

        # Testfall: Datenbankfehler beim Einfügen des Berichts
        ressource = MagicMock(Ressource)
        ressource.experience_reports = ""
        self.mock_rm.get_ressource_by_id.return_value = ressource
        self.mock_db.execute_query.side_effect = LookupError

        result = self.ressource_actions.add_experience_report(1, "test report")
        self.assertFalse(result)

        # Testfall: Fehler beim Speichern der Ressource
        self.mock_db.execute_query.return_value = [{'last_row_id': 1}]
        self.mock_rm.save_ressource.return_value = False
        result = self.ressource_actions.add_experience_report(1, "test report")
        self.assertFalse(result)