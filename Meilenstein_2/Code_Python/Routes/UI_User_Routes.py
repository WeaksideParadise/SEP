from Code_Python.User_Management import User_Management
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
                        user = User_Management.get_user_by_name(username).user_id
                        
                        session["username"] = username
                        session["user_id"]  = user.user_id
                        if user.is_administrator:
                            session["role"] = "administrator" 
                        elif user.is_moderator:
                            session["role"] = "moderator" 
                        else:
                            session["role"] = "user"

                        flash("Anmeldung erfoglreich", "success")
                        return #redirect(url_for(index_user))
                    else:
                         flash("Anmeldung fehlgeschlagen. Konto existiert nicht / Falsches Passwort.", "failure")
                         return #redirect(url_for(login))
                except LookupError as e:
                    flash("Bei der Anmeldung ging etwas schief, bitte erneut versuchen", "error")

            # Zeige das Login-Formular an (GET-Anfrage)

        @self.app.route("/logout", methods = ["GET","POST"])
        def UI_loggout_user():
                
                if User_Management.logout_user(session["user_id"]):
                    session["user_id"] = -1
                    session["username"]= None
                    session["role"]    = None
                    flash("Erfolgreich abgemeldet", "success")
                    return redirect(url_for("index"))
                else:
                    flash("Bei der Abmledung ging etwas schief", "error")
                    return

        @self.app.route("/register", methods = ["GET","POST"])
        def UI_register_user():
            if request.method == "POST":
                username = request.form.get("username")
                suggested_password = request.form.get("password")

            try:
                if User_Management.register_user(username, suggested_password):
                    flash("Registrierung erfolgreich", "success")
                    return redirect(url_for("UI_login_user"))
                else:
                    flash("Registrierung fehlgeschlagen", "failure")
                    return
            except NameError as e:
                    flash("Benutzername ist bereits vergeben", "error")
            except ValueError as e:
                    flash("Passwort besteht nicht aus mindestens 4 Zeichen", "error")

            # Zeige das Registrierungs-Formular an (GET-Anfrage)
            