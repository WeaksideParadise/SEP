

class Ressource:
    def __init__(self, ressource_id: int, name: str, is_published: bool, description: str, link: str, created_by: str, faculty: str, ressource_type: str, opening_hours: str):
        self.ressource_id = ressource_id
        self.name = name
        self.is_published = is_published
        self.description = description
        self.link = link
        self.created_by = created_by
        self.faculty = faculty
        self.ressource_type = ressource_type
        self.opening_hours = opening_hours


    def get_ressource_id(self) -> int:
        return self.ressource_id

    def get_name(self) -> str:
        return self.name
    
    def set_name(self, name: str):
        self.name = name

    
