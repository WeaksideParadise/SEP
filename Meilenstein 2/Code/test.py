import Database
import User_Management
import Ressource_Management

db = Database.Database()
db._connect()
print("Connected")

um = User_Management.User_Management(db)
r = Ressource_Management.Ressource_Management(db, um)

