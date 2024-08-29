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
