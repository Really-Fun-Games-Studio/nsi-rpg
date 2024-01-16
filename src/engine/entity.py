import math

from src.engine.enums import EntityDeathResult
from src.engine.map_manager import MapManager
from src.engine.mobs_AI import MobAI

class Entity:
    """Classe permettant de gérer les entités. Créée automatiquement par `EntityManager.register_entity()`"""

    def __init__(self, name: str):
        self.x = 8
        self.y = 8

        self.locked = False # Variable définissant si l'entité est bloqué ou non (.lock() et .unlock())
        self.locked_animation = False

        self.direction = 0  # 0 : tourné vers la droite (ou sens par défaut), 1 : tourné vers la gauche (ou retourné)

        # Variables utilisées pour détecter les mouvements
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
        self.brain: MobAI | None = None

        self.name = name

        self.animation_name = None

        self.shadow = None

        self.death_callback = None
        self.death_result = EntityDeathResult.REMOVED

    def set_default_life(self, life: int):
        """Définit le nombre de PV de l'entité. Mettre -1 pour rendre l'entité immortelle."""
        self.life_points = life
        self.max_life_points = life

    def set_ai(self, ai: MobAI, engine: 'Engine'):
        """Enregistre une classe permettant de gérer l'IA du mob."""

        # La ligne suivante crée une instance de la classe d'IA. Cette ligne peut causer des warnings sur certains IDE
        # mais elle est bien valide
        self.brain = ai(self, engine.entity_manager, engine.map_manager)

    def update(self, delta: float):
        """Met à jour l'entité."""
        self.time += delta


        # Diminue la valeur du cooldown de dégât
        self.damage_cooldown -= delta
        if self.damage_cooldown < 0:
            self.damage_cooldown = 0

        # Si les coordonnées ont changé, l'entité a bougé

        x_motion = (self.x - self.last_x)

        if x_motion > 0:
            self.mouvements[0] = 1
        elif x_motion < 0:
            self.mouvements[0] = -1
        else:
            self.mouvements[0] = 0

        y_motion = (self.y - self.last_y)

        if y_motion > 0:
            self.mouvements[1] = 1
        elif y_motion < 0:
            self.mouvements[1] = -1
        else:
            self.mouvements[1] = 0

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

    def get_collisions_with_entity(self, other: 'Entity'):
        """Retourne True si l'entité courante est en collision avec l'entité donnée."""
        return (self.x+self.collision_rect[0] <= other.x+other.collision_rect[2] and
                self.x+self.collision_rect[2] >= other.x+other.collision_rect[0] and
                self.y+self.collision_rect[3] >= other.y+other.collision_rect[1] and
                self.y+self.collision_rect[1] <= other.y+other.collision_rect[3])

    def get_collisions(self, x: float, y: float, map_manager: MapManager):
        """Calcule les collisions."""

        # On calcule les coordonnées des points en haut à gauche et en bas à droite
        top_left_corner_tile = (math.floor((x + self.collision_rect[0]) / 16),
                                math.floor((y + self.collision_rect[1]) / 16))

        bottom_right_corner_tile = (math.floor((x + self.collision_rect[2]-1) / 16),
                                    math.floor((y + self.collision_rect[3]-1) / 16))

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

    def move(self, x: float, y: float, map_manager: MapManager, delta: float):
        """Fait bouger l'entité en tenant compte des collisions."""

        if not self.locked:  # Si l'entité n'est pas verrouillée on calcul le mouvement
            
            # On vérifie le sens du mouvement pour changer self.direction
            if x > 0:
                self.direction = 0
            elif x < 0:
                self.direction = 1
            # On ne met pas de else car si x = 0, on ne change pas de direction

            # On normalise la vitesse
            initial_speed = math.sqrt(x**2+y**2)

            x = x*delta/initial_speed*self.max_speed
            y = y*delta/initial_speed*self.max_speed

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
        """Met à jour l'animation en cours de l'entitée."""
        self.animation_name = name


    def lock(self, lock_animation: bool = False):
        """Bloque tout les mouvements de l'entitée"""
        if lock_animation:
            self.locked_animation = True
        self.locked = True

    def unlock(self):
        """Débloque tout les mouvements de l'entitée"""
        self.locked_animation = False
        self.locked = False