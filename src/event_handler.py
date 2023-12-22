from pygame import event
from pygame.locals import *

import src.engine as engine


class EventHandler:
    """Classe utilisée pour traiter les pygame.event.get() et gérer les interactions avec le reste du programme."""
    def __init__(self, core: 'engine.Engine'):
        self.engine = core
        self.key_pressed = []

    def update(self):
        """Vérifie s'il y a de nouvelles interactions et les traites."""

        # Récupère les événements
        for e in event.get():
            if e.type == QUIT:
                self.engine.stop()
            elif e.type == KEYDOWN:
                self.key_pressed.append(e.key)
            elif e.type == KEYUP:
                self.key_pressed.remove(e.key)

        if K_RIGHT in self.key_pressed:
            self.engine.camera.x += 2
        if K_LEFT in self.key_pressed:
            self.engine.camera.x -= 2
        if K_UP in self.key_pressed:
            self.engine.camera.y -= 2
        if K_DOWN in self.key_pressed:
            self.engine.camera.y += 2
        if K_x in self.key_pressed:
            self.engine.camera.zoom *= 1.01
        if K_c in self.key_pressed:
            self.engine.camera.zoom *= 0.99
