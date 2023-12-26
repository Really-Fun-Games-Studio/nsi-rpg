import random

from src.engine.animation import Anim
from src.engine.engine import Engine


class Game(Engine):
    def __init__(self):
        super().__init__()
        self.map_manager.load_new("maps/map2.tmj")

        self.renderer.load_tile_set("assets/textures/tiles.png", 16)

        anim = Anim(0.5)
        anim.load_animation_from_directory("assets/textures/entities/player/none")
        self.renderer.register_animation(anim, "player_none")

        player = self.entity_manager.register_entity("player")
        player.link_animation("player_none")
        player.collision_rect = [-7, -7, 7, 7]

        player.set_default_life(10)

        self.camera.follow_entity(player)

        for i in range(20):
            anim = Anim(0.5)
            anim.load_animation_from_directory("assets/textures/entities/player/none")
            self.renderer.register_animation(anim, f"player_none_{i}")

            test = self.entity_manager.register_entity(f"test_{i}")
            test.x = random.randint(0, 200)
            test.y = random.randint(0, 200)
            test.link_animation(f"player_none_{i}")
            test.collision_rect = [-7, -7, 7, 7]

            test.set_default_life(10)


game = Game()
game.loop()
