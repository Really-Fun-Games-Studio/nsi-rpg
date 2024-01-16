from src.engine import engine
from src.engine.menu_manager import Menu, Slider, Label, Image
import pygame

class SettingsManager:
    def __init__(self, engine: 'engine.Engine', default_master_volume: float, default_zoom: float) -> None:

        self.engine = engine
        self.menu_is_displaying = False

        self.refresh_rate_list = [-1, 10, 30, 60]
        self.refresh_rate = -1


        self.latency_precision = 100 # Nombre de valeurs de latence stocké (Pour faire la moyenne)
        self.master_volume = default_master_volume
        self.sound_master_volume = 100
        self.music_master_volume = 100
        self.sound_global_master_volume = 100

        self.zoom = default_zoom

        self.setup_menu()
    
    def get_refresh_rate(self):
        return self.refresh_rate
    
    def get_refresh_rate_text(self):
        refresh_rate = self.get_refresh_rate()

        if refresh_rate == -1:
            refresh_rate = "Illimités"
        
        return f"FPS : {refresh_rate}"
    
    def set_refresh_rate(self, value: float):
        if value == 0:
            self.refresh_rate = self.refresh_rate_list[0]
        else:
            chunk = 1 / len(self.refresh_rate_list)
            cur_chunk = 0
            for val in self.refresh_rate_list:
                if value <= cur_chunk:
                    self.refresh_rate = val
                    break
                else:
                    cur_chunk += chunk

        self.engine.menu_manager.get_widgets_at_name("settings", "fps_text")[0].text = self.get_refresh_rate_text()

    def setup_menu(self):
        """Crée les éléments du menu de paramètre"""
        menu = Menu()
        menu.add_widget(Image(0, 0, 1, ".\\assets\\textures\\Settings_menu.png", "settings_menu_image", False, 2))

        menu.add_widget(Label(0, 0.2, "Paramètres", 0.05, (192,192,192), True, 0))

        base_image = pygame.image.load("assets\\textures\\GUI\\slider_cursor_1.png")
        hover_image = pygame.image.load("assets\\textures\\GUI\\slider_cursor_2.png")
        rail_image = pygame.image.load("assets\\textures\\GUI\\slider_rail_1.png")

        menu.add_widget(Slider((0.5, 0.5), (0.3, 0.4), 0.1, base_image, hover_image, rail_image, "fps",
                               self.set_refresh_rate, 0))
        
        menu.add_widget(Label(0.35, 0.35, self.get_refresh_rate_text(), 0.02, (192, 192, 192), "fps_text", True, 0))
        self.engine.menu_manager.register_menu(menu, "settings")

    def show_menu(self):
        self.engine.entity_manager.pause(True)
        self.engine.renderer.fadeout(0.5, (0, 0, 0), 60, callback=self.__show_menu_callback)
        
    
    def __show_menu_callback(self):
        self.engine.menu_manager.show("settings")
        self.menu_is_displaying = True
    
    def hide_menu(self):
        self.engine.renderer.fadein(0.5, (0, 0, 0), 60, callback=self.engine.entity_manager.resume)
        self.engine.menu_manager.hide()
        self.menu_is_displaying = False

    def get_zoom(self):
        return self.zoom
    
    def get_music_master_volume(self):
        return round(self.master_volume / 100 * self.music_master_volume, 3)
    
    def get_sound_global_master_volume(self):
        return round(self.master_volume / 100 * self.sound_global_master_volume, 3)
    
    def get_sound_master_volume(self):
        return round(self.master_volume / 100 * self.sound_master_volume, 3)


