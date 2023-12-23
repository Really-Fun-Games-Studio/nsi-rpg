from src.camera import Camera
from src.event_handler import EventHandler
from src.map_manager import MapManager
from src.renderer import Renderer
import pygame


class Engine:
    """Classe principale qui regroupe tous les composants du programme (Renderer, MapManager, EventHandler, etc ...)"""
    def __init__(self):
        # L'initialisation de Pygame est nécessaire pour tous les modules
        pygame.init()
        self.clock = pygame.time.Clock()

        self.running = False

        self.renderer = Renderer(self)
        self.event_handler = EventHandler(self)
        self.map_manager = MapManager()
        self.camera = Camera()

        self.map_manager.load_new("maps/map1.tmj")

        self.renderer.load_tile_set("assets/tiles.png", 16)

    def loop(self):
        """Fonction à lancer au début du programme et qui va lancer les updates dans une boucle.
        Attend jusqu'à la fin du jeu."""
        self.running = True
        while self.running:
            self.update()
            self.clock.tick(60.)

    def update(self):
        """Fonction qui regroupe toutes les updates des composants. Elle permet de mettre à jour le jeu quand on
        l'appelle."""
        self.renderer.update()
        self.event_handler.update()
        self.camera.update()

    def stop(self):
        """Arrête le programme."""
        self.running = False
        pygame.quit()
