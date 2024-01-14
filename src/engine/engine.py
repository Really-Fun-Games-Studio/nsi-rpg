import time

from src.engine.boss_fight_manager import BossFightManager
from src.engine.camera import Camera
from src.engine.dialogs_manager import DialogsManager
from src.engine.entity_manager import EntityManager
from src.engine.event_handler import EventHandler
from src.engine.event_sheduler import EventSheduler
from src.engine.map_manager import MapManager
from src.engine.menu_manager import MenuManager
from src.engine.renderer import Renderer
from src.engine.enums import GameState
from src.engine.sound_manager import SoundManager
from src.engine.settings_manager import SettingsManager
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

        self.running = False

        # Composants du moteur de jeu
        self.settings_manager = SettingsManager(60, 1.75) # DOIT ABSOLUMENT ETRE EN PREMIER (Sinon les autres composants qui nécessite les settings crash)
        self.renderer = Renderer(self)
        self.event_handler = EventHandler(self)
        self.map_manager = MapManager()
        self.camera = Camera(self.DEBUG_MODE, self.settings_manager.get_zoom())
        self.entity_manager = EntityManager(self.map_manager)
        self.boss_fight_manager = BossFightManager(self)
        self.event_sheduler = EventSheduler(self)
        self.dialogs_manager = DialogsManager(self)
        self.menu_manager = MenuManager(self)
        self.sound_manager = SoundManager(self.settings_manager.get_music_master_volume(), 
                                  self.settings_manager.get_sound_global_master_volume(),
                                  self.settings_manager.get_sound_master_volume())
        
        self.global_latency = 0
        self.last_latency = []
        self.latency_precision = self.settings_manager.latency_precision

    def loop(self):
        """Fonction à lancer au début du programme et qui va lancer les updates dans une boucle.
        Attend jusqu'à la fin du jeu."""
        self.running = True

        self.start_time = time.time()
        self.frames = 0

        # Initialisation ddes valeurs de delta et de last_time
        delta = 1.  # Le delta est le temps depuis la dernière image
        last_time = time.time()

        latency = 0

        
        

        while self.running:
            refresh_rate = self.settings_manager.get_refresh_rate()
            if refresh_rate == -1: # Pas de limite, vers l'infini et l'au-delà !!!

                self.update(delta)
                new_time = time.time()
                delta = new_time - last_time
                last_time = new_time

            else:
                while time.time() < last_time + 1 / refresh_rate - self.global_latency:
                    pass

                new_time = time.time()
                delta = new_time-last_time
                last_time = new_time


                self.update(delta)

                latency = delta - 1/refresh_rate
                if not latency > self.global_latency * 100 or self.global_latency == 0 or self.settings_manager.get_refresh_rate() != refresh_rate: # Impossible que le jeu prenne autant de retard, on skip cette latence dans le calcul, l'utilisateur a surement cliquer hors de la fenêtre
                    if len(self.last_latency) < self.latency_precision:
                        self.last_latency.append(latency)
                    else:
                        self.last_latency.pop(0)
                        self.last_latency.append(latency)

                    n = 0
                    for i in self.last_latency:
                        n += i

                    self.global_latency = n/len(self.last_latency)

    def update(self, delta: float):
        self.frames += 1
        if time.time() > 50 + self.start_time:
            print(self.frames/50)
            exit()
        """Fonction qui regroupe toutes les updates des composants. Elle permet de mettre à jour le jeu quand on
        l'appelle."""
        self.camera.update(delta, self.settings_manager.get_zoom())
        self.entity_manager.update(delta)
        self.renderer.update(delta)
        self.event_handler.update(delta)
        self.event_sheduler.update()
        self.dialogs_manager.update(delta)
        self.sound_manager.update(delta, self.settings_manager.get_music_master_volume(), 
                                  self.settings_manager.get_sound_global_master_volume(),
                                  self.settings_manager.get_sound_master_volume())

    def stop(self):
        """Arrête le programme."""
        self.running = False
        pygame.quit()
