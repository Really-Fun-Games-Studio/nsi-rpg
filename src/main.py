import random

from src.engine.animation import Anim
from src.engine.engine import Engine


class Game(Engine):
    def __init__(self):
        super().__init__()
        self.map_manager.load_new("maps/map3.tmj")

        self.renderer.load_tile_set("assets/textures/tiles.png", 16)

        anim = Anim(0.5)
        anim.load_animation_from_directory("assets/textures/entities/player/none")
        self.renderer.register_animation(anim, "player_none")

        player = self.entity_manager.register_entity("player")
        player.link_animation("player_none")
        player.collision_rect = [-7, -7, 7, 7]

        player.set_default_life(10)

        self.camera.follow_entity(player)

game = Game()
game.loop()
