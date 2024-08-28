class User:
    def __init__(self, user_id: int, is_logged_in: bool, name: str, hashed_password: str, is_administrator: bool, is_moderator: bool, ressource_suggestions: str):
        self._user_id = user_id                             # Primärschlüssel - Setter wird nur genutzt, um Gast anzumelden
        self._is_logged_in = is_logged_in                   #
        self._name = name                                   # Maximale Länge = 40 Zeichen
        self._hashed_password = hashed_password             # MD5 Hash
        self._is_administrator = is_administrator           #
        self._is_moderator = is_moderator                   # Bonus
        self._ressource_suggestions = ressource_suggestions # Vorschläge zu neuen Ressourcen

    # -------------------------- Getters --------------------------

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def is_logged_in(self) -> bool:
        return self._is_logged_in

    @property
    def name(self) -> str:
        return self._name

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    @property
    def is_administrator(self) -> bool:
        return self._is_administrator

    @property
    def is_moderator(self) -> bool:
        return self._is_moderator
    
    @property
    def ressource_suggestions(self) -> str:
        return self._ressource_suggestions

    #  -------------------------- Setters --------------------------

    @user_id.setter
    def user_id(self, user_id: int):
        self._user_id = user_id

    @is_logged_in.setter
    def is_logged_in(self, is_logged_in: bool):
        self._is_logged_in = is_logged_in

    @name.setter
    def name(self, name: str):
        self._name = name

    @hashed_password.setter
    def hashed_password(self, hashed_password: str):
        self._hashed_password = hashed_password

    @is_administrator.setter
    def is_administrator(self, is_administrator: bool):
        self._is_administrator = is_administrator

    @is_moderator.setter
    def is_moderator(self, is_moderator: bool):
        self._is_moderator = is_moderator

    @is_moderator.setter
    def ressource_suggestions(self, ressource_suggestions: str):
        self._ressource_suggestions = ressource_suggestions