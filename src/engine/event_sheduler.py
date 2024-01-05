from types import FunctionType

import src.engine.engine
from src.engine.entity import Entity


class EventSheduler:
    """Gère le lancement d'évenements avec des conditions."""
    def __init__(self, engine: 'src.engine.engine.Engine'):
        self.area_callbacks = []
        self.engine = engine

    def register_area(self, area_rect: tuple[int, int, int, int], callback: FunctionType | classmethod | staticmethod,
                      linked_entities_name: list[Entity]):
        self.area_callbacks.append((area_rect, callback, linked_entities_name))

    @staticmethod
    def get_collisions_with_entity(rect: tuple[int, int, int, int], entity: 'Entity'):
        """Retourne True si l'entité donnée touche le rectange donné."""
        return (rect[0] <= entity.x+entity.collision_rect[2] and
                rect[0] + rect[2] >= entity.x+entity.collision_rect[0] and
                rect[1] + rect[3] >= entity.y+entity.collision_rect[1] and
                rect[1] <= entity.y+entity.collision_rect[3])

    def update(self):
        """Met à jour l'event sheluder et execute les actions si les conditions à son execution sont respéctées."""

        # On itère dans la liste des zones de détection
        for area in self.area_callbacks:
            # On itère dans toutes les entités enregistrées
            for entity in area[2]:
                if self.get_collisions_with_entity(area[0], self.engine.entity_manager.get_by_name(entity)):
                    area[1](entity)
