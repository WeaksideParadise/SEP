import Code_Python.Database 
import Code_Python.User_Management
import Code_Python.Ressource_Management
import Code_Python.Ressource_Actions
import Code_Python.User_Interface

db = Code_Python.Database.Database()
#print("Connected")

um = Code_Python.User_Management.User_Management(db)
rm = Code_Python.Ressource_Management.Ressource_Management(db, um)
ra = Code_Python.Ressource_Actions.Ressource_Actions(db, rm)

ui = Code_Python.User_Interface.User_Interface(um, ra, db)
ui.run()
