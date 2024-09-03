import unittest
from Code_Python.Ressource import Ressource

class test_Ressource(unittest.TestCase):
    
    def setUp(self):
        # Setup eine Ressource Instanz für Tests
        self.ressource = Ressource(
            ressource_id=1,
            name="Test Ressource",
            is_published=True,
            description="Eine Testbeschreibung",
            link="https://example.com",
            created_by="user#1",
            faculty="Informatik",
            ressource_type="Buch",
            opening_hours="Mo-Fr 9-17",
            likes=[1, 2, 3],
            experience_reports="Sehr gut",
            ressource_tags=["Test", "Buch"]
        )

    def test_getters(self):
        # Testet, ob die Getter korrekt arbeiten
        self.assertEqual(self.ressource.ressource_id, 1)
        self.assertEqual(self.ressource.name, "Test Ressource")
        self.assertEqual(self.ressource.is_published, True)
        self.assertEqual(self.ressource.description, "Eine Testbeschreibung")
        self.assertEqual(self.ressource.link, "https://example.com")
        self.assertEqual(self.ressource.created_by, "user#1")
        self.assertEqual(self.ressource.faculty, "Informatik")
        self.assertEqual(self.ressource.ressource_type, "Buch")
        self.assertEqual(self.ressource.opening_hours, "Mo-Fr 9-17")
        self.assertEqual(self.ressource.likes, [1, 2, 3])
        self.assertEqual(self.ressource.experience_reports, "Sehr gut")
        self.assertEqual(self.ressource.ressource_tags, ["Test", "Buch"])

    def test_setters(self):
        # Testet, ob die Setter korrekt arbeiten
        self.ressource.name = "Neue Ressource"
        self.assertEqual(self.ressource.name, "Neue Ressource")

        self.ressource.is_published = False
        self.assertEqual(self.ressource.is_published, False)

        self.ressource.description = "Neue Beschreibung"
        self.assertEqual(self.ressource.description, "Neue Beschreibung")

        self.ressource.link = "https://newexample.com"
        self.assertEqual(self.ressource.link, "https://newexample.com")

        self.ressource.created_by = "admin#2"
        self.assertEqual(self.ressource.created_by, "admin#2")

        self.ressource.faculty = "Mathematik"
        self.assertEqual(self.ressource.faculty, "Mathematik")

        self.ressource.ressource_type = "Artikel"
        self.assertEqual(self.ressource.ressource_type, "Artikel")

        self.ressource.opening_hours = "Mo-Fr 10-18"
        self.assertEqual(self.ressource.opening_hours, "Mo-Fr 10-18")

        self.ressource.likes = [4, 5]
        self.assertEqual(self.ressource.likes, [4, 5])

        self.ressource.experience_reports = "Gut"
        self.assertEqual(self.ressource.experience_reports, "Gut")

        self.ressource.ressource_tags = ["Neu", "Artikel"]
        self.assertEqual(self.ressource.ressource_tags, ["Neu", "Artikel"])

    def test_invalid_link(self):
        # Testet, ob ein ungültiger Link korrekt gesetzt wird
        with self.assertRaises(ValueError):
            self.ressource.link = None
