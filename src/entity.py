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

    def move(self, x: float, y: float, map_manager: MapManager):
        """Fait bouger l'entité en tenant compte des collisions."""

        # Pour les collisions, on utilise le layer 1 (le deuxième)

        top_left_corner_tile = map_manager.get_tile_at(self.x+x-self.collision_rect[0], self.y+y-self.collision_rect[1])



    def link_animation(self, name: str):
        self.animation_name = name
