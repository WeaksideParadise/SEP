from flask import *

class Admin_Panel_Routes:
    def __init__(self, app):
        self.app = app

        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route("/checklinks", methods = ["GET","POST"])
        def UI_check_links(self):
            if not session["is_administrator"] and not session["is_moderator"]:
                flash("Du hast keine Rechte für diese Aktion", "error")