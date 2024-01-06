import math
from types import FunctionType

from pygame import event, display
from pygame.locals import *

import src.engine.engine as engine


class EventHandler:
    """Classe utilisée pour traiter les pygame.event.get() et gérer les interactions avec le reste du programme."""

    def __init__(self, core: 'engine.Engine'):
        self.engine = core
        self.key_pressed = []
        self.buttons_area = []

    @staticmethod
    def get_click_collision(rect: tuple[float | int, float | int, float | int, float | int], point: tuple[int, int],
                            is_window_relative: int):
        """Vérifie si le point et le rectangle donné sont en collision."""
        window_size = display.get_window_size()

        if is_window_relative == 0:
            return (rect[0]*window_size[0] < point[0] < rect[0]*window_size[0] + rect[2]*window_size[0]
                    and rect[1]*window_size[0] < point[1] < rect[1]*window_size[0] + rect[3]*window_size[0])

        elif is_window_relative == 1:
            return (rect[0]*window_size[1] < point[0] < rect[0]*window_size[1] + rect[2]*window_size[1] and
                    rect[1]*window_size[1] < point[1] < rect[1]*window_size[1] + rect[3]*window_size[1])

        return rect[0] < point[0] < rect[0] + rect[2] and rect[1] < point[1] < rect[1] + rect[3]

    def register_button_area(self, rect: tuple[float | int, float | int, float | int, float | int],
                             callback: FunctionType | classmethod | staticmethod,
                             is_window_relative: int = -1):
        """Enregistre une zone comme bouton. La fonction donnée sera donc executé lorsque la zone sur la fenêtre
        sera cliqué. is_window_relative doit être 0 pour que le rect soit multipliée par la largeur de la fenêtre et 1
        pour qu'elle soit multipliée par la hauteur"""
        self.buttons_area.append((rect, callback, is_window_relative))

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
            elif e.type == MOUSEBUTTONDOWN:
                # Vérifie si une des zones enregistrées comme bouton n'a pas été cliqué
                if e.button == 1:
                    for area in self.buttons_area:
                        if self.get_click_collision(area[0], e.pos, area[2]):
                            area[1]()

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
