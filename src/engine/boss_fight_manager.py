from src.engine import engine
from src.engine.enums import GameState


class BossFightManager:
    """Classe permettant de gérer les combats de boss."""
    def __init__(self, core: "engine.Engine"):
        self.boss_name = "none"
        self.engine = core

        self.current_boss_animation = "none"
        self.current_player_animation = "none"

    def update(self):
        """Met à jour le combat de boss."""
        if self.engine.game_state == GameState.BOSS_FIGHT:
            pass
