from Code_Python.Ressource_Actions import Ressource_Actions
from Code_Python.User_Management   import User_Management
from flask import *

class Admin_Panel_Routes:
    def __init__(self, app, um: User_Management, ra: Ressource_Actions ):
        self.app = app
        self.um = um
        self.ra = ra

        self.setup_routes()
    
    def setup_routes(self):
        
        @self.app.route("/check_links", methods = ["POST"])
        def UI_check_links():
            if not session["role"] == "administrator" and not session["role"] == "moderator":
                flash("Du hast keine Rechte für diese Aktion", "error")
        
        @self.app.route("/promote_user", methods = ["POST"])
        def UI_promote_user():
            if not session["role"] == "administrator":
                flash("Du hast keine Rechte für diese Aktion", "error")
                return redirect(url_for("UI_index"))
            
            if not self.um.promote_user_to_Admin(request.args.get("user_id")):
                flash("Fehler beim Ausführen der Aktion", "error")
                return redirect(url_for("UI_admin_panel"))
            
            flash(f"Nutzer {request.args.get('user_id')} wurde auf Moderator befördert", "success")
            return redirect(url_for("UI_admin_panel"))
        
        @self.app.route("/demote_user", methods = ["GET","POST"])
        def UI_demote_user():
            if not session["role"] == "administrator":
                flash("Du hast keine Rechte für diese Aktion", "error")
                return redirect(url_for("UI_index"))
            
            if not self.um.demote_user(request.args.get("user_id")):
                flash("Fehler beim Ausführen der Aktion", "error")
                return redirect(url_for("UI_admin_panel"))
            
            #Nutzer zwangsweise ausloggen
            if not self.um.logout_user(request.args.get("user_id")):
                flash("Fehler beim Ausführen der Aktion", "error")
                return redirect(url_for("UI_admin_panel"))
            
            flash(f"Nutzer {request.args.get('user_id')} wurde auf degradiert", "success")
            return redirect(url_for("UI_admin_panel"))

            

        @self.app.route("/delete_user", methods = ["GET","POST"])
        def UI_delete_user():
            if not session["role"] == "administrator":
                flash("Du hast keine Rechte für diese Aktion", "error")
                return redirect(url_for("UI_index"))
            
            if not self.um.delete_user(request.args.get("user_id")):
                flash("Fehler beim Ausführen der Aktion", "error")
                return redirect(url_for("UI_admin_panel"))
            
            flash(f"Nutzer {request.args.get('user_id')} wurde gelöscht", "success")
            return redirect(url_for("UI_admin_panel"))
        
        @self.app.route("/change_ressource", methods = ["GET","POST"])
        def UI_change_ressource():
            if not session["role"] == "administrator":
                flash("Du hast keine Rechte für diese Aktion", "error")
                return redirect(url_for("UI_index"))
            
            # TODO

            flash(f"Ressource {request.args.get('ressource_id')} wurde geändert", "success")
            return redirect(url_for("UI_admin_panel"))
        
        @self.app.route("/delete_ressource", methods = ["GET","POST"])
        def UI_delete_ressource():
            if not session["role"] == "administrator":
                flash("Du hast keine Rechte für diese Aktion", "error")
                return redirect(url_for("UI_index"))
            
            if not self.ra.ressource_management.delete_ressource(request.args.get("ressource_id"), "Test"):
                flash("Fehler beim Ausführen der Aktion", "error")
                return redirect(url_for("UI_admin_panel"))
            
            flash(f"Ressource {request.args.get('ressource_id')} wurde gelöscht", "success")
            return redirect(url_for("UI_admin_panel"))