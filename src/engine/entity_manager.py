from src.engine.entity import Entity
from src.engine.map_manager import MapManager


class EntityManager:
    """Classe chargée de gérer les entités."""
    def __init__(self, map_manager: MapManager):
        self.entities: dict[str:Entity] = {}
        self.player_entity_name = ""
        self.map_manager = map_manager

    def register_entity(self, name: str):
        """Crée une entité et l'enregistre dans un dictionnaire."""
        entity = Entity(name)
        self.entities[name] = entity
        return entity

    def set_player_entity(self, name: str):
        """Définit l'entité donnée comme le joueur. Elle peut donc être controlée."""
        self.player_entity_name = name

    def move_player_controls(self, x: float, y: float):
        """Bouge le joueur. X et y doivent être compris entre 0 et 1"""
        player: Entity = self.get_by_name(self.player_entity_name)
        player.move(x, y, self.map_manager)

    def update(self, delta: float):
        """Met à jour toutes les entités enregistrées."""
        for entity_name in list(self.entities.keys()):
            entity = self.entities[entity_name]
            entity.update(delta)
            if entity.life_points == 0:
                self.entities.pop(entity_name)

        if self.player_entity_name:
            player: Entity = self.get_by_name(self.player_entity_name)
            if player.mouvements[0] != 0. or player.mouvements[1] != 0.:
                player.link_animation("player_walking")
            else:
                player.link_animation("player_none")

    def get_all_entities(self):
        """Donne la liste de toutes les entités enregistrées."""
        return list(self.entities.values())

    def get_by_name(self, name: str):
        """Donne l'entité avec le nom donné."""
        return self.entities[name]
