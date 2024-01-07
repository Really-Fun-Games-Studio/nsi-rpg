class Widget:
    """Classe parente des widgets de menu."""
    def __init__(self, x, y, is_window_relative):
        self.x = x
        self.y = y
        self.is_window_relative = is_window_relative


class Label(Widget):
    """Un widget de texte."""
    def __init__(self, x: int | float, y: int | float, text: str, size: int | float, color: tuple[int, int, int],
                 centered: bool = False, is_window_relative: bool = -1):
        super().__init__(x, y, is_window_relative)
        self.text = text
        self.size = size
        self.centered = centered
        self.color = color


class Menu:
    """Un menu contenant des widgets."""
    def __init__(self):
        self.widgets: list[Widget] = []

    def add_widget(self, widget: Widget):
        """Ajoute le widget donné au menu."""
        self.widgets.append(widget)


class MenuManager:
    """Classe qui gère les menus."""

    def __init__(self):
        self.menus = {}
        self.active_menu: Menu | None = None

    def register_menu(self, menu: Menu, name: str):
        """Ajoute le menu donné au manager de menu avec le nom donné."""
        self.menus[name] = menu

    def show(self, name: str):
        """Affiche le menu au nom donné."""
        self.active_menu = self.menus[name]

    def hide(self):
        """Affiche le menu actuelement à l'écran."""
        self.active_menu = None
