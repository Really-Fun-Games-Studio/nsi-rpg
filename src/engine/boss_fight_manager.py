from src.engine import engine
from src.engine.enums import GameState


class BossFightManager:
    """Classe permettant de gérer les combats de boss."""
    def __init__(self, core: "engine.Engine"):
        self.boss_name = "none"
        self.engine = core

        self.current_boss_animation = "none"
        self.current_player_animation = "none"

        self.fights = {}
        self.current_fight_id = -1

        self.player_points = -1
        self.boss_points = -1

    def update(self):
        """Met à jour le combat de boss."""
        if self.engine.game_state == GameState.BOSS_FIGHT:
            pass

    def register_fight_data(self, fight_id: int, boss_name: str, total_concurrent_points: int, boss_damage_count: int):
        """Enregistre les données permettant de mettre en place le combat."""
        self.fights[fight_id] = [boss_name, total_concurrent_points, boss_damage_count]

    def enter_boss_fight(self, fight_id: int):
        """Entre dans le combat de boss donné."""
        self.current_fight_id = fight_id
        self.engine.sound_manager.music_pause(3)
        self.engine.renderer.fadeout(3, (0, 0, 0), 100, True, self.setup_fight)


    def setup_fight(self):
        """Met en place le combat."""

        # Change la musique
        self.engine.sound_manager.music_remove_from_playlist(".\\assets\\OST\\forest_sound.mp3")
        self.engine.sound_manager.music_add_to_playlist(".\\assets\\OST\\boss_fight_1.mp3")
        self.engine.sound_manager.music_start_playlist()
        volume = self.engine.sound_manager.music_get_volume()
        self.engine.sound_manager.music_set_volume(0)
        self.engine.sound_manager.music_resume(0)
        self.engine.sound_manager.music_next()
        self.engine.sound_manager.music_set_volume(volume)

        self.engine.entity_manager.pause()

        self.player_points = self.fights[self.current_fight_id][1]
        self.boss_points = self.fights[self.current_fight_id][1]

        self.engine.game_state = GameState.BOSS_FIGHT
