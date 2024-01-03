import math

from src.engine.entity import Entity
from src.engine.entity_manager import EntityManager
from src.engine.map_manager import MapManager
from src.engine.mobs_AI import MobAI


class WolfAI(MobAI):
    def __init__(self, entity: 'Entity', entity_manager: 'EntityManager', map_manager: 'MapManager'):
        super().__init__(entity, entity_manager, map_manager)

    def update(self):

        player: Entity = self.entity_manager.get_by_name(self.entity_manager.player_entity_name)

        x_distance = (player.x - self.entity.x)
        y_distance = (player.y - self.entity.y)

        player_distance = math.sqrt(x_distance ** 2 + y_distance ** 2)

        #player.take_damages(1)

        if abs(player_distance) > self.entity.max_speed:
            self.entity.move(x_distance / player_distance*self.entity.max_speed,
                             y_distance / player_distance*self.entity.max_speed, self.map_manager)
