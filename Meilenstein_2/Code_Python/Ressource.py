class Ressource:
    """
    Diese Klasse repräsentiert eine Ressource mit verschiedenen Attributen, einschließlich Name, Beschreibung, Link und weiteren Metadaten.
    """
    def __init__(self, ressource_id: int, name: str, is_published: bool, is_deleted: bool, description: str, link: str, created_by: str, faculty: str, ressource_type: str, opening_hours: str, likes: str, experience_reports: str, ressource_tags: list[str]):
        """
        Initialisiert eine neue Ressource mit den angegebenen Attributen.

        :param ressource_id: Die ID der Ressource (Primärschlüssel).
        :type ressource_id: int
        :param name: Der Name der Ressource, maximal 128 Zeichen.
        :type name: str
        :param is_published: Gibt an, ob die Ressource veröffentlicht ist.
        :type is_published: bool
        :param is_deleted: Gibt an, ob die Ressource gelöscht ist.
        :type is_deleted: bool
        :param description: Eine Beschreibung der Ressource, maximal 512 Zeichen.
        :type description: str
        :param link: Ein Link zur Ressource. Darf nicht None sein.
        :type link: str
        :param created_by: Der Ersteller der Ressource (Name oder Benutzer-ID).
        :type created_by: str
        :param faculty: Die Fakultät oder der Bereich, dem die Ressource zugeordnet ist.
        :type faculty: str
        :param ressource_type: Der Typ der Ressource.
        :type ressource_type: str
        :param opening_hours: Die Öffnungszeiten der Ressource, Struktur nicht festgelegt.
        :type opening_hours: str
        :param likes: Eine Optionale Angabe von Likes zur Ressource (Bonus).
        :type likes: str
        :param experience_reports: Erfahrungsberichte zur Ressource (Bonus).
        :type experience_reports: str
        :param ressource_tags: Tags, die die Ressource beschreiben (Bonus).
        :type ressource_tags: list[str]
        """
        self._ressource_id = ressource_id                # Primärschlüssel
        self._name = name                                # Maximal 128 Zeichen
        self._is_published = is_published                # 
        self._is_deleted = is_deleted
        self._description = description                  # Maximal 512 Zeichen
        self._link = link                                # Darf nicht None sein
        self._created_by = created_by                    # name#user_id
        self._faculty = faculty                          # 
        self._ressource_type = ressource_type            # 
        self._opening_hours = opening_hours              # Struktur nicht sicher festgelegt
        self._likes = likes                              # Bonus
        self._experience_reports = experience_reports    # Bonus
        self._ressource_tags = ressource_tags            # Bonus

    # Getters

    @property
    def ressource_id(self) -> int:
        """
        Gibt die ID der Ressource zurück.

        :return: Die ID der Ressource.
        :rtype: int
        """
        return self._ressource_id

    @property
    def name(self) -> str:
        """
        Gibt den Namen der Ressource zurück.

        :return: Der Name der Ressource.
        :rtype: str
        """
        return self._name

    @property
    def is_published(self) -> bool:
        """
        Gibt an, ob die Ressource veröffentlicht ist.

        :return: True, wenn die Ressource veröffentlicht ist, andernfalls False.
        :rtype: bool
        """
        return self._is_published
    
    @property
    def is_deleted(self) -> bool:
        """
        Gibt an, ob die Ressource gelöscht ist.

        :return: True, wenn die Ressource gelöscht ist, andernfalls False.
        :rtype: bool
        """
        return self._is_deleted

    @property
    def description(self) -> str:
        """
        Gibt die Beschreibung der Ressource zurück.

        :return: Die Beschreibung der Ressource.
        :rtype: str
        """
        return self._description

    @property
    def link(self) -> str:
        """
        Gibt den Link zur Ressource zurück.

        :return: Der Link zur Ressource.
        :rtype: str
        """
        return self._link

    @property
    def created_by(self) -> str:
        """
        Gibt den Ersteller der Ressource zurück.

        :return: Der Ersteller der Ressource.
        :rtype: str
        """
        return self._created_by

    @property
    def faculty(self) -> str:
        """
        Gibt die Fakultät oder den Bereich der Ressource zurück.

        :return: Die Fakultät oder der Bereich der Ressource.
        :rtype: str
        """
        return self._faculty

    @property
    def ressource_type(self) -> str:
        """
        Gibt den Typ der Ressource zurück.

        :return: Der Typ der Ressource.
        :rtype: str
        """
        return self._ressource_type

    @property
    def opening_hours(self) -> str:
        """
        Gibt die Öffnungszeiten der Ressource zurück.

        :return: Die Öffnungszeiten der Ressource.
        :rtype: str
        """
        return self._opening_hours
    
    @property
    def likes(self) -> str:
        """
        Gibt die Likes der Ressource zurück (optional).

        :return: Die Likes der Ressource.
        :rtype: str
        """
        return self._likes
    
    @property
    def experience_reports(self) -> str:
        """
        Gibt die Erfahrungsberichte zur Ressource zurück (optional).

        :return: Die Erfahrungsberichte zur Ressource.
        :rtype: str
        """
        return self._experience_reports
    
    @property
    def ressource_tags(self) -> str:
        """
        Gibt die Tags der Ressource zurück (optional).

        :return: Die Tags der Ressource.
        :rtype: list[str]
        """
        return self._ressource_tags

    # Setters

    @name.setter
    def name(self, name: str):
        """
        Setzt den Namen der Ressource.

        :param name: Der neue Name der Ressource.
        :type name: str
        """
        self._name = name

    @is_published.setter
    def is_published(self, is_published: bool):
        """
        Setzt den Veröffentlichungsstatus der Ressource.

        :param is_published: Der neue Veröffentlichungsstatus.
        :type is_published: bool
        """
        self._is_published = is_published

    @is_deleted.setter
    def is_deleted(self, is_deleted: bool):
        """
        Setzt den Löschstatus der Ressource.

        :param is_deleted: Der neue Löschstatus.
        :type is_deleted: bool
        """
        self._is_deleted = is_deleted

    @description.setter
    def description(self, description: str):
        """
        Setzt die Beschreibung der Ressource.

        :param description: Die neue Beschreibung der Ressource.
        :type description: str
        """
        self._description = description

    @link.setter
    def link(self, link: str):
        """
        Setzt den Link zur Ressource.

        :param link: Der neue Link zur Ressource.
        :type link: str
        """
        self._link = link

    @created_by.setter
    def created_by(self, created_by: str):
        """
        Setzt den Ersteller der Ressource.

        :param created_by: Der neue Ersteller der Ressource.
        :type created_by: str
        """
        self._created_by = created_by

    @faculty.setter
    def faculty(self, faculty: str):
        """
        Setzt die Fakultät oder den Bereich der Ressource.

        :param faculty: Die neue Fakultät oder den neuen Bereich.
        :type faculty: str
        """
        self._faculty = faculty

    @ressource_type.setter
    def ressource_type(self, ressource_type: str):
        """
        Setzt den Typ der Ressource.

        :param ressource_type: Der neue Typ der Ressource.
        :type ressource_type: str
        """
        self._ressource_type = ressource_type

    @opening_hours.setter
    def opening_hours(self, opening_hours: str):
        """
        Setzt die Öffnungszeiten der Ressource.

        :param opening_hours: Die neuen Öffnungszeiten der Ressource.
        :type opening_hours: str
        """
        self._opening_hours = opening_hours

    @likes.setter
    def likes(self, likes: str):
        """
        Setzt die Likes der Ressource (optional).

        :param likes: Die neuen Likes der Ressource.
        :type likes: str
        """
        self._likes = likes

    @experience_reports.setter
    def experience_reports(self, experience_reports: str):
        """
        Setzt die Erfahrungsberichte zur Ressource (optional).

        :param experience_reports: Die neuen Erfahrungsberichte zur Ressource.
        :type experience_reports: str
        """
        self._experience_reports = experience_reports

    @ressource_tags.setter
    def ressource_tags(self, ressource_tags: str):
        """
        Setzt die Tags der Ressource (optional).

        :param ressource_tags: Die neuen Tags der Ressource.
        :type ressource_tags: list[str]
        """
        self._ressource_tags = ressource_tags
