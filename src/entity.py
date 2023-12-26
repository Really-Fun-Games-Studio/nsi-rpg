import math

from src.map_manager import MapManager


class Entity:
    """Classe permettant de gérer les entités. Créée automatiquement par `EntityManager.register_entity()`"""

    def __init__(self, name: str):
        self.x = 8
        self.y = 8

        self.collision_rect = [0, 0, 0, 0]  # x1, y1, x2, y2

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

        # On calcule les coordonnées des points en haut à gauche et en bas à droite
        top_left_corner_tile = (int((x + self.collision_rect[0]) / 16),
                                int((y + self.collision_rect[1]) / 16))

        bottom_right_corner_tile = (int((x + self.collision_rect[2]-1) / 16),
                                    int((y + self.collision_rect[3]-1) / 16))

        collision = False

        # On itère dans toute la zone de collision
        for xx in range(top_left_corner_tile[0], bottom_right_corner_tile[0]+1):
            for yy in range(top_left_corner_tile[1], bottom_right_corner_tile[1]+1):
                # Pour les collisions, on utilise le layer 1 (le deuxième)
                # On récupère la tile aux coordonnées données
                tile = map_manager.get_tile_at(xx, yy, 1)

                # Si la tile n'est pas du vide, il y a une collision.
                if tile != 0:
                    collision = True

        return collision

    def move(self, x: float, y: float, map_manager: MapManager):
        """Fait bouger l'entité en tenant compte des collisions."""

        # On simule le mouvement. Si on ne rencontre pas de collision, on applique le mouvement
        if not self.get_collisions(self.x + x, self.y, map_manager):
            self.x += x
        else:
            # Si on a une collision, on avance pixel par pixel jusqu'à atteindre la collision
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

        # On répète le procédé avec l'ordonnée
        if not self.get_collisions(self.x, self.y + y, map_manager):
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

    def link_animation(self, name: str):
        """Met à jour l'animation en cours de l'entité."""
        self.animation_name = name
