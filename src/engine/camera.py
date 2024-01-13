from src.engine.entity import Entity


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.zoom = 1.75

        # Décalage lors du mouvement du joueur
        self.player_moving_offset = 100

        # Variables utilisées pour le scrolling
        self.target_x = self.x
        self.target_y = self.y
        self.target_zoom = self.zoom

        self.smoothness = 0.5

        self.followed_entity: Entity | None = None

    def update(self, delta: float):
        """Met à jour la caméra. Permet, par exemple, de faire le scrolling."""

        # Si on suit une entité, on met à jour les coordonnées de suivi
        if self.followed_entity is not None:
            self.target_x = (self.followed_entity.x + self.followed_entity.mouvements[0] *
                             self.player_moving_offset / self.zoom)
            self.target_y = (self.followed_entity.y + self.followed_entity.mouvements[1] *
                             self.player_moving_offset / self.zoom)

        self.x += (self.target_x - self.x)*delta / self.smoothness
        self.y += (self.target_y - self.y)*delta / self.smoothness
        self.zoom += (self.target_zoom - self.zoom)*delta / self.smoothness

    def follow_entity(self, entity: Entity | None):
        """Active le suivit de l'entité donnée. Mettre `None` pour retirer le suivit."""
        self.followed_entity = entity
