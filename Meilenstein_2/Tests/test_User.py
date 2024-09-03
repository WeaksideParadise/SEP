import unittest
from Code_Python.User_Management import User

class test_User(unittest.TestCase):

    def setUp(self):
        # Setup eine User Instanz für Tests
        self.user = User(
            user_id=1,
            is_logged_in=True,
            name="TestUser",
            hashed_password="5f4dcc3b5aa765d61d8327deb882cf99",  # MD5 Hash für 'password'
            is_administrator=True,
            is_moderator=False,
            ressource_suggestions="Vorschlag A"
        )

    def test_getters(self):
        # Testet, ob die Getter korrekt arbeiten
        self.assertEqual(self.user.user_id, 1)
        self.assertTrue(self.user.is_logged_in)
        self.assertEqual(self.user.name, "TestUser")
        self.assertEqual(self.user.hashed_password, "5f4dcc3b5aa765d61d8327deb882cf99")
        self.assertTrue(self.user.is_administrator)
        self.assertFalse(self.user.is_moderator)
        self.assertEqual(self.user.ressource_suggestions, "Vorschlag A")

    def test_setters(self):
        # Testet, ob die Setter korrekt arbeiten
        self.user.user_id = 2
        self.assertEqual(self.user.user_id, 2)

        self.user.is_logged_in = False
        self.assertFalse(self.user.is_logged_in)

        self.user.name = "NewUser"
        self.assertEqual(self.user.name, "NewUser")

        self.user.hashed_password = "098f6bcd4621d373cade4e832627b4f6"  # MD5 Hash für 'test'
        self.assertEqual(self.user.hashed_password, "098f6bcd4621d373cade4e832627b4f6")

        self.user.is_administrator = False
        self.assertFalse(self.user.is_administrator)

        self.user.is_moderator = True
        self.assertTrue(self.user.is_moderator)

        self.user.ressource_suggestions = "Vorschlag B"
        self.assertEqual(self.user.ressource_suggestions, "Vorschlag B")

    def test_name_length(self):
        # Testet, ob der Name nicht länger als 40 Zeichen ist
        with self.assertRaises(ValueError):
            self.user.name = "A" * 41  # Name mit 41 Zeichen

    def test_invalid_hashed_password(self):
        # Testet, ob ein ungültiger Hash korrekt behandelt wird
        with self.assertRaises(ValueError):
            self.user.hashed_password = "invalidhash"

    def test_invalid_user_id(self):
        # Testet, ob eine ungültige User ID korrekt behandelt wird
        with self.assertRaises(ValueError):
            self.user.user_id = -10