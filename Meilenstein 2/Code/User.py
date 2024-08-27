class User:
    def __init__(self, user_id: int, is_logged_in: bool, name: str, hashed_password: str, is_administrator: bool, is_moderator: bool):
        self.user_id = user_id                      # Primärschlüssel
        self.is_logged_in = is_logged_in    
        self.name = name                            # Maximale Länge = 40 Zeichen
        self.hashed_password = hashed_password      # MD5 Hash
        self.is_administrator = is_administrator    
        self.is_moderator = is_moderator            # Bonus

    # Getters
    def get_user_id(self) -> int:
        return self.user_id

    def get_is_logged_in(self) -> bool:
        return self.is_logged_in

    def get_name(self) -> str:
        return self.name

    def get_hashed_password(self) -> str:
        return self.hashed_password

    def get_is_administrator(self) -> bool:
        return self.is_administrator

    def get_is_moderator(self) -> bool:
        return self.is_moderator

    # Setters
    def set_is_logged_in(self, is_logged_in: bool):
        self.is_logged_in = is_logged_in

    def set_name(self, name: str):
        self.name = name

    def set_hashed_password(self, hashed_password: str):
        self.hashed_password = hashed_password

    def set_is_administrator(self, is_administrator: bool):
        self.is_administrator = is_administrator

    def set_is_moderator(self, is_moderator: bool):
        self.is_moderator = is_moderator
