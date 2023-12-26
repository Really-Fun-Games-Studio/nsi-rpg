import random

from src.animation import Anim
from src.camera import Camera
from src.entity_manager import EntityManager
from src.event_handler import EventHandler
from src.map_manager import MapManager
from src.renderer import Renderer
from src.enums import GameState
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
        self.entity_manager = EntityManager()

        # TODO : REMOVE (ONLY USED FOR TESTING)

        self.map_manager.load_new("maps/map2.tmj")

        self.renderer.load_tile_set("assets/tiles.png", 16)

        anim = Anim(0.5)
        anim.load_animation_from_directory("assets/entities/player/none")
        self.renderer.register_animation(anim, "player_none")

        player = self.entity_manager.register_entity("player")
        player.link_animation("player_none")
        player.collision_rect = [-7, -7, 7, 7]

        player.set_default_life(10)

        self.camera.follow_entity(player)

        for i in range(20):
            anim = Anim(0.5)
            anim.load_animation_from_directory("assets/entities/player/none")
            self.renderer.register_animation(anim, f"player_none_{i}")

            test = self.entity_manager.register_entity(f"test_{i}")
            test.x = random.randint(0, 200)
            test.y = random.randint(0, 200)
            test.link_animation(f"player_none_{i}")
            test.collision_rect = [-7, -7, 7, 7]

            test.set_default_life(10)

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

    def stop(self):
        """Arrête le programme."""
        self.running = False
        pygame.quit()
