from types import FunctionType

import pygame

import src.engine.engine


class Widget:
    """Classe parente des widgets de menu."""
    def __init__(self, x, y, is_window_relative, widget_name):
        self.x = x
        self.y = y
        self.is_window_relative = is_window_relative
        self.widget_name = widget_name


class Label(Widget):
    """Un widget de texte."""
    def __init__(self, x: int | float, y: int | float, text: str, size: int | float, color: tuple[int, int, int],
                 widget_name: str, centered: bool = False, is_window_relative: int = -1):
        super().__init__(x, y, is_window_relative, widget_name)
        self.text = text
        self.size = size
        self.centered = centered
        self.color = color


class Slider(Widget):
    """Un widget pouvant être glissé pour récupérer une valeur."""

    def __init__(self, cursor_size: tuple[int | float, int | float],
                 area_rect: tuple[int | float, int | float],
                 width: int | float,
                 base_image: pygame.Surface,
                 hover_image: pygame.Surface,
                 rail_image: pygame.Surface,
                 widget_name: str,
                 value_changed_callback: FunctionType | classmethod | staticmethod | None = None,
                 is_window_relative: int = -1,
                 area_name: str = "menu_slider"):
        super().__init__(area_rect[0], area_rect[1], is_window_relative, widget_name)
        self.base_image = base_image
        self.hover_image = hover_image
        self.rail_image = rail_image
        self.area_name = area_name
        self.value_changed_callback = value_changed_callback
        self.hovered = False
        self.follow_mouse = False
        self.cursor_size = cursor_size
        self.value = 0.
        self.width = width

    def set_hover_state(self, state: bool):
        """Modifie la valeur du hover."""
        self.hovered = state

    def set_value(self, values: tuple[float, float]):
        """Appelée lorsque la valeur du slider est modifiée."""
        new_value = values[0]

        if new_value != self.value:
            self.value = new_value
            if self.value_changed_callback is not None:
                self.value_changed_callback(self.value)

    def get_value(self):
        """Retourne la valeur entre 0.0 et 1.0 du slider."""
        return self.value


class Button(Widget):
    """Un widget de bouton."""
    def __init__(self, x: int | float, y: int | float, text: str, size: int | float, color: tuple[int, int, int],
                 callback: FunctionType | classmethod | staticmethod, base_image: pygame.Surface,
                 hover_image: pygame.Surface, widget_name: str, centered: bool = False, is_window_relative: int = -1,
                 area_name: str = "menu_button"):
        super().__init__(x, y, is_window_relative, widget_name)
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

    def get_widgets_at_name(self, menu_name: str, widget_name: str):
        """Donne le widget au nom donné dans le menu au nom donné."""
        menu = self.menus[menu_name]

        found_sliders = []
        for widget in menu.widgets:
            if widget.widget_name == widget_name:
                found_sliders.append(widget)

        return found_sliders

    def show(self, name: str):
        """Affiche le menu au nom donné."""
        self.active_menu = self.menus[name]

        # On itère dans tous les bouttons pour leur ajouter une interaction
        for widget in self.active_menu.widgets:
            if isinstance(widget, Button):
                width = widget.base_image.get_width() / self.engine.renderer.window_size[0]
                height = widget.base_image.get_height() / self.engine.renderer.window_size[1]
                area_x = widget.x
                area_y = widget.y
                if widget.centered:
                    area_x -= width / 2
                    area_y -= height / 2
                self.engine.event_handler.register_button_area((area_x, area_y, width, height), widget.callback,
                                                               widget.area_name,
                                                               widget.is_window_relative, widget.set_hover_state)
            elif isinstance(widget, Slider):
                self.engine.event_handler.register_slider_area(widget.cursor_size,
                                                               (widget.x, widget.y, widget.width, 1), (True, False),
                                                               widget.area_name,
                                                               widget.is_window_relative,
                                                               hover_callback=widget.set_hover_state,
                                                               motion_callback=widget.set_value)

    def hide(self):
        """Affiche le menu actuelement à l'écran."""
        # On itère dans tous les bouttons pour retirer l'interaction
        for widget in self.active_menu.widgets:
            if isinstance(widget, Button):
                self.engine.event_handler.remove_button_area(widget.area_name)
            if isinstance(widget, Slider):
                self.engine.event_handler.remove_slider_area(widget.area_name)
        self.active_menu = None
