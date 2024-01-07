from pygame import mixer

class SoundManager:
    def __init__(self, music_base_volume: float):
        self.__tick = 0 # Compteur de la valeur d'un tick sur 1 (Utilisé pour le comptage de tick)
        self.time = 0 # Temps local a la class (en s)

        self.music_playlist = []
        self.music_current_song = ""
        self.play_music_playlist = False

        self.music_before_pause_pos = 0
        self.music_before_pause_song = ""
        self.music_is_paused = False

        self.set_music_volume(music_base_volume)


        self.add_to_music_playlist("C:\\Users\\kerri\\Downloads\\Code\\NSI-RPG\\assets\\OST\\Lost Woods - The Legend of Zelda Ocarina of Time.mp3")
        self.add_to_music_playlist("C:\\Users\\kerri\\Downloads\\Code\\NSI-RPG\\assets\\OST\\Hyrule Field - The Legend of Zelda Ocarina of Time.mp3")
        self.start_music_playlist()


        self.do1 = True
        self.do2 = True

    

    def update(self, delta: float):
        self.__tick += delta
        self.tick = int(self.__tick / delta)
        self.time = self.tick * delta


        if self.play_music_playlist and not self.music_is_paused:
            if not mixer.music.get_busy():
                current_song_index = self.music_playlist.index(self.music_current_song)
                if len(self.music_playlist) == 0:
                    pass
                elif len(self.music_playlist) - 1 <= current_song_index:
                    self.__play_music(self.music_playlist[0]) # Recommence depuis le début de la playlist
                else:
                    self.__play_music(self.music_playlist[current_song_index + 1]) # Joue la musique suivante dans la playlist

                
        if self.time > 5 and self.do1:
            self.do1 = False
            self.pause_music(5)
        
        if self.time > 15 and self.do2:
            self.do2 = False
            self.resume_music(5)


    def get_music_volume(self):
        return mixer.music.get_volume() * 100

    def set_music_volume(self, new_volume: float):
        """Définit le nouveau volume de la musique"""
        mixer.music.set_volume((round(new_volume / 100, 3)))
    
    def pause_music(self, fade_s: float, restart_tolerance: float = 33):
        """Met en pause la musique, la musique reprendra à la fin de la musique moin la tolérance (en pourcentage)"""
        self.music_is_paused = True
        self.music_before_pause_pos = mixer.music.get_pos() / 1000 + fade_s * restart_tolerance / 100 # Récupère la position a laquelle le son doit reprendre lors du .resume()
        self.music_before_pause_song = self.music_current_song
        mixer.music.fadeout(fade_s * 1000)

    def resume_music(self, fade_s: float):
        self.__play(self.music_before_pause_song, fade_s, self.music_before_pause_pos)
        self.music_before_pause_pos = 0
        self.music_before_pause_song = ""

    def __play_music(self, song: str, fade_s: float = 0, start_at: float = 0):
        mixer.music.unload()
        mixer.music.load(song)
        mixer.music.play(0, start_at, fade_s * 1000)

        self.music_is_paused = False
        self.music_current_song = song

    def add_to_music_playlist(self, song_path: str):
        self.music_playlist.append(song_path)
    
    def remove_from_music_playlist(self, song_path: str = None, index: int = None):
        if song_path:
            index = self.music_playlist.index(song_path)
        if index:
            self.music_playlist.pop(index)

    def start_music_playlist(self):
        self.play_music_playlist = True
    
    def stop_music_playlist(self):
        self.play_music_playlist = False