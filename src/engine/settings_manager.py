from src.engine import engine
from src.engine.menu_manager import Menu, Slider, Label, Image, Button
from src.engine.enums import GameState
from pygame.locals import FULLSCREEN, RESIZABLE
import pygame


class SettingsManager:
    def __init__(self, engine: 'engine.Engine', default_master_volume: float, default_zoom: float) -> None:

        self.engine = engine
        self.menu_is_displaying = False
        self.menu_background_opacity = 55
        self.menu_fade_time = 0.3

        self.screen_max_resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.screen_resolution = (1280, 720)
        self.screen_mode = RESIZABLE
        self.screen_resolution_list = [(854, 480), (1280, 720), (1366, 768), (1920, 1080), (2560, 1440), (3840, 2160), (7680, 4320), self.screen_max_resolution] # 16:9

        self.refresh_rate_list = [10, 30, 60, -1]
        self.refresh_rate = -1



        self.latency_precision = 100 # Nombre de valeurs de latence stocké (Pour faire la moyenne)
        self.master_volume = default_master_volume
        self.sound_master_volume = 100
        self.music_master_volume = 100
        self.sound_global_master_volume = 100

        self.zoom = default_zoom

        self.setup_menu()
    
    def get_menu_background_opacity(self):
        return round(self.menu_background_opacity / 100 * 255)
    
    def setup_menu(self):
        """Crée les éléments du menu de paramètre"""
        menu = Menu()

        menu.add_widget(Label(0, 0.2, "Paramètres", 0.05, (192,192,192), True, 0))

        base_image = pygame.image.load("assets\\textures\\GUI\\slider_cursor_1.png")
        hover_image = pygame.image.load("assets\\textures\\GUI\\slider_cursor_2.png")
        rail_image = pygame.image.load("assets\\textures\\GUI\\slider_rail_212p.png")

        menu.add_widget(Button(0, 0, "Quit Game", 0.05, (192, 192, 192), self.quit_game, base_image, hover_image, "menu_quit_game_button", True, 2, "menu_quit_game_button_area"))


        menu.add_widget(Slider((0.03, 0.03), (0.3, 0.4), 0.054, base_image, hover_image, rail_image, "menu_fps_rail",
                               self.set_refresh_rate, 0, "menu_fps_slider_area"))
        
        menu.add_widget(Label(0.35, 0.35, self.get_refresh_rate_text(), 0.02, (192, 192, 192), "menu_fps_text", True, 0))
        self.engine.menu_manager.register_menu(menu, "settings_menu")


        base_image2 = pygame.image.load("assets\\textures\\GUI\\slider_cursor_1.png")
        hover_image2 = pygame.image.load("assets\\textures\\GUI\\slider_cursor_2.png")
        rail_image2 = pygame.image.load("assets\\textures\\GUI\\slider_rail_600p.png")

        menu.add_widget(Slider((0.03, 0.03), (0.4, 0.1), 0.166, base_image2, hover_image2, rail_image2, "menu_screen_res_rail", 
                               self.menu_set_screen_resolution, 0, "menu_screen_res_rail_area"))
        
        menu.add_widget(Label(0.45, 0.45, self.get_screen_resolution_text(), 0.02, (192, 192, 192), "menu_screen_res_text", True, 0))


    def __show_menu_callback(self):
        self.engine.menu_manager.show("settings_menu")
        self.menu_is_displaying = True

    def show_menu(self):
        self.engine.entity_manager.pause(True)
        self.engine.renderer.fadeout(self.menu_fade_time, (0, 0, 0), self.menu_background_opacity, callback=self.__show_menu_callback)
    
    def hide_menu(self):
        self.engine.renderer.fadein(self.menu_fade_time, (0, 0, 0), self.menu_background_opacity, callback=self.engine.entity_manager.resume)
        self.engine.menu_manager.hide()
        self.menu_is_displaying = False

    def get_refresh_rate(self):
        return self.refresh_rate
    
    def get_refresh_rate_text(self):
        refresh_rate = self.get_refresh_rate()

        if refresh_rate == -1:
            refresh_rate = "Illimités"
        
        return f"FPS : {refresh_rate}"
    
    def set_refresh_rate(self, value: float):
        if len(self.refresh_rate_list) == 0:
            self.refresh_rate = -1
        else:
            chunk = 1 / len(self.refresh_rate_list)
            cur_chunk = chunk
            for val in self.refresh_rate_list:
                if value <= cur_chunk:
                    self.refresh_rate = val
                    break
                else:
                    cur_chunk += chunk

        self.engine.menu_manager.get_widgets_at_name("settings_menu", "menu_fps_text")[0].text = self.get_refresh_rate_text()
    
    def menu_set_screen_resolution(self, value: float):
        if len(self.screen_resolution_list) == 0:
            self.set_screen_resolution(max_res=True)
        else:
            chunk = 1 / len(self.screen_resolution_list)
            cur_chunk = chunk
            for val in self.refresh_rate_list:
                if value <= cur_chunk:
                    self.refresh_rate = val
                    break
                else:
                    cur_chunk += chunk
        print(value)
        return
    
    def set_screen_resolution(self, res: tuple[int, int] = None, max_res: bool = False):
        if max_res:
            self.screen_resolution = self.screen_max_resolution
        else:
            self.screen_resolution = res

        self.engine.renderer.set_display(self.get_screen_mode(), self.screen_resolution)
    
    def set_screen_mode(self, mode: FULLSCREEN | RESIZABLE):
        self.screen_mode = mode

        self.engine.renderer.set_display(self.screen_mode, self.get_screen_resolution())
    
    def get_screen_resolution_text(self):
        res = self.get_screen_resolution()
        return f"{res[0]} x {res[1]}"
    
    def get_screen_resolution(self):
        return self.screen_resolution
    
    def get_screen_mode(self):
        return self.screen_mode

    def quit_game(self):
        print("Thanks for playing !")
        self.engine.running = False



    def get_zoom(self):
        return self.zoom
    
    def get_music_master_volume(self):
        return round(self.master_volume / 100 * self.music_master_volume, 3)
    
    def get_sound_global_master_volume(self):
        return round(self.master_volume / 100 * self.sound_global_master_volume, 3)
    
    def get_sound_master_volume(self):
        return round(self.master_volume / 100 * self.sound_master_volume, 3)