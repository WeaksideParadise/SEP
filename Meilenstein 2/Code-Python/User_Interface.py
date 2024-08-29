import User
import Ressource
import User_Management
import Ressource_Management
import Routes.UI_User_Routes
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import os
from dotenv import load_dotenv


class User_Interface:
    def __init__(self, um: User_Management, rm: Ressource_Management):
        load_dotenv()
        
        # -> Flask initialiseren
        self.app = Flask(__name__)
        self.app.secret_key = os.getenv('FLASK_SECRET_KEY')

        # -> Session initialiseren
        self.app.config["SESSION_TYPE"] = "sqlalchemy"
        self.app.config['SQLALCHEMY_DATABASE_URI'] = (
                                                     f'mysql+mysqlconnector://'
                                                     f'{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@'
                                                     f'{os.getenv('DB_HOST')}:3306/{os.getenv('DB_DATABASE')}'
                                                     )
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.session_db = SQLAlchemy(self.app)
        
        self.app.config['SESSION_SQLALCHEMY'] = self.session_db
        self.app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'

        Session(self.app)
        
        # -> Instanzen erstellen
        self.um = um
        self.rm = rm

        # -> Session Tabelle erstellen
        # self.create_session_table()

    def create_session_table(self):
        class SessionModel(self.session_db.Model):
            __tablename__ = 'sessions'
            id = self.session_db.Column(self.session_db.String(255), primary_key=True)
            data = self.session_db.Column(self.session_db.Text)

        with self.app.app_context():
            self.session_db.create_all()

    #def initialize_routes(self):


    #def run(self):
    #    self.app.run(debug=True)