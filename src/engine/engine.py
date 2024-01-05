from src.engine.boss_fight_manager import BossFightManager
from src.engine.camera import Camera
from src.engine.entity_manager import EntityManager
from src.engine.event_handler import EventHandler
from src.engine.event_sheduler import EventSheduler
from src.engine.map_manager import MapManager
from src.engine.renderer import Renderer
from src.engine.enums import GameState
import pygame


class Engine:
    """Classe principale qui regroupe tous les composants du programme (Renderer, MapManager, EventHandler, etc ...)"""
    def __init__(self):
        # L'initialisation de Pygame est nécessaire pour tous les modules
        pygame.init()

        # Debug mode utilisé pour tricher (voir les collisions, etc...) WOW ! n'utilisez pas ça pour jouer !
        self.DEBUG_MODE = False

        # Etat courant du jeu
        self.game_state = GameState.NORMAL

        self.clock = pygame.time.Clock()

        self.running = False

        # Composants du moteur de jeu
        self.renderer = Renderer(self)
        self.event_handler = EventHandler(self)
        self.map_manager = MapManager()
        self.camera = Camera()
        self.entity_manager = EntityManager(self.map_manager)
        self.boss_fight_manager = BossFightManager(self)
        self.event_sheduler = EventSheduler(self)

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
        self.camera.update()
        self.entity_manager.update(0.016666666)
        self.renderer.update(0.016666666)
        self.event_handler.update()
        self.event_sheduler.update()

    def stop(self):
        """Arrête le programme."""
        self.running = False
        pygame.quit()
