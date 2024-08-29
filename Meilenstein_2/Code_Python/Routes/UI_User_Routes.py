from Code_Python.User_Management import User_Management
from flask import *

class User_Routes:
    def __init__(self, app, um: User_Management):
        self.app = app
        self.um = um

        self.setup_routes()

    def setup_routes(self):

        @self.app.route("/login_user", methods = ["GET","POST"])
        def UI_login_user():

            if request.method == "POST":
                username = request.form.get("username")
                password = request.form.get("password")

                try:
                    if self.um.login_user(username, password):
                        user = self.um.get_user_by_name(username)
                        print("Here")
                        session["username"] = user.name
                        session["user_id"]  = user.user_id
                        if user.is_administrator:
                            session["role"] = "administrator" 
                        elif user.is_moderator:
                            session["role"] = "moderator" 
                        else:
                            session["role"] = "user"

                        flash("Anmeldung erfoglreich", "success")
                        return redirect(url_for("UI_index"))
                    else:
                         flash("Anmeldung fehlgeschlagen. Konto existiert nicht / Falsches Passwort.", "failure")
                         return redirect(url_for("UI_login"))
                except LookupError as e:
                    flash("Bei der Anmeldung ging etwas schief, bitte erneut versuchen", "error")
                    return redirect(url_for("UI_login"))

            # Zeige das Login-Formular an (GET-Anfrage)

        @self.app.route("/logout", methods = ["GET","POST"])
        def UI_logout_user():
                
                if self.um.logout_user(session["user_id"]):
                    session["user_id"] = -1
                    session["username"]= None
                    session["role"]    = None
                    flash("Erfolgreich abgemeldet", "success")
                    return redirect(url_for("UI_index"))
                else:
                    flash("Bei der Abmeldung ging etwas schief", "error")
                    return redirect(url_for("UI_index"))

        @self.app.route("/register_user", methods = ["GET","POST"])
        def UI_register_user():
            if request.method == "POST":
                username = request.form.get("username")
                suggested_password = request.form.get("password")

            try:
                if self.um.register_user(username, suggested_password):
                    flash("Registrierung erfolgreich", "success")
                    return redirect(url_for("UI_login"))
                else:
                    flash("Registrierung fehlgeschlagen", "failure")
                    return redirect(url_for("UI_register"))
            except NameError as e:
                    flash("Benutzername ist bereits vergeben", "error")
                    return redirect(url_for("UI_register"))
            except ValueError as e:
                    flash("Passwort besteht nicht aus mindestens 4 Zeichen", "error")
                    return redirect(url_for("UI_register"))

            # Zeige das Registrierungs-Formular an (GET-Anfrage)
            