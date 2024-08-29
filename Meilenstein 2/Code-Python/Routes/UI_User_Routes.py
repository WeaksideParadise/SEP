import User
import Ressource
import User_Management
import Ressource_Management
from flask import *

class User_Routes:
    def __init__(self, app):
        self.app = app

        self.setup_routes()

    def setup_routes(self):

        @self.app.route("/login", methods = ["GET","POST"])
        def UI_login_user():
            if request.method == "POST":
                username = request.form.get("username")
                password = request.form.get("password")

                try:
                    if User_Management.login_user(username, password):
                        flash("Anmeldung erfoglreich", "success")
                        return
                    else:
                         flash("Anmeldung fehlgeschlagen. Konto existiert nicht / Falsches Passwort.", "failure")
                         return
                except LookupError as e:
                    flash("Bei der Anmeldung ging etwas schief, bitte erneut versuchen", "error")

            # Zeige das Login-Formular an (GET-Anfrage)

        @self.app.route("/register", methods = ["GET","POST"])
        def UI_register_user():
            if request.method == "Post":
                username = request.form.get("username")
                suggested_password = request.form.get("password")

            try:
                if User_Management.register_user(username, suggested_password):
                    flash("Registrierung erfolgreich", "success")
                    return
                else:
                    flash("Registrierung fehlgeschlagen", "failure")
                    return
            except NameError as e:
                    flash("Benutzername ist bereits vergeben", "error")
            except ValueError as e:
                    flash("Passwort besteht nicht aus mindestens 4 Zeichen", "error")

            # Zeige das Registrierungs-Formular an (GET-Anfrage)
            