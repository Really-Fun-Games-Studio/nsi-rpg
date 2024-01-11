from types import FunctionType

import pygame

import src.engine.engine


class Widget:
    """Classe parente des widgets de menu."""
    def __init__(self, x, y, is_window_relative):
        self.x = x
        self.y = y
        self.is_window_relative = is_window_relative


class Label(Widget):
    """Un widget de texte."""
    def __init__(self, x: int | float, y: int | float, text: str, size: int | float, color: tuple[int, int, int],
                 centered: bool = False, is_window_relative: int = -1):
        super().__init__(x, y, is_window_relative)
        self.text = text
        self.size = size
        self.centered = centered
        self.color = color


class Button(Widget):
    """Un widget de bouton."""
    def __init__(self, x: int | float, y: int | float, text: str, size: int | float, color: tuple[int, int, int],
                 callback: FunctionType | classmethod | staticmethod, base_image: pygame.Surface,
                 hover_image: pygame.Surface, centered: bool = False, is_window_relative: int = -1,
                 area_name: str = "menu_button"):
        super().__init__(x, y, is_window_relative)
        self.text = text
        self.size = size
        self.color = color
        self.callback = callback
        self.base_image = base_image
        self.hover_image = hover_image
        self.centered = centered
        self.area_name = area_name
        self.hovered = False

    def set_hover_state(self, state: bool):
        """Modifie la valeur du hover."""
        self.hovered = state


class Menu:
    """Un menu contenant des widgets."""
    def __init__(self):
        self.widgets: list[Widget] = []

    def add_widget(self, widget: Widget):
        """Ajoute le widget donné au menu."""
        self.widgets.append(widget)


class MenuManager:
    """Classe qui gère les menus."""

    def __init__(self, engine: 'src.engine.engine.Engine'):
        self.menus = {}
        self.active_menu: Menu | None = None
        self.engine = engine

    def register_menu(self, menu: Menu, name: str):
        """Ajoute le menu donné au manager de menu avec le nom donné."""
        self.menus[name] = menu

    def show(self, name: str):
        """Affiche le menu au nom donné."""
        self.active_menu = self.menus[name]

        # On itère dans tous les bouttons pour leur ajouter une interaction
        for btn in self.active_menu.widgets:
            if isinstance(btn, Button):
                width = btn.base_image.get_width() / self.engine.renderer.window_size[0]
                height = btn.base_image.get_height() / self.engine.renderer.window_size[1]
                area_x = btn.x
                area_y = btn.y
                if btn.centered:
                    area_x -= width / 2
                    area_y -= height / 2
                self.engine.event_handler.register_button_area((area_x, area_y, width, height), btn.callback,
                                                               btn.area_name,
                                                               btn.is_window_relative, btn.set_hover_state)

    def hide(self):
        """Cache le menu actuelement à l'écran."""
        # On itère dans tous les bouttons pour retirer l'interaction
        for elem in self.active_menu.widgets:
            if isinstance(elem, Button):
                self.engine.event_handler.remove_button_area(elem.area_name)
        self.active_menu = None
