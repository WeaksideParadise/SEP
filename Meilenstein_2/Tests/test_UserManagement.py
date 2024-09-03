import unittest
from unittest.mock import MagicMock
from Code_Python.Database import Database
from Code_Python.User_Management import User_Management
from Code_Python.User import User

class test_UserManagement(unittest.TestCase):

    def setUp(self):
        # Erstellen eines Mock-Datenbankobjekts
        self.mock_db = MagicMock(Database)
        self.user_management = User_Management(self.mock_db)

        # Beispiel User-Objekt
        self.test_user = User(
            user_id=1,
            is_logged_in=False,
            name="TestUser",
            hashed_password="5f4dcc3b5aa765d61d8327deb882cf99",  # MD5 Hash für 'password'
            is_administrator=False,
            is_moderator=False,
            ressource_suggestions="Vorschlag A"
        )

    def test_get_user_by_id_valid(self):
        # Datenbank-Mock-Rückgabe einstellen
        self.mock_db.execute_query.return_value = [{
            "user_id": 1,
            "is_logged_in": False,
            "name": "TestUser",
            "hashed_password": "5f4dcc3b5aa765d61d8327deb882cf99",
            "is_administrator": False,
            "is_moderator": False,
            "ressource_suggestions": "Vorschlag A"
        }]

        user = self.user_management.get_user_by_id(1)
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.name, "TestUser")

    def test_get_user_by_id_invalid(self):
        # Keine Rückgabe von der Datenbank
        self.mock_db.execute_query.return_value = []
        
        user = self.user_management.get_user_by_id(1)
        self.assertIsNone(user)

    def test_get_user_by_name_valid(self):
        # Datenbank-Mock-Rückgabe einstellen
        self.mock_db.execute_query.return_value = [{
            "user_id": 1,
            "is_logged_in": False,
            "name": "TestUser",
            "hashed_password": "5f4dcc3b5aa765d61d8327deb882cf99",
            "is_administrator": False,
            "is_moderator": False,
            "ressource_suggestions": "Vorschlag A"
        }]

        user = self.user_management.get_user_by_name("TestUser")
        self.assertEqual(user.name, "TestUser")

    def test_get_user_by_name_invalid(self):
        # Name ist "Deleted", was nicht erlaubt ist
        with self.assertRaises(ValueError):
            self.user_management.get_user_by_name("Deleted")

    def test_save_user_insert(self):
        # Testet das Einfügen eines neuen Users
        self.test_user.user_id = -1
        self.mock_db.execute_query.return_value = [{"last_row_id": 1}]
        result = self.user_management.save_user(self.test_user)
        self.assertTrue(result)

    def test_save_user_update(self):
        # Testet das Aktualisieren eines bestehenden Users
        self.test_user.user_id = 1
        self.mock_db.execute_query.return_value = []
        result = self.user_management.save_user(self.test_user)
        self.assertTrue(result)

    def test_register_user_existing_name(self):
        # Testet die Registrierung eines Users mit einem bereits vorhandenen Namen
        self.mock_db.execute_query.return_value = [{
            "user_id": 1,
            "is_logged_in": False,
            "name": "TestUser",
            "hashed_password": "5f4dcc3b5aa765d61d8327deb882cf99",
            "is_administrator": False,
            "is_moderator": False,
            "ressource_suggestions": "Vorschlag A"
        }]
        
        with self.assertRaises(NameError):
            self.user_management.register_user("TestUser", "password")

    def test_register_user_short_password(self):
        # Testet die Registrierung eines Users mit zu kurzem Passwort
        with self.assertRaises(ValueError):
            self.user_management.register_user("NewUser", "pwd")

    def test_delete_user(self):
        # Testet das Löschen eines Users
        self.mock_db.execute_query.return_value = [{
            "user_id": 1,
            "is_logged_in": True,
            "name": "TestUser",
            "hashed_password": "5f4dcc3b5aa765d61d8327deb882cf99",
            "is_administrator": True,
            "is_moderator": True,
            "ressource_suggestions": "Vorschlag A"
        }]
        
        result = self.user_management.delete_user(1)
        self.assertTrue(result)

    def test_login_user_valid(self):
        # Testet den erfolgreichen Login eines Users
        self.mock_db.execute_query.return_value = [{
            "user_id": 1,
            "is_logged_in": False,
            "name": "TestUser",
            "hashed_password": "5f4dcc3b5aa765d61d8327deb882cf99",
            "is_administrator": False,
            "is_moderator": False,
            "ressource_suggestions": "Vorschlag A"
        }]

        result = self.user_management.login_user("TestUser", "password")
        self.assertTrue(result)

    def test_login_user_invalid(self):
        # Testet den fehlgeschlagenen Login, wenn das Passwort nicht übereinstimmt
        self.mock_db.execute_query.return_value = [{
            "user_id": 1,
            "is_logged_in": False,
            "name": "TestUser",
            "hashed_password": "5f4dcc3b5aa765d61d8327deb882cf99",
            "is_administrator": False,
            "is_moderator": False,
            "ressource_suggestions": "Vorschlag A"
        }]

        result = self.user_management.login_user("TestUser", "wrong_password")
        self.assertFalse(result)

    def test_logout_user(self):
        # Testet das erfolgreiche Ausloggen eines Users
        self.mock_db.execute_query.return_value = [{
            "user_id": 1,
            "is_logged_in": True,
            "name": "TestUser",
            "hashed_password": "5f4dcc3b5aa765d61d8327deb882cf99",
            "is_administrator": False,
            "is_moderator": False,
            "ressource_suggestions": "Vorschlag A"
        }]
        
        result = self.user_management.logout_user(1)
        self.assertTrue(result)
