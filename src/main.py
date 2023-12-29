import pygame.image

from src.engine.animation import Anim
from src.engine.engine import Engine
from src.engine.enums import GameState


class Game(Engine):
    def __init__(self):
        super().__init__()
        self.map_manager.load_new("maps/map5.tmj")

        self.renderer.load_tile_set("assets/textures/tileset.png", 16)

        self.create_player_entity()
        self.load_boss_fight_assets()

        self.DEBUG_MODE = False

        self.game_state = GameState.NORMAL

    def create_player_entity(self):
        """Crée une entité joueur."""
        anim = Anim(0.5)
        anim.load_animation_from_directory("assets/textures/entities/player/none")
        self.renderer.register_animation(anim, "player_none")

        anim = Anim(0.1)
        anim.load_animation_from_directory("assets/textures/entities/player/walking")
        self.renderer.register_animation(anim, "player_walking")

        player = self.entity_manager.register_entity("player")
        player.link_animation("player_none")
        player.collision_rect = [-6, -7, 6, 16]

        player.set_default_life(10)
        player.max_speed = 1.

        self.entity_manager.set_player_entity("player")

        player.shadow = "player_shadow"
        self.renderer.register_shadow("assets/textures/entities/player/shadow.png", "player_shadow")

        self.camera.follow_entity(player)

    def load_boss_fight_assets(self):
        """Charge les animations de combat des combats de boss."""
        player_none = Anim(1)
        player_none.load_animation_from_directory("assets/textures/boss_fight/player_big/none")
        self.renderer.register_boss_fight_player_animation(player_none, "none")
        boss_none = Anim(1)
        boss_none.load_animation_from_directory("assets/textures/boss_fight/boss_sprite/test/none")
        self.renderer.register_boss_fight_boss_animation(boss_none, "none")

        self.renderer.boss_fight_GUI_container = pygame.image.load("assets/textures/boss_fight/fight_actions_GUI.png")


game = Game()
game.loop()
