import math
from types import FunctionType

from pygame import event, display
from pygame.locals import *

import src.engine.engine as engine
from src.engine.enums import GameState

class EventHandler:
    """Classe utilisée pour traiter les pygame.event.get() et gérer les interactions avec le reste du programme."""

    def __init__(self, core: 'engine.Engine'):
        self.engine = core
        self.key_pressed = []
        self.buttons_area = []
        self.hovered_buttons_area = []
        self.hovered_sliders_area = []
        self.sliders_area = []
        self.key_cooldown: dict[int: float] = {}

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

        elif is_window_relative == 2:
            return (rect[0]*window_size[0] < point[0] < rect[0]*window_size[0] + rect[2]*window_size[0] and
                    rect[1]*window_size[1] < point[1] < rect[1]*window_size[1] + rect[3]*window_size[1])

        return rect[0] < point[0] < rect[0] + rect[2] and rect[1] < point[1] < rect[1] + rect[3]

    def register_button_area(self, rect: tuple[float | int, float | int, float | int, float | int],
                             callback: FunctionType | classmethod | staticmethod, name: str,
                             is_window_relative: int = -1,
                             hover_callback: FunctionType | classmethod | staticmethod = None):
        """Enregistre une zone comme bouton. La fonction donnée sera donc executée lorsque la zone sur la fenêtre
        sera cliqué. is_window_relative doit être 0 pour que le rect soit multipliée par la largeur de la fenêtre et 1
        pour qu'elle soit multipliée par la hauteur"""
        self.buttons_area.append((rect, callback, is_window_relative, name, hover_callback))

    def remove_button_area(self, name: str):
        """Supprime les boutons aux noms donnés."""

        # On itère dans toute la liste et on ne garde que les éléments ne portant pas le nom cherché
        cleared_list = []
        for area in self.buttons_area:
            if area[3] != name:
                cleared_list.append(area)

        self.buttons_area = cleared_list

    def register_slider_area(self, size: tuple[float | int, float | int],
                             motion_rect: tuple[float | int, float | int, float | int, float | int],
                             motion_axes: tuple[bool, bool],
                             name: str,
                             is_window_relative: int = -1,
                             clicked_callback: FunctionType | classmethod | staticmethod = None,
                             released_callback: FunctionType | classmethod | staticmethod = None,
                             motion_callback: FunctionType | classmethod | staticmethod = None,
                             hover_callback: FunctionType | classmethod | staticmethod = None,
                             default_values: tuple[int, int] = (0., 0.)):
        """Enregistre une zone comme une zone déplaçable à l'écran."""
        self.sliders_area.append([[motion_rect[0]+default_values[0]*motion_rect[2], motion_rect[1]+default_values[1]*motion_rect[3], *size], is_window_relative, False, default_values,
                                  motion_axes, motion_rect,
                                  clicked_callback, released_callback, hover_callback, motion_callback, name])
        # Le premier booléen correspond à l'état de suivi de la souris

    def remove_slider_area(self, name: str):
        """Supprime les sliders aux noms donnés."""

        # On itère dans toute la liste et on ne garde que les éléments ne portant pas le nom cherché
        cleared_list = []
        for area in self.sliders_area:
            if area[10] != name:
                cleared_list.append(area)

        self.sliders_area = cleared_list

    @staticmethod
    def get_slider_area_values(slider: list):
        """Donne la valeur de la zone de slider donnée."""
        if slider[5][2]:
            x_value = round((slider[0][0]-slider[5][0])/slider[5][2], 5)
        else:
            x_value = -1
        if slider[5][3]:
            y_value = round((slider[0][1]-slider[5][1])/slider[5][3], 5)
        else:
            y_value = -1
        return x_value, y_value


    def update(self, delta: float):
        """Vérifie s'il y a de nouvelles interactions et les traites."""

        window_size = display.get_window_size()

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


                    for area in self.sliders_area:
                        if self.get_click_collision(
                                (area[0][0]-area[0][2]/2, area[0][1]-area[0][3]/2, area[0][2], area[0][3]),
                                                    e.pos, area[1]):
                            area[2] = True
                            if area[1] == 0:
                                area[3] = (e.pos[0]/window_size[0] - area[0][0], e.pos[1]/window_size[0] - area[0][1])
                            elif area[1] == 1:
                                area[3] = (e.pos[0]/window_size[1] - area[0][0], e.pos[1]/window_size[1] - area[0][1])
                            elif area[1] == 2:
                                area[3] = (e.pos[0]/window_size[0] - area[0][0], e.pos[1]/window_size[1] - area[0][1])
                            else:
                                area[3] = (e.pos[0] - area[0][0], e.pos[1] - area[0][1])

                            if area[6] is not None:
                                area[6](self.get_slider_area_values(area))

            elif e.type == MOUSEBUTTONUP:
                for area in self.sliders_area:
                    if area[2]:
                        area[2] = False
                        if area[7] is not None:
                            area[7](self.get_slider_area_values(area))

            elif e.type == MOUSEMOTION:
                for area in self.buttons_area:
                    if area[4] is not None:
                        if self.get_click_collision(area[0], e.pos, area[2]):
                            if area not in self.hovered_buttons_area:
                                area[4](True)
                                self.hovered_buttons_area.append(area)
                        else:
                            if area in self.hovered_buttons_area:
                                area[4](False)
                                self.hovered_buttons_area.remove(area)

                for area in self.sliders_area:
                    if area[2]:
                        if area[4][0]:
                            if area[1] == 0:
                                area[0][0] = e.pos[0]/window_size[0]-area[3][0]
                            elif area[1] == 1:
                                area[0][0] = e.pos[0]/window_size[1]-area[3][0]
                            elif area[1] == 2:
                                area[0][0] = e.pos[0]/window_size[0]-area[3][0]
                            else:
                                area[0][0] = e.pos[0] - area[3][0]
                        if area[4][1]:
                            if area[1] == 0:
                                area[0][1] = e.pos[1]/window_size[0]-area[3][1]
                            elif area[1] == 1:
                                area[0][1] = e.pos[1]/window_size[1]-area[3][1]
                            elif area[1] == 2:
                                area[0][1] = e.pos[1]/window_size[1]-area[3][1]
                            else:
                                area[0][1] = e.pos[1]-area[3][1]

                        if area[0][0] < area[5][0]:
                            area[0][0] = area[5][0]
                        if area[0][0] > area[5][0]+area[5][2]:
                            area[0][0] = area[5][0]+area[5][2]

                        if area[0][1] < area[5][1]:
                            area[0][1] = area[5][1]
                        if area[0][1] > area[5][1]+area[5][3]:
                            area[0][1] = area[5][1]+area[5][3]

                        if area[9] is not None:
                            area[9](self.get_slider_area_values(area))
                    if area[8] is not None:
                        if self.get_click_collision(
                                (area[0][0] - area[0][2] / 2, area[0][1] - area[0][3] / 2, area[0][2], area[0][3]),
                                e.pos, area[1]):
                            if area not in self.hovered_sliders_area:
                                area[8](True)
                                self.hovered_sliders_area.append(area)
                        else:
                            if area in self.hovered_sliders_area:
                                area[8](False)
                                self.hovered_sliders_area.remove(area)

        if self.engine.entity_manager.player_entity_name:
            if K_RIGHT in self.key_pressed:
                self.engine.entity_manager.move_player_controls(1, 0, delta)
            if K_LEFT in self.key_pressed:
                self.engine.entity_manager.move_player_controls(-1, 0, delta)
            if K_UP in self.key_pressed:
                self.engine.entity_manager.move_player_controls(0, -1, delta)
            if K_DOWN in self.key_pressed:
                self.engine.entity_manager.move_player_controls(0, 1, delta)

            if K_SPACE in self.key_pressed:
                self.engine.dialogs_manager.next_signal()
                self.key_pressed.remove(K_SPACE)
            
            if K_ESCAPE in self.key_pressed and self.key_cooldown.get(K_ESCAPE, 0) <= 0 and self.engine.game_state == GameState.NORMAL:
                if not self.engine.settings_manager.menu_is_displaying:
                    self.engine.settings_manager.show_menu()
                else:
                    self.engine.settings_manager.hide_menu()
                self.cooldown(K_ESCAPE, self.engine.settings_manager.menu_fade_time)
            
            if K_F11 in self.key_pressed and self.key_cooldown.get(K_F11, 0) <= 0:
                screen_mode = self.engine.settings_manager.get_screen_mode()
                if screen_mode == FULLSCREEN:
                    self.engine.settings_manager.set_screen_mode(RESIZABLE)

                elif screen_mode == RESIZABLE:
                    self.engine.settings_manager.set_screen_mode(FULLSCREEN)

                self.cooldown(K_F11, 0.2)

            if self.engine.DEBUG_MODE:
                if K_l in self.key_pressed:
                    self.engine.entity_manager.get_by_name("player").take_damages(1)
                if K_p in self.key_pressed:
                    self.engine.renderer.emit_particles(math.floor(self.engine.entity_manager.get_by_name("player").x),
                                                        math.floor(self.engine.entity_manager.get_by_name("player").y),
                                                        16, 16, 16, 1, 8, 0, 60., 0.2, 1., (0, 200, 200))
                if K_o in self.key_pressed:
                    print(f"Player pos: X = {self.engine.entity_manager.get_by_name('player').x} "
                          f"Y = {self.engine.entity_manager.get_by_name('player').y}")
                    self.key_pressed.remove(K_o)

                if K_x in self.key_pressed:
                    self.engine.settings_manager.zoom *= 1.01
                if K_c in self.key_pressed:
                    self.engine.settings_manager.zoom *= 0.99
        
        for key in self.key_cooldown.keys():
            if key not in self.key_pressed:
                self.key_cooldown[key] -= delta

    def cooldown(self, key: int, cooldown: float):
        self.key_cooldown[key] = cooldown