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


    def get_ressource_id(self) -> int:
        return self.ressource_id

    def get_name(self) -> str:
        return self.name
    
    def set_name(self, name: str):
        self.name = name

    
#TODO: Getter und Setter