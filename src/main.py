import pygame.image

from src.custom_AI import WolfAI
from src.engine.animation import Anim
from src.engine.engine import Engine
from src.engine.enums import GameState, EntityDeathResult
from src.engine.menu_manager import Menu, Label, Button, Slider, Image
from pygame.locals import FULLSCREEN, RESIZABLE

class Game(Engine):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption("The Forest's Secret")
        icon = pygame.image.load("assets\\textures\\icon.png")
        pygame.display.set_icon(icon)
        self.map_manager.load_new("maps/map5.tmj")

        self.renderer.load_tile_set("assets/textures/tileset.png", 16)
        self.dialogs_manager.load_dialogs("assets/dialogs.json")

        self.create_player_entity()
        self.setup_boss_fight()
        self.spawn_mobs()

        self.DEBUG_MODE = False

        self.game_state = GameState.MAIN_MENU

        self.renderer.dialogs_box = pygame.image.load("assets/textures/GUI/dialogs_box.png").convert_alpha()

        self.sound_manager.music_add_to_playlist(".\\assets\\OST\\boss_fight_1.mp3")
        self.sound_manager.music_start_playlist()

        self.setup_main_menu()

    def start_game(self):
        self.game_state = GameState.NORMAL
        self.settings_manager.set_screen_resolution(max_res=True)
        self.settings_manager.set_screen_mode(FULLSCREEN)
        self.renderer.fadein(1, (0, 0, 0), 100, True)

    def play_button_callback(self):
        self.renderer.fadeout(1, (0, 0, 0), 100, True, self.start_game)
        self.menu_manager.hide()

        self.sound_manager.music_remove_from_playlist(".\\assets\\OST\\boss_fight_1.mp3")
        self.sound_manager.music_add_to_playlist(".\\assets\\OST\\forest_sound.mp3")
        self.sound_manager.music_next()

    def setup_main_menu(self):
        """Crée les éléments du menu principal."""
        menu = Menu()
        menu.add_widget(Image(0, 0, 1, ".\\assets\\textures\\title_screen\\Title Screen.png", "title_screen_image", False, 2))
        menu.add_widget(Image(0.09, 0.05, 1, ".\\assets\\textures\\title_screen\\Word The.png", "title_screen_word_the", False, 2))
        menu.add_widget(Image(0.3, 0.1, 1, ".\\assets\\textures\\title_screen\\Word Forest.png", "title_screen_word_forest", False, 2))
        menu.add_widget(Image(0.54, 0.06, 1, ".\\assets\\textures\\title_screen\\Word 's.png", "title_screen_word_'s'", False, 2))
        menu.add_widget(Image(0.62, 0.05, 1, ".\\assets\\textures\\title_screen\\Word Secret.png", "title_screen_word_secret", False, 2))

        btn_base_image = pygame.image.load("assets/textures/Button Play.png").convert_alpha()
        btn_hover_image = pygame.image.load("assets/textures/Button Play Hovered.png").convert_alpha()


        menu.add_widget(Button(0.5, 0.4, "", 0.03, (0, 0, 0), self.play_button_callback, btn_base_image, btn_hover_image, "play_button", True, 0))

        self.menu_manager.register_menu(menu, "main")

        self.menu_manager.show("main")
    
        self.create_boss_temple_area()


    def create_boss_temple_area(self):
        """Enregistre les zones d'entrées de boss fight."""
        self.event_sheduler.register_area((3104, 608, 48, 16), lambda _: self.boss_fight_manager.enter_boss_fight(1),
                                          ["player"], True)
        self.event_sheduler.register_area((4544, 592, 48, 16), lambda _: self.boss_fight_manager.enter_boss_fight(2),
                                          ["player"], True)
        self.event_sheduler.register_area((5664, 688, 32, 16), lambda _: self.boss_fight_manager.enter_boss_fight(3),
                                          ["player"], True)
        self.event_sheduler.register_area((6720, 720, 16, 32), lambda _: self.boss_fight_manager.enter_boss_fight(4),
                                          ["player"], True)
        self.event_sheduler.register_area((591, 358, 98, 46), lambda _: self.boss_fight_manager.player_at_door(),
                                          ["player"], False, True)
        
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
        player.max_speed = 64. # Default = 64.0
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

    def setup_boss_fight(self):
        """Charge les animations de combat des combats de boss."""
        player_none = Anim(1)
        player_none.load_animation_from_directory("assets/textures/boss_fight/player_big/none")
        self.renderer.register_boss_fight_player_animation(player_none, "none")
        boss_none = Anim(1)
        boss_none.load_animation_from_directory("assets/textures/boss_fight/boss_sprite/test/none")
        self.renderer.register_boss_fight_boss_animation(boss_none, "none")

        self.renderer.boss_fight_GUI_container = pygame.image.load("assets/textures/boss_fight/fight_actions_GUI.png").convert_alpha()

        # On crée les boss
        self.boss_fight_manager.register_fight_data(1, "Greg", 15, 1)
        self.boss_fight_manager.register_fight_data(2, "Mark", 18, 2)
        self.boss_fight_manager.register_fight_data(3, "Steve", 20, 3)
        self.boss_fight_manager.register_fight_data(4, "The ultra-supra boss", 25, 4)


game = Game()
game.loop()
