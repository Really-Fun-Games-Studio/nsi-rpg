from src.entity import Entity


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.zoom = 1.

        # Variables utilisées pour le scrolling
        self.target_x = self.x
        self.target_y = self.y
        self.target_zoom = self.zoom

        self.smoothness = 20.

        self.followed_entity: Entity | None = None

    def update(self):
        """Met à jour la caméra. Permet, par exemple, de faire le scrolling."""

        # Si on suit une entité, on met à jour les coordonnées de suivi
        if self.followed_entity is not None:
            self.target_x = self.followed_entity.x
            self.target_y = self.followed_entity.y

        self.x += (self.target_x - self.x) / self.smoothness
        self.y += (self.target_y - self.y) / self.smoothness
        self.zoom += (self.target_zoom - self.zoom) / self.smoothness

    def follow_entity(self, entity: Entity):
        self.followed_entity = entity
