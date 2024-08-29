class Ressource:
    def __init__(self, ressource_id: int, name: str, is_published: bool, description: str, link: str, created_by: str, faculty: str, ressource_type: str, opening_hours: str, likes: list[int], experience_reports: str, ressource_tags: list[str]):
        self._ressource_id = ressource_id                # Primärschlüssel
        self._name = name                                # Maximal 128 Zeichen
        self._is_published = is_published                # 
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
        return self._ressource_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_published(self) -> bool:
        return self._is_published

    @property
    def description(self) -> str:
        return self._description

    @property
    def link(self) -> str:
        return self._link

    @property
    def created_by(self) -> str:
        return self._created_by

    @property
    def faculty(self) -> str:
        return self._faculty

    @property
    def ressource_type(self) -> str:
        return self._ressource_type

    @property
    def opening_hours(self) -> str:
        return self._opening_hours
    
    @property
    def likes(self) -> str:
        return self._likes
    
    @property
    def experience_reports(self) -> str:
        return self._experience_reports
    
    @property
    def ressource_tags(self) -> str:
        return self._ressource_tags

    # Setters

    @name.setter
    def name(self, name: str):
        self._name = name

    @is_published.setter
    def is_published(self, is_published: bool):
        self._is_published = is_published

    @description.setter
    def description(self, description: str):
        self._description = description

    @link.setter
    def link(self, link: str):
        self._link = link

    @created_by.setter
    def created_by(self, created_by: str):
        self._created_by = created_by

    @faculty.setter
    def faculty(self, faculty: str):
        self._faculty = faculty

    @ressource_type.setter
    def ressource_type(self, ressource_type: str):
        self._ressource_type = ressource_type

    @opening_hours.setter
    def opening_hours(self, opening_hours: str):
        self._opening_hours = opening_hours

    @likes.setter
    def likes(self, likes: str):
        self._likes = likes

    @experience_reports.setter
    def experience_reports(self, experience_reports: str):
        self._experience_reports = experience_reports

    @ressource_tags.setter
    def ressource_tags(self, ressource_tags: str):
        self._ressource_tags = ressource_tags
