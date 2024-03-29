from types import FunctionType

import src.engine.engine
from src.engine.entity import Entity


class EventSheduler:
    """Gère le lancement d'évenements avec des conditions."""
    def __init__(self, engine: 'src.engine.engine.Engine'):
        self.area_callbacks = []
        self.engine = engine

    def register_area(self, area_rect: tuple[int, int, int, int], callback: FunctionType | classmethod | staticmethod,
                      linked_entities_name: list[Entity], single_use: bool = True, no_spam: bool = False):
        self.area_callbacks.append((area_rect, callback, linked_entities_name, single_use, no_spam, []))
        # La liste vide en dernier argument correspond aux entités actuellement dans la zone

    @staticmethod
    def get_collisions_with_entity(rect: tuple[int, int, int, int], entity: 'Entity'):
        """Retourne True si l'entité donnée touche le rectangle donné."""
        return (rect[0] <= entity.x+entity.collision_rect[2] and
                rect[0] + rect[2] >= entity.x+entity.collision_rect[0] and
                rect[1] + rect[3] >= entity.y+entity.collision_rect[1] and
                rect[1] <= entity.y+entity.collision_rect[3])

    def update(self):
        """Met à jour l'event sheduler et execute les actions si les conditions à son execution sont respéctées."""

        # On itère dans la liste des zones de détection
        for area in self.area_callbacks.copy():
            # On itère dans toutes les entités enregistrées
            for entity in area[2]:
                entity_in_area = self.get_collisions_with_entity(area[0], self.engine.entity_manager.get_by_name(entity))
                if entity_in_area and not (area[4] and entity in area[5]):
                    area[1](entity)
                    if area[3]:
                        self.area_callbacks.remove(area)
                    if area[4]:
                        area[5].append(entity)
                elif (not entity_in_area) and (area[4] and entity in area[5]):
                    area[5].remove(entity)
