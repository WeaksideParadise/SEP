from flask import *

class Navigation_Bar_Routes:
    def __init__(self, app):
        self.app = app

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
            return render_template("search.html")
        
        @self.app.route("/add_res" ,methods = ["GET","POST"])
        def UI_add_res():
            if not session["role"]:
                flash("Melden Sie sich an, um diese Funktion zu nutzen!", "error")
                return redirect(url_for("UI_search"))
            else:
                return render_template("add_res.html")
            
        @self.app.route("/admin" ,methods = ["GET","POST"])
        def UI_admin_panel():
            if not session["role"] == "administator" and not session["role"] == "moderator":
                flash("Sie haben keine Rechte hierfür!", "error")
                return redirect(url_for("UI_index"))
            else:
                return render_template("admin_panel.html")