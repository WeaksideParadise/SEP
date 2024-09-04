import unittest
from unittest.mock import patch, MagicMock
from mysql.connector import Error
from Code_Python.Database import Database
class test_Database(unittest.TestCase):
#chatgpt tests für getter und setter
    @patch('mysql.connector.connect')
    def test_connect_success(self, mock_connect):
        # Arrange
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.is_connected.return_value = True

        # Act
        db = Database()
        connection = db._connect()

        # Assert
        self.assertIsNotNone(connection)
        mock_connect.assert_called_once_with(**db.config)
        self.assertTrue(mock_connection.is_connected.called)

    @patch('mysql.connector.connect')
    def test_connect_failure(self, mock_connect):
        # Arrange
        mock_connect.side_effect = Error("Connection failed")

        # Act
        db = Database()
        connection = db._connect()

        # Assert
        self.assertIsNone(connection)
        mock_connect.assert_called_once_with(**db.config)

    @patch('mysql.connector.connect')
    def test_execute_query_success(self, mock_connect):
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.is_connected.return_value = True
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [{"col1": "value1"}]
        query = "SELECT * FROM table WHERE id = %s"
        params = (1,)

        # Act
        db = Database()
        result = db.execute_query(query, params)

        # Assert
        self.assertEqual(result, [{"col1": "value1"}])
        mock_connect.assert_called_once_with(**db.config)
        mock_cursor.execute.assert_called_once_with(query, params)
        mock_cursor.fetchall.assert_called_once()
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('mysql.connector.connect')
    def test_execute_query_failure(self, mock_connect):
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.is_connected.return_value = True
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Error("Query failed")
        query = "SELECT * FROM table WHERE id = %s"
