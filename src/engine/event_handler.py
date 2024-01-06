import math

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
                if e.key in self.key_pressed:
                    self.key_pressed.remove(e.key)

        if self.engine.entity_manager.player_entity_name:
            if K_RIGHT in self.key_pressed:
                self.engine.entity_manager.move_player_controls(1, 0)
            if K_LEFT in self.key_pressed:
                self.engine.entity_manager.move_player_controls(-1, 0)
            if K_UP in self.key_pressed:
                self.engine.entity_manager.move_player_controls(0, -1)
            if K_DOWN in self.key_pressed:
                self.engine.entity_manager.move_player_controls(0, 1)

            if K_SPACE in self.key_pressed:
                self.engine.dialogs_manager.next_signal()
                self.key_pressed.remove(K_SPACE)

            if self.engine.DEBUG_MODE:
                if K_l in self.key_pressed:
                    self.engine.entity_manager.get_by_name("player").take_damages(1)
                if K_p in self.key_pressed:
                    self.engine.renderer.emit_particles(math.floor(self.engine.entity_manager.get_by_name("player").x),
                                                    math.floor(self.engine.entity_manager.get_by_name("player").y),
                                                    16, 16, 16, 1, 8, 0, 1, 0.2, 1., (0, 200, 200))
                if K_o in self.key_pressed:
                    print(f"Player pos: X = {self.engine.entity_manager.get_by_name('player').x} "
                          f"Y = {self.engine.entity_manager.get_by_name('player').y}")

        if K_x in self.key_pressed:
            self.engine.camera.target_zoom *= 1.01
        if K_c in self.key_pressed:
            self.engine.camera.target_zoom *= 0.99

