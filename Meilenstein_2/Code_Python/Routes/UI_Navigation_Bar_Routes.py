from Code_Python.Ressource_Actions import Ressource_Actions
from Code_Python.User_Management   import User_Management
from flask import *
import os
import subprocess

class Navigation_Bar_Routes:
    def __init__(self, app, um: User_Management, ra: Ressource_Actions ):
        self.app = app
        self.um = um
        self.ra = ra

        self.setup_routes()
   
    def setup_routes(self):
        
        @self.app.route("/", methods = ["GET","POST"])
        def UI_index():
            most_liked_ressources = self.ra.fetch_most_liked_ressources()
            likes = self.ra.list_likes(most_liked_ressources)
            is_liked = self.ra.is_liked_by_user(int(session["user_id"]), most_liked_ressources)
            amount_suggestions = len(self.ra.fetch_suggestions(session["user_id"]))
            
            return render_template("index.html", most_liked_ressources = most_liked_ressources, likes = likes, is_liked = is_liked, amount_suggestions = amount_suggestions)
        
        @self.app.route("/login", methods = ["GET","POST"])
        def UI_login():
            return render_template("login.html")

        @self.app.route("/docs", methods = ["GET","POST"])
        def UI_docs():
            file_path = __file__

            # Split the path into components
            path_parts = file_path.split('\\')  # Use '\\' for Windows paths

            # Remove the last two folders
            new_path_parts = path_parts[:-4]  # Keep all except the last two parts

            # Join the parts back into a path
            new_path = '\\'.join(new_path_parts)

            # If the original path had a trailing separator, add it back
            if file_path.endswith('\\'):
                new_path += '\\'

            new_path += r"/Meilenstein_3/docs/_build/index.html"

            subprocess.run(['start', new_path], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            return redirect("/") #idealer wäre hier die vorher geöffnete seite wieder zu öffnen
        
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
                    users = self.um.sort_users_by_role(users)
                except LookupError as e:
                    flash("Beim Laden der Nutzer ist ein Fehler aufgetreten", "error")
                    return redirect(url_for("UI_index"))
                
                try:
                    resources = self.ra.ressource_management.get_ressources_by_query("SELECT * FROM ressources",[])
                except LookupError as e:
                    flash("Beim Laden der Ressourcen ist ein Fehler aufgetreten", "error")
                    return redirect(url_for("UI_index"))
                
    
                
                return render_template("admin.html", users=users, resources=resources)
            
        @self.app.route("/admin2" ,methods = ["GET","POST"])
        def UI_admin_panel_2():
            if not session["role"] == "administrator" and not session["role"] == "moderator":
                flash("Sie haben keine Rechte hierfür!", "error")
                return redirect(url_for("UI_index"))
            else:
                
                try:
                    deleted_ressources = self.ra.fetch_deleted_ressources()
                    deleted_ressources.reverse()
                except LookupError as e:
                    flash("Beim Laden der Nutzer ist ein Fehler aufgetreten", "error")
                    return redirect(url_for("UI_index"))
                
                try:
                    reports = self.ra.fetch_ressource_reports()
                    reports.reverse()
                except LookupError as e:
                    flash("Beim Laden der Ressourcen ist ein Fehler aufgetreten", "error")
                    return redirect(url_for("UI_index"))
                
                try:
                    invalid_link_reports = self.ra.fetch_invalid_link_reports()
                    invalid_link_reports.reverse()
                except LookupError as e:
                    flash("Beim Laden der Ressourcenmeldungen ist ein Fehler aufgetreten", "error")
                    return redirect(url_for("UI_index"))
            
                
                return render_template("admin2.html", deleted_ressources=deleted_ressources, reports=reports, invalid_link_reports=invalid_link_reports)