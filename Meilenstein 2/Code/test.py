import Database
import User_Management
import Ressource_Management

db = Database.Database()
db._connect()
print("Connected")

um = User_Management.User_Management(db)
rs = Ressource_Management.Ressource_Management(db, um)

ressources = rs.search_ressources("Ressource", "Bericht", "X")
for ressource in ressources:
    print(ressource.ressource_id)

print(rs.add_experience_report(4, "Meine Erfahrung2"))