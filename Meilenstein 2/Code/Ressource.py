class Ressource:
    def __init__(self, ressource_id: int, name: str, is_published: bool, description: str, link: str, created_by: str, faculty: str, ressource_type: str, opening_hours: str, likes: list[int], experience_reports: str, ressource_tags: list[str]):
        self.ressource_id = ressource_id                # Primärschlüssel
        self.name = name                                # Maximal 128 Zeichen
        self.is_published = is_published                # 
        self.description = description                  # Maximal 512 Zeichen
        self.link = link                                # Darf nicht None sein
        self.created_by = created_by                    # name#user_id
        self.faculty = faculty                          # 
        self.ressource_type = ressource_type            # 
        self.opening_hours = opening_hours              # Struktur nicht sicher festgelegt
        self.likes = likes                              # Bonus
        self.experience_reports = experience_reports    # Bonus
        self.ressource_tags = ressource_tags            # Bonus

    # Getters
    def get_ressource_id(self) -> int:
        return self.ressource_id

    def get_name(self) -> str:
        return self.name

    def get_is_published(self) -> bool:
        return self.is_published

    def get_description(self) -> str:
        return self.description

    def get_link(self) -> str:
        return self.link

    def get_created_by(self) -> str:
        return self.created_by

    def get_faculty(self) -> str:
        return self.faculty

    def get_ressource_type(self) -> str:
        return self.ressource_type

    def get_opening_hours(self) -> str:
        return self.opening_hours

    # Setters
    def set_name(self, name: str):
        self.name = name

    def set_is_published(self, is_published: bool):
        self.is_published = is_published

    def set_description(self, description: str):
        self.description = description

    def set_link(self, link: str):
        self.link = link

    def set_created_by(self, created_by: str):
        self.created_by = created_by

    def set_faculty(self, faculty: str):
        self.faculty = faculty

    def set_ressource_type(self, ressource_type: str):
        self.ressource_type = ressource_type

    def set_opening_hours(self, opening_hours: str):
        self.opening_hours = opening_hours
