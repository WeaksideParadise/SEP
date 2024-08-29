from flask import *

class Admin_Panel_Routes:
    def __init__(self, app):
        self.app = app

        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route("/check_links", methods = ["GET","POST"])
        def UI_login_user(self):
            if not session["is_administrator"] and not session["is_moderator"]:
                flash("Du hast keine Rechte für diese Aktion", "error")