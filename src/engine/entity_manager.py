from src.engine.entity import Entity


class EntityManager:
    """Classe chargée de gérer les entités."""
    def __init__(self):
        self.entities: dict[str:Entity] = {}

    def register_entity(self, name: str):
        """Crée une entité et l'enregistre dans un dictionnaire."""
        entity = Entity(name)
        self.entities[name] = entity
        return entity

    def update(self, delta: float):
        """Met à jour toutes les entités enregistrées."""
        for entity_name in list(self.entities.keys()):
            entity = self.entities[entity_name]
            entity.update(delta)
            if entity.life_points == 0:
                self.entities.pop(entity_name)

    def get_all_entities(self):
        """Donne la liste de toutes les entités enregistrées."""
        return list(self.entities.values())

    def get_by_name(self, name: str):
        """Donne l'entité avec le nom donné."""
        return self.entities[name]
