class User:
    """
    Diese Klasse repräsentiert einen Benutzer im System mit verschiedenen Attributen, einschließlich Anmelde-Status, Name, Passwort und Berechtigungen.
    """
    def __init__(self, user_id: int, is_logged_in: bool, name: str, hashed_password: str, is_administrator: bool, is_moderator: bool, ressource_suggestions: str):
        """
        Initialisiert einen neuen Benutzer mit den angegebenen Attributen.

        :param user_id: Die ID des Benutzers (Primärschlüssel). Wird nur verwendet, um den Benutzer anzumelden.
        :type user_id: int
        :param is_logged_in: Gibt an, ob der Benutzer angemeldet ist.
        :type is_logged_in: bool
        :param name: Der Name des Benutzers. Maximale Länge = 40 Zeichen.
        :type name: str
        :param hashed_password: Das gehashte Passwort des Benutzers (MD5 Hash).
        :type hashed_password: str
        :param is_administrator: Gibt an, ob der Benutzer Administratorrechte hat.
        :type is_administrator: bool
        :param is_moderator: Gibt an, ob der Benutzer Moderatorrechte hat (Bonus).
        :type is_moderator: bool
        :param ressource_suggestions: Vorschläge des Benutzers zu neuen Ressourcen.
        :type ressource_suggestions: str
        """
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
        """
        Gibt die ID des Benutzers zurück.

        :return: Die ID des Benutzers.
        :rtype: int
        """
        return self._user_id

    @property
    def is_logged_in(self) -> bool:
        """
        Gibt an, ob der Benutzer angemeldet ist.

        :return: True, wenn der Benutzer angemeldet ist, andernfalls False.
        :rtype: bool
        """
        return self._is_logged_in

    @property
    def name(self) -> str:
        """
        Gibt den Namen des Benutzers zurück.

        :return: Der Name des Benutzers.
        :rtype: str
        """
        return self._name

    @property
    def hashed_password(self) -> str:
        """
        Gibt das gehashte Passwort des Benutzers zurück.

        :return: Das gehashte Passwort des Benutzers (MD5 Hash).
        :rtype: str
        """
        return self._hashed_password

    @property
    def is_administrator(self) -> bool:
        """
        Gibt an, ob der Benutzer Administratorrechte hat.

        :return: True, wenn der Benutzer Administratorrechte hat, andernfalls False.
        :rtype: bool
        """
        return self._is_administrator

    @property
    def is_moderator(self) -> bool:
        """
        Gibt an, ob der Benutzer Moderatorrechte hat.

        :return: True, wenn der Benutzer Moderatorrechte hat, andernfalls False.
        :rtype: bool
        """
        return self._is_moderator
    
    @property
    def ressource_suggestions(self) -> str:
        """
        Gibt die Vorschläge des Benutzers zu neuen Ressourcen zurück.

        :return: Die Vorschläge des Benutzers zu neuen Ressourcen.
        :rtype: str
        """
        return self._ressource_suggestions

    #  -------------------------- Setters --------------------------

    @user_id.setter
    def user_id(self, user_id: int):
        """
        Setzt die ID des Benutzers.

        :param user_id: Die neue ID des Benutzers.
        :type user_id: int
        """
        self._user_id = user_id

    @is_logged_in.setter
    def is_logged_in(self, is_logged_in: bool):
        """
        Setzt den Anmelde-Status des Benutzers.

        :param is_logged_in: Der neue Anmelde-Status des Benutzers.
        :type is_logged_in: bool
        """
        self._is_logged_in = is_logged_in

    @name.setter
    def name(self, name: str):
        """
        Setzt den Namen des Benutzers.

        :param name: Der neue Name des Benutzers.
        :type name: str
        """
        self._name = name

    @hashed_password.setter
    def hashed_password(self, hashed_password: str):
        """
        Setzt das gehashte Passwort des Benutzers.

        :param hashed_password: Das neue gehashte Passwort des Benutzers (MD5 Hash).
        :type hashed_password: str
        """
        self._hashed_password = hashed_password

    @is_administrator.setter
    def is_administrator(self, is_administrator: bool):
        """
        Setzt, ob der Benutzer Administratorrechte hat.

        :param is_administrator: Der neue Wert für Administratorrechte.
        :type is_administrator: bool
        """
        self._is_administrator = is_administrator

    @is_moderator.setter
    def is_moderator(self, is_moderator: bool):
        """
        Setzt, ob der Benutzer Moderatorrechte hat.

        :param is_moderator: Der neue Wert für Moderatorrechte.
        :type is_moderator: bool
        """
        self._is_moderator = is_moderator

    @ressource_suggestions.setter
    def ressource_suggestions(self, ressource_suggestions: str):
        """
        Setzt die Vorschläge des Benutzers zu neuen Ressourcen.

        :param ressource_suggestions: Die neuen Vorschläge des Benutzers zu neuen Ressourcen.
        :type ressource_suggestions: str
        """
        self._ressource_suggestions = ressource_suggestions