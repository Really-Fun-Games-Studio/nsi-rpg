import math

from src.map_manager import MapManager


class Entity:
    """Classe permettant de gérer les entités. Créée automatiquement par `EntityManager.register_entity()`"""

    def __init__(self, name: str):
        self.x = 8
        self.y = 8

        self.collision_rect = [-7, -7, 7, 7]  # x1, y1, x2, y2

        # Time utilisé pour les IA
        self.time = 0

        self.name = name

        self.animation_name = None

    def update(self, delta: float):
        """Met à jour l'entité."""
        # self.x += 1

        self.time += delta

    def get_collisions(self, x: float, y: float, map_manager: MapManager):
        """Calcule les collisions."""
        # Pour les collisions, on utilise le layer 1 (le deuxième)

        top_left_corner_tile = (int((x + self.collision_rect[0]) / 16),
                                int((y + self.collision_rect[1]) / 16))

        bottom_right_corner_tile = (int((x + self.collision_rect[2]-1) / 16),
                                    int((y + self.collision_rect[3]-1) / 16))

        collision = False

        for xx in range(top_left_corner_tile[0], bottom_right_corner_tile[0]+1):
            for yy in range(top_left_corner_tile[1], bottom_right_corner_tile[1]+1):
                tile = map_manager.get_tile_at(xx, yy, 1)
                if tile != 0:
                    collision = True

        return collision

    def move(self, x: float, y: float, map_manager: MapManager):
        """Fait bouger l'entité en tenant compte des collisions."""

        collision_x = self.get_collisions(self.x + x, self.y, map_manager)
        collision_y = self.get_collisions(self.x, self.y + y, map_manager)

        if not collision_x:
            self.x += x
        else:
            i = 0
            if x > 0:
                while not self.get_collisions(self.x + i, self.y, map_manager):
                    i += 1
                i -= 1
            else:
                while not self.get_collisions(self.x + i, self.y, map_manager):
                    i -= 1
                i += 1

            self.x += i

        if not collision_y:
            self.y += y
        else:
            i = 0
            if y > 0:
                while not self.get_collisions(self.x, self.y + i, map_manager):
                    i += 1
                i -= 1
            else:
                while not self.get_collisions(self.x, self.y + i, map_manager):
                    i -= 1
                i += 1

            self.y += i


        #print(top_left_corner_tile, top_right_corner_tile, bottom_left_corner_tile, bottom_right_corner_tile)

    def link_animation(self, name: str):
        self.animation_name = name
