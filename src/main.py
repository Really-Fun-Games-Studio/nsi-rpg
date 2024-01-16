import pygame.image

from src.custom_AI import WolfAI
from src.engine.animation import Anim
from src.engine.engine import Engine
from src.engine.enums import GameState, EntityDeathResult
from src.engine.menu_manager import Menu, Label, Button, Image, Slider
from pygame.locals import FULLSCREEN, RESIZABLE
import time

class Game(Engine):
    def __init__(self):
        super().__init__()
        self.map_manager.load_new("maps/map5.tmj")

        self.renderer.load_tile_set("assets/textures/tileset.png", 16)
        self.dialogs_manager.load_dialogs("assets/dialogs.json")

        self.create_player_entity()
        self.load_boss_fight_assets()
        self.spawn_mobs()

        self.DEBUG_MODE = False

        self.game_state = GameState.MAIN_MENU

        self.event_sheduler.register_area((64, 64, 32, 32), lambda _: self.dialogs_manager.start_dialog("test"), ["player"], False, True)

        self.renderer.dialogs_box = pygame.image.load("assets/textures/GUI/dialogs_box.png").convert_alpha()

        self.event_handler.register_button_area((0, 0, 0.1, 0.1), lambda : print("salut"), 0)

        self.sound_manager.music_add_to_playlist(".\\assets\\OST\\Main Title (Y'as pas de boss la donc jpp le mettre pour un fight).mp3")
        self.sound_manager.music_start_playlist()

        self.setup_main_menu()

    def start_game(self):
        self.game_state = GameState.NORMAL
        self.renderer.set_display(FULLSCREEN)
        self.renderer.fadein(1, (0, 0, 0), 100, True)

    def play_button_callback(self):
        self.renderer.fadeout(1, (0, 0, 0), 100, True, self.start_game)
        self.menu_manager.hide()

        self.sound_manager.music_remove_from_playlist(".\\assets\\OST\\Main Title (Y'as pas de boss la donc jpp le mettre pour un fight).mp3")
        self.sound_manager.music_add_to_playlist(".\\assets\\OST\\Bruit de foret pour yannis.mp3")
        self.sound_manager.music_next()

    def setup_main_menu(self):
        """Crée les éléments du menu principal."""
        menu = Menu()
        menu.add_widget(Image(0, 0, 1, ".\\assets\\textures\\Title_Screen.png", "title_screen_image", False, 2))

        btn_base_image = pygame.image.load("assets/textures/GUI/button_1.png").convert_alpha()
        btn_hover_image = pygame.image.load("assets/textures/GUI/button_2.png").convert_alpha()

        slider_base_image = pygame.image.load("assets/textures/GUI/slider_cursor_1.png").convert_alpha()
        slider_hover_image = pygame.image.load("assets/textures/GUI/slider_cursor_2.png").convert_alpha()
        slider_rail_image = pygame.image.load("assets/textures/GUI/slider_rail_1.png").convert_alpha()

        menu.add_widget(Button(0.5, 0.4, "Play", 0.08, (0, 0, 0), self.play_button_callback, btn_base_image, btn_hover_image, "play_button", True, 0))

        self.menu_manager.register_menu(menu, "main")

        self.menu_manager.show("main")
    
        self.create_boss_temple_area()


    def create_boss_temple_area(self):
        """Enregistre les zones d'entrées de boss fight."""
        self.event_sheduler.register_area((3104, 608, 48, 16), lambda _: print("temple 1"), ["player"], True)
        self.event_sheduler.register_area((4544, 592, 48, 16), lambda _: print("temple 2"), ["player"], True)
        self.event_sheduler.register_area((5664, 688, 32, 16), lambda _: print("temple 3"), ["player"], True)
        self.event_sheduler.register_area((6720, 720, 16, 32), lambda _: print("temple 4"), ["player"], True)

    def create_player_entity(self):
        """Crée une entité joueur."""

        # On crée l'entité
        player = self.entity_manager.register_entity("player")
        
        # On crée les animations
        anim = Anim(0.5, player)
        anim.load_animation_from_directory("assets/textures/entities/player/none")
        self.renderer.register_animation(anim, "player_none")

        anim = Anim(0.1, player)
        anim.load_animation_from_directory("assets/textures/entities/player/walking")
        self.renderer.register_animation(anim, "player_walking")

        player.link_animation("player_none")
        player.collision_rect = [-6, -7, 6, 16]
        player.death_result = EntityDeathResult.RESET_LIFE
        player.death_callback = self.create_player_entity

        self.entity_manager.set_player_entity("player")

        player.shadow = "player_shadow"
        self.renderer.register_shadow("assets/textures/entities/player/shadow.png", "player_shadow")

        # On définit ses attributs
        player.set_default_life(15)
        player.max_speed = 64.0
        player.x = 220.
        player.y = 767.

        # On place la caméra au niveau du joueur
        self.camera.x = player.x
        self.camera.y = player.y
        self.camera.target_x = player.x
        self.camera.target_y = player.y

        # On enregistre l'entité
        self.entity_manager.set_player_entity("player")

        self.camera.follow_entity(player)

    def spawn_mobs(self):
        """Fait apparaitre les mobs de la map."""

        mob = self.entity_manager.register_entity("wolf1")

        anim = Anim(0.5, mob)
        anim.load_animation_from_directory("assets/textures/entities/wolf/none")
        self.renderer.register_animation(anim, "wolf_none")

        
        mob.set_ai(WolfAI, self)

        mob.link_animation("wolf_none")
        mob.collision_rect = [-15, -7, 12, 7]

        mob.set_default_life(5)
        mob.max_speed = 60.

        mob.x, mob.y = 1600, 16



    def load_boss_fight_assets(self):
        """Charge les animations de combat des combats de boss."""
        player_none = Anim(1)
        player_none.load_animation_from_directory("assets/textures/boss_fight/player_big/none")
        self.renderer.register_boss_fight_player_animation(player_none, "none")
        boss_none = Anim(1)
        boss_none.load_animation_from_directory("assets/textures/boss_fight/boss_sprite/test/none")
        self.renderer.register_boss_fight_boss_animation(boss_none, "none")

        self.renderer.boss_fight_GUI_container = pygame.image.load("assets/textures/boss_fight/fight_actions_GUI.png").convert_alpha()


game = Game()
game.loop()
