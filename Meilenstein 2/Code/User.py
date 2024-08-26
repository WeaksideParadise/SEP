class User:
    def __init__(self, user_id: int, is_logged_in: bool, name: str, hashed_password: str, is_administrator: bool, is_moderator: bool):
        self.user_id = user_id
        self.is_logged_in = is_logged_in
        self.name = name
        self.hashed_password = hashed_password
        self.is_administrator = is_administrator
        self.is_moderator = is_moderator

#TODO: Getter und Setter 