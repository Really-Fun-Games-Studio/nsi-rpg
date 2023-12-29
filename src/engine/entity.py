import math

from src.engine.map_manager import MapManager


class Entity:
    """Classe permettant de gérer les entités. Créée automatiquement par `EntityManager.register_entity()`"""

    def __init__(self, name: str):
        self.x = 8
        self.y = 8

        # Variables utilisées pour detecter les mouvements
        self.last_x = 0
        self.last_y = 0

        self.mouvements = [0., 0.]

        self.max_speed = 1.

        self.life_points = -1
        self.max_life_points = -1

        # Cooldown entre deux points de dégât
        self.damage_cooldown = 0
        self.default_damage_cooldown = 0.5

        self.collision_rect = [0, 0, 0, 0]  # x1, y1, x2, y2

        # Time utilisé pour les IA
        self.time = 0

        self.name = name

        self.animation_name = None

    def set_default_life(self, life: int):
        """Définit le nombre de PV de l'entité. Mettre -1 pour rendre l'entité immortelle."""
        self.life_points = life
        self.max_life_points = life

    def update(self, delta: float):
        """Met à jour l'entité."""
        self.time += delta

        # Diminue la valeur du cooldown de dégât
        self.damage_cooldown -= delta
        if self.damage_cooldown < 0:
            self.damage_cooldown = 0

        # Si les coordonnées ont changé, l'entité a bougé

        self.mouvements[0] = (self.x - self.last_x) / self.max_speed
        self.mouvements[1] = (self.y - self.last_y) / self.max_speed

        self.last_x = self.x
        self.last_y = self.y

    def take_damages(self, damages: int):
        """Inflige {damages} dégâts à l'entité."""

        # Si life_points est égal à -1, l'entité est immortelle
        if self.life_points != -1 and self.damage_cooldown == 0:
            # On inflige les dégâts
            self.life_points -= damages
            # Remet le cooldown au maximum
            self.damage_cooldown = self.default_damage_cooldown
            # Si la vie passe en négatif, on la remet à 0
            if self.life_points < 0:
                self.life_points = 0

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
            final_x = x
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

            final_x = i

        # On répète le procédé avec l'ordonnée
        if not self.get_collisions(self.x, self.y + y, map_manager):
            final_y = y
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

            final_y = i

        # On normalise le vecteur x, y pour ne pas dépacer la vitesse maximale de l'entité

        total_len = math.sqrt(final_x**2+final_y**2)
        if total_len == 0.:
            return

        self.x += final_x/total_len*self.max_speed
        self.y += final_y/total_len*self.max_speed

    def link_animation(self, name: str):
        """Met à jour l'animation en cours de l'entité."""
        self.animation_name = name
