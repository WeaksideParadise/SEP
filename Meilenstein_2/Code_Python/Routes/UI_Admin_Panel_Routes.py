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
                return redirect(url_for("UI_index"))
            
            if self.ra.check_links():
                flash("Links erfolgreich überprüft", "success")
                return redirect(url_for("UI_admin_panel"))
            
            flash("Fehler beim Überprüfen der Links", "error")
            return redirect(url_for("UI_admin_panel"))
        
        @self.app.route("/promote_user", methods = ["POST"])
        def UI_promote_user():
            if not session["role"] == "administrator":
                flash("Du hast keine Rechte für diese Aktion", "error")
                return redirect(url_for("UI_admin_panel"))
            
            if not self.um.promote_user_to_Moderator(int(request.args.get("user_id"))):
                flash("Fehler beim Ausführen der Aktion", "error")
                return redirect(url_for("UI_admin_panel"))
            
            flash(f"Nutzer {request.args.get('user_id')} wurde auf Moderator befördert", "success")
            return redirect(url_for("UI_admin_panel"))
        
        @self.app.route("/demote_user", methods = ["GET","POST"])
        def UI_demote_user():
            if not session["role"] == "administrator":
                flash("Du hast keine Rechte für diese Aktion", "error")
                return redirect(url_for("UI_admin_panel"))
            
            if not self.um.demote_user(int(request.args.get("user_id"))):
                flash("Fehler beim Ausführen der Aktion", "error")
                return redirect(url_for("UI_admin_panel"))
            
            #Nutzer zwangsweise ausloggen
            if not self.um.logout_user(int(request.args.get("user_id"))):
                flash("Fehler beim Ausführen der Aktion", "error")
                return redirect(url_for("UI_admin_panel"))
            
            flash(f"Nutzer {request.args.get('user_id')} wurde degradiert", "success")
            return redirect(url_for("UI_admin_panel"))

            

        @self.app.route("/delete_user", methods = ["GET","POST"])
        def UI_delete_user():
            if not session["role"] == "administrator":
                flash("Du hast keine Rechte für diese Aktion", "error")
                return redirect(url_for("UI_admin_panel"))
            
            try:
                if not self.um.delete_user(request.args.get("user_id")):
                    flash("Fehler beim Ausführen der Aktion", "error")
                    return redirect(url_for("UI_admin_panel"))
            except ValueError as e:
                flash("Sie können keine Administratoren löschen")
                return redirect(url_for("UI_admin_panel"))
            
            flash(f"Nutzer {request.args.get('user_id')} wurde gelöscht", "success")
            return redirect(url_for("UI_admin_panel"))
        
        @self.app.route("/change_ressource", methods = ["POST"])
        def UI_change_ressource():
            if not session["role"] in ["administrator","moderator"]:
                flash("Du hast keine Rechte für diese Aktion", "error")
                return redirect(url_for("UI_index"))
            
            ressource_id           = request.form.get("ressource_id")
            ressource_is_published = int(request.form.get("hidden_is_published"))
            ressource_name         = request.form.get("name")
            ressource_description  = request.form.get("description")
            ressource_link         = request.form.get("link")
            ressource_opening_hours= request.form.get("opening_hours")
            ressource_faculty      = request.form.get("faculty")
            ressource_type         = request.form.get("ressource_type")

            if ressource_is_published:
                is_published = True
            else:
                is_published = False

            if not self.ra.ressource_management.change_ressource(int(ressource_id), name=ressource_name, description=ressource_description, link=ressource_link, opening_hours=ressource_opening_hours, faculty=ressource_faculty, ressource_type=ressource_type, is_published=is_published):
                flash("Fehler beim Ändern der Ressource")
                return redirect(url_for("UI_admin_panel"))
            
            flash(f"Ressource {ressource_id} wurde geändert", "success")
            return redirect(url_for("UI_admin_panel"))
        
        @self.app.route("/delete_ressource", methods = ["GET","POST"])
        def UI_delete_ressource():
            if not session["role"] in ["administrator","moderator"]:
                flash("Du hast keine Rechte für diese Aktion", "error")
                return redirect(url_for("UI_index"))
            
            if not self.ra.ressource_management.delete_ressource(request.args.get("ressource_id"), int(session["user_id"]), request.form.get("reason")):
                flash("Fehler beim Ausführen der Aktion", "error")
                return redirect(url_for("UI_admin_panel"))
            
            flash(f"Ressource {request.args.get('ressource_id')} wurde gelöscht", "success")
            return redirect(url_for("UI_admin_panel"))
        
        @self.app.route("/publish_ressource", methods = ["GET","POST"])
        def UI_publish_ressource():
            if not session["role"] in ["administrator","moderator"] :
                flash("Du hast keine Rechte für diese Aktion", "error")
                return redirect(url_for("UI_index"))
            
            if not self.ra.publish_ressource(int(request.args.get("ressource_id"))):
                flash("Fehler beim Veröffentlichen der Ressource")
                return redirect(url_for("UI_admin_panel"))

            flash(f"Ressource {request.args.get('ressource_id')} wurde veröffentlicht", "success")
            return redirect(url_for("UI_admin_panel"))
        
        @self.app.route("/delete_report", methods = ["POST"])
        def UI_delete_report():
            if not session["role"] in ["administrator","moderator"] :
                flash("Du hast keine Rechte für diese Aktion", "error")
                return redirect(url_for("UI_index"))
            
            if not self.ra.delete_report(int(request.args.get("report_id"))):
                flash("Fehler beim Löschen der Meldung")
                return redirect(url_for("UI_admin_panel_2"))

            flash(f"Meldung {request.args.get('report_id')} wurde geschlossen", "success")
            return redirect(url_for("UI_admin_panel_2"))
        
        @self.app.route("/revive_ressource", methods = ["POST"])
        def UI_revive_ressource():
            if not session["role"] == "administrator" :
                flash("Du hast keine Rechte für diese Aktion", "error")
                return redirect(url_for("UI_admin_panel_2"))
            
            if not self.ra.revive_ressource(int(request.args.get("ressource_id"))):
                flash("Fehler beim Wiederherstellen der Meldung")
                return redirect(url_for("UI_admin_panel_2"))

            flash(f"Ressource {request.args.get('ressource_id')} wurde wiederhergestellt", "success")
            return redirect(url_for("UI_admin_panel_2"))