from pygame import event
from pygame.locals import QUIT

import src.engine as engine


class EventHandler:
    """Classe utilisée pour traiter les pygame.event.get() et gérer les interactions avec le reste du programme."""
    def __init__(self, core: 'engine.Engine'):
        self.engine = core

    def update(self):
        """Vérifie s'il y a de nouvelles interactions et les traites."""
        for e in event.get():
            if e.type == QUIT:
                self.engine.stop()
