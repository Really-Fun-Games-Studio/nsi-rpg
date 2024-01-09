class Settings:
    def __init__(self) -> None:
        self.master_volume = 60
        self.music_volume = 100

        self.zoom = 1.75
    

    def get_music_volume(self):
        return self.master_volume / 100 * self.music_volume
    