import Database

db = Database.Database()
db.execute_query("""CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY)""")
print("GOOD")