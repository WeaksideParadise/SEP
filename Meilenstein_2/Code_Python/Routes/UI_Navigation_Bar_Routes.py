from Code_Python.Ressource_Actions import Ressource_Actions
from Code_Python.User_Management   import User_Management
from flask import *

class Navigation_Bar_Routes:
    def __init__(self, app, um: User_Management, ra: Ressource_Actions ):
        self.app = app
        self.um = um
        self.ra = ra

        self.setup_routes()
   
    def setup_routes(self):
        
        @self.app.route("/", methods = ["GET","POST"])
        def UI_index():
            return render_template("index.html")
        
        @self.app.route("/login", methods = ["GET","POST"])
        def UI_login():
            return render_template("login.html")
        
        @self.app.route("/register", methods = ["GET","POST"])
        def UI_register():
            return render_template("register.html")
        
        @self.app.route("/search", methods = ["GET","POST"])
        def UI_search():
            return redirect(url_for("UI_search_ressource"))
            
        @self.app.route("/admin" ,methods = ["GET","POST"])
        def UI_admin_panel():
            if not session["role"] == "administrator" and not session["role"] == "moderator":
                flash("Sie haben keine Rechte hierfür!", "error")
                return redirect(url_for("UI_index"))
            else:
                
                try:
                    users = self.um.get_users_by_query("SELECT * FROM users")
                except LookupError as e:
                    flash("Beim Laden der Nutzer ist ein Fehler aufgetreten", "error")
                    return redirect(url_for("UI_index"))
                
                try:
                    resources = self.ra.ressource_management.get_ressources_by_query("SELECT * FROM ressources",[])
                except LookupError as e:
                    flash("Beim Laden der Ressourcen ist ein Fehler aufgetreten", "error")
                    return redirect(url_for("UI_index"))
                
                try:
                    _invalid_link_reports = self.ra.fetch_invalid_link_reports()
                except LookupError as e:
                    flash("Beim Laden der Ressourcenmeldungen ist ein Fehler aufgetreten", "error")
                    return redirect(url_for("UI_index"))
                
                return render_template("admin.html", users=users, resources=resources, reports=_invalid_link_reports)
            
        @self.app.route("/admin2" ,methods = ["GET","POST"])
        def UI_admin_panel_2():
            if not session["role"] == "administrator" and not session["role"] == "moderator":
                flash("Sie haben keine Rechte hierfür!", "error")
                return redirect(url_for("UI_index"))
            else:
                
                try:
                    deleted_ressources = self.ra.fetch_deleted_ressources()
                except LookupError as e:
                    flash("Beim Laden der Nutzer ist ein Fehler aufgetreten", "error")
                    return redirect(url_for("UI_index"))
                
                try:
                    reports = self.ra.fetch_ressource_reports()
                except LookupError as e:
                    flash("Beim Laden der Ressourcen ist ein Fehler aufgetreten", "error")
                    return redirect(url_for("UI_index"))
            
                
                return render_template("admin2.html", deleted_ressources=deleted_ressources, reports=reports)