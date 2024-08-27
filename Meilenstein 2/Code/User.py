class User:
    def __init__(self, user_id: int, is_logged_in: bool, name: str, hashed_password: str, is_administrator: bool, is_moderator: bool):
        self.user_id = user_id                      # Primärschlüssel
        self.is_logged_in = is_logged_in    
        self.name = name                            # Maximale Länge = 40 Zeichen
        self.hashed_password = hashed_password      # MD5 Hash
        self.is_administrator = is_administrator    
        self.is_moderator = is_moderator            # Bonus

#TODO: Getter und Setter 