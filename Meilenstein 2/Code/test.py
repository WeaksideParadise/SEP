import Database
import User_Management

db = Database.Database()
db._connect()
print("Connected")

um = User_Management.User_Management(db)