import Database
import User_Management
import Ressource_Management
import User_Interface

db = Database.Database()
db._connect()
#print("Connected")

um = User_Management.User_Management(db)
rm = Ressource_Management.Ressource_Management(db, um)

test = User_Interface.User_Interface(um, rm)