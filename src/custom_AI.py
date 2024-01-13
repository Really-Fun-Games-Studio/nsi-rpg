import math
import random

from src.engine.entity import Entity
from src.engine.entity_manager import EntityManager
from src.engine.map_manager import MapManager
from src.engine.mobs_AI import MobAI


class WolfAI(MobAI):
    def __init__(self, entity: 'Entity', entity_manager: 'EntityManager', map_manager: 'MapManager'):
        super().__init__(entity, entity_manager, map_manager)

        self.ATTACK_DISTANCE = 160
        self.timer = 0
        self.walk_x = 0
        self.walk_y = 0
        self.comportment = 0  # 0 : waiting, 1: walking

    def update(self, delta: float):
        """Fonction executée à chaque tick pour chaque loup et qui gère l'IA."""

        # On récupère l'entité joueur
        player: Entity = self.entity_manager.get_by_name(self.entity_manager.player_entity_name)

        # On calcule la distance en x et en y entre le loup et le joueur
        x_distance = (player.x - self.entity.x)
        y_distance = (player.y - self.entity.y)

        # On calcule la distance
        player_distance = math.sqrt(x_distance ** 2 + y_distance ** 2)

        # On vérifie que le loup peut voir le joueur
        if player_distance <= self.ATTACK_DISTANCE:
            # On rétablit la vitesse du loup à 1
            self.entity.max_speed = 1.

            # Si le loup touche le joueur, il lui inflige des dégats
            if player.get_collisions_with_entity(self.entity):
                player.take_damages(1)

            # Si le loup n'est pas déja sur le joueur, on le fait s'en raprocher
            if player_distance > self.entity.max_speed:
                self.entity.move(x_distance / player_distance*self.entity.max_speed,
                                 y_distance / player_distance*self.entity.max_speed, self.map_manager)

        else:
            # Comportement d'attente

            # On diminue la vitesse
            self.entity.max_speed = 0.5

            self.timer -= delta
            # Si le timer est fini et que le loup était en train d'attendre, il commence à marcher
            if self.timer <= 0 and self.comportment == 0:
                self.comportment = 1
                self.timer = random.random() * 5.

                # On choisit la direction
                self.walk_x = (random.random()-0.5)*2
                self.walk_y = (random.random()-0.5)*2
            # Si le timer est fini et que le loup était de marcher, il commence à attendre
            elif self.timer <= 0 and self.comportment == 1:
                self.comportment = 0
                self.timer = random.random() * 3

            # On fait avancer le loup quand il le doit
            if self.comportment == 1:
                self.entity.move(self.walk_x, self.walk_y, self.map_manager, delta)
