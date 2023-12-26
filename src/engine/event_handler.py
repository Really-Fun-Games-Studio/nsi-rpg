from pygame import event
from pygame.locals import *

import src.engine.engine as engine


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

        player = self.engine.entity_manager.get_by_name("player")
        if K_RIGHT in self.key_pressed:
            player.move(2, 0, self.engine.map_manager)
        if K_LEFT in self.key_pressed:
            player.move(-2, 0, self.engine.map_manager)
        if K_UP in self.key_pressed:
            player.move(0, -2, self.engine.map_manager)
        if K_DOWN in self.key_pressed:
            player.move(0, 2, self.engine.map_manager)
        if K_x in self.key_pressed:
            self.engine.camera.target_zoom *= 1.01
        if K_c in self.key_pressed:
            self.engine.camera.target_zoom *= 0.99
        if K_l in self.key_pressed:
            player.take_damages(1)

