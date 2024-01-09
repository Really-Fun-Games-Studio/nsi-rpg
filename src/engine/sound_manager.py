from src.engine.entity import Entity
from random import randint
from pygame import mixer
from math import sqrt
from time import time

class SoundManager:
    def __init__(self, music_base_volume: float, ):
        self.__tick = 0 # Compteur de la valeur d'un tick (Utilisé pour le comptage de tick)
        self.tick = 0 # Compteur de tick
        self.time = 0 # Temps local a la class (en s)

        self.music_playlist = []
        self.music_current_song = ""
        self.music_play_playlist = False
        self.music_current_index = 0
        self.music_shuffle_playlist = True
        self.music_next_request = False
        self.music_set_volume(music_base_volume)

        self.music_before_pause_pos = 0
        self.music_before_pause_song = ""
        self.music_is_paused = False
        self.music_pos_delay = 0

        self.sound_currently_playing = {float: [mixer.Sound, float, [float, float], float]} # Format {unique_id : [Sound, max_volume, [pos_x, pos_y], stop_at]}

        self.sound_loaded = {str: mixer.Sound} # Format : {name: mixer.Sound}
        self.sound_global_currently_playing = {float: [mixer.Sound, float, float]} # Format {unique_id: [Sound, volume, stop_at]}
        

        self.sound_hears_anchor = None


    def update(self, delta: float):
        self.__tick += delta
        self.tick = int(self.__tick / delta)
        self.time = self.tick * delta

        if self.sound_hears_anchor: # Update la position des "Oreilles" du joueur (Ou de l'entité séléctionné comme ancre pour les oreilles)
            self.sound_hears_x = self.sound_hears_anchor.x
            self.sound_hears_y = self.sound_hears_anchor.y

        for key in self.sound_global_currently_playing.keys(): # Son globaux
            if self.sound_global_currently_playing[key][2] > self.time:
                self.sound_global_currently_playing.pop(key)

        for key in self.sound_currently_playing.keys(): # Son locaux
            if self.sound_currently_playing[key][3] > self.time: # Timeout des sons
                self.sound_currently_playing.pop(key)

            else: # Gère le volume en fonction de la position
                sound = self.sound_currently_playing[key][0]
                max_volume = self.sound_currently_playing[key][1]
                pos_x, pos_y = self.sound_currently_playing[2]
                sound.set_volume(max(0, int((max_volume / 100) - sqrt((pos_x - self.sound_hears_x) ** 2 + (pos_y - self.sound_hears_y) ** 2))) / (max_volume / 100))

        if self.music_play_playlist and not self.music_is_paused: # Musique de fond
            if not mixer.music.get_busy() or self.music_next_request:
                if self.music_next_request:
                    self.music_next_request = False
                    mixer.music.fadeout(1)

                if len(self.music_playlist) == 0:
                    pass
                elif self.music_current_song == "":
                    self.__music_play(self.music_playlist[0])
                else:
                    if self.music_current_song in self.music_playlist:
                        just_played_index = self.music_playlist.index(self.music_current_song)

                        if self.music_shuffle_playlist and len(self.music_playlist) != 1:
                            while True:
                                new_index = randint(0, len(self.music_playlist) - 1)
                                if new_index != just_played_index:
                                    break

                            self.music_current_index = new_index
                            self.__music_play(self.music_playlist[new_index])

                        elif len(self.music_playlist) - 1 <= just_played_index: # Dernier son de la playlist / la playlist a rétréci entre temps
                            self.music_current_index = 0
                            self.__music_play(self.music_playlist[0]) # Recommence depuis le début de la playlist

                        else:
                            self.music_current_index = just_played_index + 1
                            self.__music_play(self.music_playlist[self.music_current_index]) # Joue la musique suivante dans la playlist

                    else: # Song removed from playlist, no idea what was the index, starting again from start or from random index if playlist_shuffle = True
                        new_index = randint(0, len(self.music_playlist) - 1)
                        self.music_current_index = new_index
                        self.__music_play(self.music_playlist[new_index])


    def music_get_volume(self):
        return mixer.music.get_volume() * 100

    def music_set_volume(self, new_volume: float):
        """Définit le nouveau volume de la musique"""
        mixer.music.set_volume((round(new_volume / 100, 3)))
    
    def music_pause(self, fade_s: float, restart_tolerance: float = 33):
        """Met en pause la musique, la musique reprendra à la fin de la musique moin la tolérance (en pourcentage)"""
        self.music_is_paused = True
        self.music_before_pause_pos = self.music_get_current_song_pos() + fade_s * restart_tolerance / 100 # Récupère la position a laquelle le son doit reprendre lors du .resume()
        self.music_before_pause_song = self.music_current_song
        
        mixer.music.fadeout(fade_s * 1000)

    def music_resume(self, fade_s: float):
        self.__music_play(self.music_before_pause_song, fade_s, self.music_before_pause_pos)
        self.music_before_pause_pos = 0
        self.music_before_pause_song = ""

    def music_get_current_song_pos(self):
        if mixer.music.get_busy():
            return round(mixer.music.get_pos() /1000 + self.music_pos_delay, 3)
        else:
            return round(self.music_before_pause_pos, 3)
    
    def __music_play(self, song: str, fade_s: float = 0, start_at: float = 0):
        mixer.music.unload()
        mixer.music.load(song)
        mixer.music.play(0, start_at, fade_s * 1000)

        self.music_is_paused = False
        self.music_current_song = song
        self.music_pos_delay = start_at

    def music_add_to_playlist(self, song_path: str):
        self.music_playlist.append(song_path)
    
    def music_remove_from_playlist(self, song_path: str = None, index: int = None):
        if song_path:
            index = self.music_playlist.index(song_path)
        if index:
            self.music_playlist.pop(index)

    def music_start_playlist(self):
        self.music_play_playlist = True
    
    def music_stop_playlist(self):
        self.music_play_playlist = False
    
    def music_playlist_set_shuffle(self, shuffle: bool):
        self.music_shuffle_playlist = shuffle

    def music_next(self):
        self.music_next_request = True

    def sound_link_hears(self, entity: Entity):
        self.sound_hears_anchor = entity
    
    def create_unique_id(self):
        return time()*10e99999

    def sound_load(self, file_path: str, name: str):
        self.sound_loaded[name] = mixer.Sound(file_path)
    
    def sound_play(self, name: str, max_volume: float, pos_x: float, pos_y: float):
        sound = self.sound_loaded[name]
        stop_at = stop_at = self.time + sound.get_length()

        self.sound_currently_playing[self.create_unique_id()] = [sound, max_volume, [pos_x, pos_y], stop_at] # Format {unique_id : [Sound, max_volume, [pos_x, pos_y], stop_at]


    def sound_global_play(self, name: str, volume: float):
        """Joue un son avec le même son dans tout le monde"""
        sound = self.sound_loaded[name]
        sound.set_volume(round(volume / 100, 3))

        stop_at = self.time + sound.get_length()
        self.sound_global_currently_playing[self.create_unique_id()] = [sound, volume, stop_at]
        sound.play()
    
    def sound_global_stop(self, name: str, all: bool = False):
        if all:
            for key in self.sound_global_currently_playing.keys():
                self.sound_global_currently_playing.pop(key)[0].stop()