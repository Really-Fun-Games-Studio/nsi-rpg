class SettingsManager:
    def __init__(self) -> None:
        self.master_volume = 60
        self.sound_master_volume = 100
        self.music_master_volume = 100
        self.sound_global_master_volume = 100

        self.zoom = 1.75
    

    def get_music_master_volume(self):
        return round(self.master_volume / 100 * self.music_master_volume, 3)
    
    def get_sound_global_master_volume(self):
        return round(self.master_volume / 100 * self.sound_global_master_volume, 3)
    
    def get_sound_master_volume(self):
        return round(self.master_volume / 100 * self.sound_master_volume, 3)


