from Code_Python.Ressource            import Ressource                
from Code_Python.User_Management      import User_Management
from Code_Python.Ressource_Actions    import Ressource_Actions
from flask import *
import math

class Ressource_Routes:
    def __init__(self, app, um: User_Management, ra: Ressource_Actions):
        self.app = app
        self.um = um
        self.ra = ra

        self.setup_routes()

    def setup_routes(self):

        @self.app.route("/search_ressource", methods = ["GET","POST"])
        def UI_search_ressource():
            
            results = []
            is_random = True
            page = 1
            search_query = ""
            faculty = ""
            ressource_type = ""
            
            if request.method == "POST":
                is_random = False
                search_query   = request.form.get("search_query", "")
                ressource_type = request.form.get("ressource_type")
                faculty        = request.form.get("faculty")
                page           = int(request.form.get("page", 1))
                if search_query == None:
                    search_query = ""
                if ressource_type == "all":
                    ressource_type = None
                if faculty == "all":
                    faculty = None
            
            if not is_random:
                try:
                    results = self.ra.search_ressources(search_query, ressource_type, faculty)
                except LookupError as e:
                    flash("Bei der Suche ging etwas schief, bitte erneut versuchen", "error")
                    return redirect(url_for("UI_search"))

            else:
                try:
                    results = self.ra.fetch_5_random_ressources()
                except LookupError as e:
                    flash("Bei der Suche ging etwas schief, bitte erneut versuchen", "error")
                    return redirect(url_for("UI_search"))
                
            ressources_per_page = 5
            total_pages = math.ceil((len(results) / ressources_per_page))
            paged_ressources = results[(page-1)*ressources_per_page:page*ressources_per_page]

            if not is_random and page == 1:
                flash(f"Es wurden {len(results)} Ergebnisse gefunden", "success")    
            
            return render_template("search.html", results=paged_ressources, page=page, total_pages=total_pages, searched_query=search_query, searched_faculty=faculty, searched_type=ressource_type)
        
        @self.app.route("/inspect_ressource", methods = ["POST"])
        def UI_inspect_ressource():
            if request.method == "POST":
                
                data = request.get_json()
                
                if not data:
                    flash("Ein Fehler ist aufgetreten", "error")
                    return redirect(url_for("UI_search"))
                
                ressource_id = data.get('ressource_id')

                ressource = self.ra.inspect_ressource(int(ressource_id))

                if ressource:
                    # Rechte-Logik
                    has_rights = False
                    if session["role"] in ["administrator", "moderator"]:
                        has_rights = True

                    # is_published-Logik
                    if not ressource[0].is_published and not has_rights:
                        flash("Diese Ressource ist noch nicht öffentlich zugänglich", "error")
                        return redirect(url_for("UI_search"))


                    # Like-Logik
                    is_liked = False
                    user_id = session["user_id"]
                    likes = ressource[0].likes.split("#")

                    if user_id in likes:
                        is_liked = True

                    return jsonify({"ressource_name":           ressource[0].name,
                                    "ressource_description":    ressource[0].description,
                                    "ressource_link":           ressource[0].link,
                                    "ressource_created_by":     ressource[0].created_by,
                                    "ressource_faculty":        ressource[0].faculty,
                                    "ressource_ressource_type": ressource[0].ressource_type,
                                    "ressource_likes":          len(ressource[0].likes)-1,
                                    "ressource_opening_hours":  ressource[0].opening_hours,
                                    "ressource_is_published":   ressource[0].is_published,
                                    "has_rights":               has_rights,
                                    "ressource_is_liked":       is_liked})
                
                
            flash("Ein Fehler ist aufgetreten", "error")
            return redirect(url_for("UI_search"))
            
        @self.app.route("/report_ressource", methods = ["GET","POST"])
        def UI_report_ressource():
            user_id = session["user_id"]
            if request.method == "POST":
                ressource_id = request.form.get("ressource_id")
                reason       = request.form.get("report_reason")

                if self.ra.report_ressource(ressource_id, user_id, reason):
                    flash(f"Ressource mit ID: {ressource_id} erfolgreich gemeldet")
                    return redirect(url_for("UI_search"))

            flash("Es ist ein Fehler aufgetreten", "error")
            return redirect(url_for("UI_search"))
            
        
        @self.app.route("/add_ressource", methods = ["GET","POST"])
        def UI_add_ressource():
            user_id = session["user_id"]
            if request.method == "POST":
                name            = request.form.get("ressource_name")
                description     = request.form.get("ressource_description")
                ressource_type  = request.form.get("ressource_type")
                link            = request.form.get("ressource_link")
                faculty         = request.form.get("ressource_faculty")
                ressource_type  = request.form.get("ressource_type")
                opening_hours   = request.form.get("ressource_opening_hours")

                
                if self.ra.ressource_management.add_ressource(user_id, name, description, link, faculty, ressource_type, opening_hours):
                    flash("Ressource erfolgreich angelegt", "success")
                    return redirect(url_for("UI_search"))

            flash("Es ist ein Fehler aufgetreten", "error")
            return redirect(url_for("UI_add_res"))
        
        @self.app.route("/like_ressource", methods = ["POST"])
        def UI_like_ressource():
            user_id = session["user_id"]
            
            if request.method == "POST":
                data = request.get_json()
                if not data:
                    flash("Beim Liken der Ressource ist ein Fehler aufgetreten", "error")
                    return redirect(url_for("UI_search"))

                ressource_id = request.form.get("ressource_id")

                
                if self.ra.like_ressource(ressource_id, user_id):
                    return jsonify({"status": 1})

            flash("Es ist ein Fehler aufgetreten", "error")
            return redirect(url_for("UI_add_res"))