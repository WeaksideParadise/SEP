from Code_Python.Database import Database
from Code_Python.User_Management import User_Management
from Code_Python.Ressource_Actions import Ressource_Actions
from Code_Python.Routes import UI_Navigation_Bar_Routes
from Code_Python.Routes import UI_User_Routes
from Code_Python.Routes import UI_Admin_Panel_Routes
from Code_Python.Routes import UI_Ressource_Routes
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import os
from dotenv import load_dotenv


class User_Interface:
    """
    Diese Klasse stellt das Benutzerinterface der Anwendung bereit, das auf Flask basiert.
    Es werden Routen initialisiert, Sessions verwaltet und verschiedene Instanzen erstellt.
    """
    
    def __init__(self, um: User_Management, ra: Ressource_Actions, db: Database):
        """
        Initialisiert das User Interface, konfiguriert Flask, setzt Session-Management auf
        und initialisiert die notwendigen Routen.

        Args:
            um (User_Management): Instanz des User-Managements zur Verwaltung von Benutzern.
            ra (Ressource_Actions): Instanz zum Verwalten von Ressourcenvorgängen.
            db (Database): Datenbank-Instanz für die Kommunikation mit der Datenbank.
        """
        load_dotenv()
        
        # -> Flask initialisieren
        self.app = Flask(__name__, static_folder='../static', template_folder='../templates')
        self.app.secret_key = os.getenv('FLASK_SECRET_KEY')

        # -> Session initialisieren
        self.app.config["SESSION_TYPE"] = "sqlalchemy"
        self.app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"mysql+mysqlconnector://"
            f"{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:3306/{os.getenv('DB_DATABASE')}"
        )
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.session_db = SQLAlchemy(self.app)
        
        self.app.config['SESSION_SQLALCHEMY'] = self.session_db
        self.app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'

        Session(self.app)
        
        # -> Instanzen erstellen
        self.um = um
        self.ra = ra
        self.db = db

        # -> Session-Tabelle erstellen (optional, auskommentiert)
        # self.create_session_table()

        # -> Routen initialisieren
        self.initialize_routes()

    def create_session_table(self):
        """
        Erstellt die Tabelle für die Sessions in der Datenbank, falls diese nicht existiert.

        Innerhalb der Flask-App wird eine SessionModel-Klasse definiert,
        die für die Speicherung der Sitzungen in der SQLAlchemy-Datenbank verantwortlich ist.
        """

        class SessionModel(self.session_db.Model):
            __tablename__ = 'sessions'
            id = self.session_db.Column(self.session_db.String(255), primary_key=True)
            data = self.session_db.Column(self.session_db.Text)

        with self.app.app_context():
            self.session_db.create_all()

    def initialize_routes(self):
        """
        Initialisiert alle notwendigen Routen für die Webanwendung.
        
        Bindet die verschiedenen Route-Klassen an die Flask-Applikation,
        um Benutzer-, Admin- und Ressourcenseiten zu verwalten.
        """
        UI_User_Routes.User_Routes(self.app, self.um)
        UI_Admin_Panel_Routes.Admin_Panel_Routes(self.app, self.um, self.ra)
        UI_Navigation_Bar_Routes.Navigation_Bar_Routes(self.app, self.um, self.ra)
        UI_Ressource_Routes.Ressource_Routes(self.app, self.um, self.ra)

    def run(self):
        """
        Startet den Flask-Webserver im Debug-Modus.
        
        Diese Methode wird aufgerufen, um die Flask-Applikation lokal oder auf einem Server
        laufen zu lassen. Debug-Informationen werden in der Konsole ausgegeben.
        """
        self.app.run(debug=True)
