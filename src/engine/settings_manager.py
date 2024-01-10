class SettingsManager:
    def __init__(self, default_master_volume: float, default_zoom: float) -> None:
        self.master_volume = default_master_volume
        self.sound_master_volume = 100
        self.music_master_volume = 100
        self.sound_global_master_volume = 100

        self.zoom = default_zoom
    
    def get_zoom(self):
        return self.zoom
    
    def get_music_master_volume(self):
        return round(self.master_volume / 100 * self.music_master_volume, 3)
    
    def get_sound_global_master_volume(self):
        return round(self.master_volume / 100 * self.sound_global_master_volume, 3)
    
    def get_sound_master_volume(self):
        return round(self.master_volume / 100 * self.sound_master_volume, 3)


