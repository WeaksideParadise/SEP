import unittest
from unittest.mock import MagicMock, patch
from Code_Python.Database import Database
from Code_Python.Ressource import Ressource
from Code_Python.User_Management import User_Management
from Code_Python.Ressource_Management import Ressource_Management

class test_RessourceManagement(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock(Database)
        self.mock_user_management = MagicMock(User_Management)
        self.ressource_management = Ressource_Management(self.mock_db, self.mock_user_management)

    def test_get_ressources_by_query_valid(self):
        # Arrange
        query = "SELECT * FROM ressources WHERE name LIKE %s"
        args = ["%Test%"]
        mock_ressources_data = [{
            "ressource_id": 1,
            "name": "Test Ressource",
            "is_published": True,
            "is_deleted": False,
            "description": "Test Description",
            "link": "http://example.com",
            "created_by": "user#1",
            "faculty": "Engineering",
            "ressource_type": "Book",
            "opening_hours": "9-5",
            "likes": 10,
            "experience_reports": "Great!",
            "ressource_tags": "tag1,tag2"
        }]
        self.mock_db.execute_query.return_value = mock_ressources_data

        # Act
        ressources = self.ressource_management.get_ressources_by_query(query, args)

        # Assert
        self.assertEqual(len(ressources), 1)
        self.assertEqual(ressources[0].name, "Test Ressource")
        self.mock_db.execute_query.assert_called_once_with(query, tuple(args))

    def test_save_ressource_insert(self):
        # Arrange
        mock_ressource = Ressource(-1, "New Ressource", False, False, "Description", "http://example.com", "user#1", "Engineering", "Book", "9-5", "0", "None", "tag1")
        self.mock_db.execute_query.return_value = None

        # Act
        result = self.ressource_management.save_ressource(mock_ressource)

        # Assert
        self.assertTrue(result)
        self.mock_db.execute_query.assert_called()

    def test_save_ressource_update(self):
        # Arrange
        mock_ressource = Ressource(1, "Updated Ressource", True, False, "Description", "http://example.com", "user#1", "Engineering", "Book", "9-5", "0", "None", "tag1")
        self.mock_db.execute_query.return_value = None

        # Act
        result = self.ressource_management.save_ressource(mock_ressource)

        # Assert
        self.assertTrue(result)
        self.mock_db.execute_query.assert_called()

    def test_add_ressource_admin_user(self):
        # Arrange
        mock_user = MagicMock()
        mock_user.is_administrator = True
        self.mock_user_management.get_user_by_id.return_value = mock_user

        # Act
        result = self.ressource_management.add_ressource(1, "Ressource Name", "Description", "http://example.com", "Engineering", "Book", "9-5")

        # Assert
        self.assertTrue(result)
        self.mock_user_management.get_user_by_id.assert_called_once_with(1)
        self.mock_db.execute_query.assert_called()

    def test_add_ressource_non_admin_user(self):
        # Arrange
        mock_user = MagicMock()
        mock_user.is_administrator = False
        self.mock_user_management.get_user_by_id.return_value = mock_user

        # Act
        result = self.ressource_management.add_ressource(1, "Ressource Name", "Description", "http://example.com", "Engineering", "Book", "9-5")

        # Assert
        self.assertFalse(result) # existiert hier schon deshalb false
        self.mock_user_management.get_user_by_id.assert_called_once_with(1)
        self.mock_db.execute_query.assert_called()

    def test_change_ressource(self):
        # Arrange
        self.mock_db.execute_query.return_value = None

        # Act
        result = self.ressource_management.change_ressource(1, name="Updated Name", description="Updated Description")

        # Assert
        self.assertFalse(result)
        self.mock_db.execute_query.assert_called()

    def test_delete_ressource(self):
        # Arrange
        mock_ressource = Ressource(1, "Test Ressource", True,False, "Description", "http://example.com", "user#1", "Engineering", "Book", "9-5", 10, "Great!", "tag1,tag2")
        self.mock_db.execute_query.side_effect = [mock_ressource, None, None]

        self.ressource_management.get_ressource_by_id = MagicMock(return_value=mock_ressource)

        # Act
        result = self.ressource_management.delete_ressource(1,1, "No longer needed")

        # Assert
        self.assertTrue(result)
        self.mock_db.execute_query.assert_called()