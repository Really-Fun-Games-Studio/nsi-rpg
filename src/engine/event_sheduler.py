from types import FunctionType

import src.engine.engine


class EventSheduler:
    """Gère le lancement d'évenements avec des conditions."""
    def __init__(self, engine: 'src.engine.engine.Engine'):
        self.area_callbacks = []
        self.engine = engine

    def register_area(self, area_rect: tuple[int, int, int, int], callback: FunctionType | classmethod | staticmethod):
        self.area_callbacks.append((area_rect, callback))

    @staticmethod
    def get_collisions_with_entity(rect: tuple[int, int, int, int], entity: 'Entity'):
        """Retourne True si l'entité donnée touche le rectange donné."""
        return (rect[0] <= entity.x+entity.collision_rect[2] and
                rect[0] + rect[2] >= entity.x+entity.collision_rect[0] and
                rect[1] + rect[3] >= entity.y+entity.collision_rect[1] and
                rect[1] <= entity.y+entity.collision_rect[3])

    def update(self):
        for area in self.area_callbacks:
            area_rect = area[0]

            if self.get_collisions_with_entity(area_rect, self.engine.entity_manager.get_by_name("player")):
                print("oui")

            else:
                print("non")
