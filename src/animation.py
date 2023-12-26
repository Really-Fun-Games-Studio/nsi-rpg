# Classe animation adaptée depuis ESG Engine :
# https://github.com/yannis300307/ESG_Engine/blob/main/ESG_Engine/client/animation.py
import os

import pygame


class Anim:
    """Une animation contenant les images pygame et le temps entre chaque frames."""
    def __init__(self, change_frame_time: float):
        self.frames = []
        self.change_frame_time = change_frame_time  # Delay entre chaque frames
        self.current_frame = 0
        self.time = 0

    def add_frame(self, frame: pygame.Surface):
        """Enregistre une nouvelle image dans la liste des frames."""
        self.frames.append(frame.convert_alpha())

    def get_frame_nbr(self):
        """Renvoie le nombre d'images enregistrées."""
        return len(self.frames)

    def get_frame(self, delta: float):
        """Donne l'image courante de l'animation."""
        # Avant de retourner l'image, on met à jour le delay
        self.update_current_frame(delta)

        return self.frames[self.current_frame]

    def update_current_frame(self, delta: float):
        """Met à jour le delay de l'image courante avec le delta time."""
        self.time += delta

        # Si le delay entre deux images est écoulé, on incrémente le numéro de l'image et on remet le temps à 0
        if self.time >= self.change_frame_time:
            self.current_frame += 1
            self.time = 0

            # Si on sort de la liste d'images, on revient au début
            if self.current_frame >= len(self.frames):
                self.current_frame = 0

    def get_specific_frame(self, base: int):
        """Donne la {base} ème image apres l'image courante."""
        # Si le delay entre deux images est écoulé, on incrémente le numéro de l'image et on remet le temps à 0
        if self.time >= self.change_frame_time:
            self.current_frame += 1
            self.time = 0

            # Si on sort de la liste d'images, on revient au début
            if self.current_frame >= len(self.frames):
                self.current_frame = 0

        return self.frames[(self.current_frame + base) % len(self.frames)]

    def load_animation_from_directory(self, path: str):
        """Récupère toutes les images au format png dans un dossier et les enregistre comme frames de l'animation."""

        # On récupère tous les fichiers dans le dossier donné
        files = os.listdir(path)

        # Si ils sont bien en PNG, on les enregistre
        for file in files:
            if file.endswith(".png"):
                self.add_frame(pygame.image.load(path + os.sep + file))
