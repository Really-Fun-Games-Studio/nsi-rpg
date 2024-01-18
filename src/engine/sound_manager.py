from pygame import mixer
from random import randint

class SoundManager:
    def __init__(self, music_base_volume: float):
        self.__tick = 0 # Compteur de la valeur d'un tick sur 1 (Utilisé pour le comptage de tick)
        self.time = 0 # Temps local a la class (en s)

        self.music_playlist = []
        self.music_current_song = ""
        self.music_play_playlist = False
        self.music_current_index = 0
        self.music_shuffle_playlist = True

        self.music_before_pause_pos = 0
        self.music_before_pause_song = ""
        self.music_is_paused = False
        self.music_next_request = False

        self.music_pos_delay = 0

        self.music_set_volume(music_base_volume)


    def update(self, delta: float):
        self.__tick += delta
        self.tick = int(self.__tick / delta)
        self.time = self.tick * delta

        if self.music_play_playlist and not self.music_is_paused: # Musique de fond
            if mixer.get_init() and (not mixer.music.get_busy() or self.music_next_request):
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
        if index != None:
            self.music_playlist.pop(index)

    def music_start_playlist(self):
        self.music_play_playlist = True
    
    def music_stop_playlist(self):
        self.music_play_playlist = False
    
    def music_playlist_set_shuffle(self, shuffle: bool):
        self.music_shuffle_playlist = shuffle

    def music_next(self):
        self.music_next_request = True
