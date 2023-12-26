from src.engine import engine
from src.engine.enums import GameState


class BossFightManager:
    def __init__(self, core: "engine.Engine"):
        self.boss_name = "none"
        self.engine = core

    def update(self):
        if self.engine.game_state == GameState.BOSS_FIGHT:
            pass
