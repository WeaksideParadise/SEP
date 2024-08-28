import Database
import User_Management
import Ressource_Management

db = Database.Database()
db._connect()
print("Connected")

um = User_Management.User_Management(db)
rs = Ressource_Management.Ressource_Management(db, um)

print(um.promote_user_to_Admin(1))
print(rs.add_ressource(1, "Test_Ressource", "bliblablub", "www.wikipedia.com", "Fakultät", "Video", "X#"))
print(rs.get_ressource_by_id(1).name)