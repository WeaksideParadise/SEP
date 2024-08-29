from Code_Python.User_Management      import User_Management
from Code_Python.Ressource_Actions    import Ressource_Actions
from flask import *

class Search_Routes:
    def __init__(self, app, um: User_Management, ra: Ressource_Actions):
        self.app = app
        self.um = um
        self.ra = ra

        self.setup_routes()

    def setup_routes(self):

        @self.app.route("/search_ressource", methods = ["GET","POST"])
        def UI_search_ressource():
            
            if request.method == "POST":
                search_query   = request.form.get("search_query")
                ressource_type = request.form.get("ressource_type")
                if ressource_type == "all":
                    ressource_type = None
                faculty        = request.form.get("faculty")
                if faculty == "all":
                    faculty = None
            
                try:
                    results = self.ra.search_ressources(search_query, ressource_type, faculty)
                    flash(f"Es wurden {len(results)} Ergebnisse gefunden", "success")
                    return render_template("search_results.html", results=results)
                except LookupError as e:
                    flash("Bei der Suche ging etwas schief, bitte erneut versuchen", "error")
                    return redirect(url_for("UI_search"))
            flash("Fehler", "error")
            return redirect(url_for("UI_search"))