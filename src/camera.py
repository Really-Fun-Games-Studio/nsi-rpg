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

    def update(self):
        """Met à jour la caméra. Permet, par exemple, de faire le scrolling."""
        self.x += (self.target_x - self.x) / self.smoothness
        self.y += (self.target_y - self.y) / self.smoothness
        self.zoom += (self.target_zoom - self.zoom) / self.smoothness
