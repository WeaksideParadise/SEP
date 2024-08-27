import Database
import User_Management

db = Database.Database()
db._connect()
print("Hi")
um = User_Management.User_Management(db)
user = um.get_user_by_id(1)
print(user.name)
print(user.is_administrator)
x: bool = 0