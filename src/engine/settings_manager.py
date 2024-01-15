class SettingsManager:
    def __init__(self, default_master_volume: float, default_zoom: float) -> None:
        self.refresh_rate = 30
        self.latency_precision = 100 # Nombre de valeurs de latence stocké (Pour faire la moyenne)
        self.master_volume = default_master_volume
        self.sound_master_volume = 100
        self.music_master_volume = 100
        self.sound_global_master_volume = 100

        self.zoom = default_zoom
    
    def get_refresh_rate(self):
        return self.refresh_rate
        
    def get_zoom(self):
        return self.zoom
    
    def get_music_master_volume(self):
        return round(self.master_volume / 100 * self.music_master_volume, 3)
    
    def get_sound_global_master_volume(self):
        return round(self.master_volume / 100 * self.sound_global_master_volume, 3)
    
    def get_sound_master_volume(self):
        return round(self.master_volume / 100 * self.sound_master_volume, 3)


