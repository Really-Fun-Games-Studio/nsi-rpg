import pygame.image

from src.custom_AI import WolfAI
from src.engine.animation import Anim
from src.engine.engine import Engine
from src.engine.enums import GameState


class Game(Engine):
    def __init__(self):
        super().__init__()
        self.map_manager.load_new("maps/map5.tmj")

        self.renderer.load_tile_set("assets/textures/tileset.png", 16)
        self.dialogs_manager.load_dialogs("assets/dialogs.json")

        self.create_player_entity()
        self.load_boss_fight_assets()
        self.spawn_mobs()

        self.DEBUG_MODE = True

        self.game_state = GameState.NORMAL

        self.event_sheduler.register_area((0, 20, 20, 20), None)

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

        player.set_default_life(15)
        player.max_speed = 1.1

        self.entity_manager.set_player_entity("player")

        player.shadow = "player_shadow"
        self.renderer.register_shadow("assets/textures/entities/player/shadow.png", "player_shadow")

        self.camera.follow_entity(player)

    def spawn_mobs(self):
        """Fait apparaitre les mobs de la map."""

        anim = Anim(0.5)
        anim.load_animation_from_directory("assets/textures/entities/wolf/none")
        self.renderer.register_animation(anim, "wolf_none")

        mob = self.entity_manager.register_entity("wolf1")
        mob.set_ai(WolfAI, self)

        mob.link_animation("wolf_none")
        mob.collision_rect = [-15, -7, 12, 7]

        mob.set_default_life(5)
        mob.max_speed = 1.

        mob.x, mob.y = 160, 16

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
