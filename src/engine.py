from src.event_handler import EventHandler
from src.renderer import Renderer
import pygame


class Engine:
    """Classe principale qui regroupe tous les composants du programme (Renderer, MapManager, EventHandler, etc ...)"""
    def __init__(self):
        # L'initialisation de Pygame est nécéssaire pour tous les modules
        pygame.init()
        self.running = False
        self.renderer = Renderer(self)
        self.event_handler = EventHandler(self)

    def loop(self):
        """Fonction à lancer au début du programme et qui va lancer les updates dans une boucle.
        Attend jusqu'à la fin du jeu."""
        self.running = True
        while self.running:
            self.update()

    def update(self):
        """Fonction qui regroupe toutes les updates des composants. Elle permet de mettre à jour le jeu quand on
        l'appelle."""
        self.renderer.update()
        self.event_handler.update()

    def stop(self):
        """Arrete le programme."""
        self.running = False
        pygame.quit()
