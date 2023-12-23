from src.map_manager import MapManager


class Entity:
    """Classe permettant de gérer les entités. Créée automatiquement par `EntityManager.register_entity()`"""

    def __init__(self, name: str):
        self.x = 8
        self.y = 8

        self.collision_rect = [-7, -7, 20, 20]  # x1, y1, x2, y2

        # Time utilisé pour les IA
        self.time = 0

        self.name = name

        self.animation_name = None

    def update(self, delta: float):
        """Met à jour l'entité."""
        # self.x += 1

        self.time += delta

    def move(self, x: float, y: float, map_manager: MapManager):
        """Fait bouger l'entité en tenant compte des collisions."""

        # Pour les collisions, on utilise le layer 1 (le deuxième)

        top_left_corner_tile = (int((self.x + x + self.collision_rect[0]) / 16),
                                int((self.y + y + self.collision_rect[1]) / 16))
        top_right_corner_tile = (int((self.x + x + self.collision_rect[2]) / 16),
                                 int((self.y + y + self.collision_rect[1]) / 16))

        bottom_left_corner_tile = (int((self.x + x + self.collision_rect[0]) / 16),
                                   int((self.y + y + self.collision_rect[3]) / 16))
        bottom_right_corner_tile = (int((self.x + x + self.collision_rect[2]) / 16),
                                    int((self.y + y + self.collision_rect[3]) / 16))

        print(top_left_corner_tile, top_right_corner_tile, bottom_left_corner_tile, bottom_right_corner_tile)

    def link_animation(self, name: str):
        self.animation_name = name
