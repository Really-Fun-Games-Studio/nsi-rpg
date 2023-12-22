from pygame import display

import src.engine as engine

class Renderer:
    """Classe contenant le moteur de rendu. On utilise, pour cela la bibliothèque Pygame."""
    def __init__(self, core: 'engine.Engine'):
        self.engine = core
        self.window = display.set_mode((600, 600))

    def update(self):
        """Fait le rendu du jeu."""

