import math

from pygame import display, image, surface, transform, draw
from pygame.locals import RESIZABLE, SRCALPHA, FULLSCREEN

import src.engine.engine as engine
from src.engine.animation import Anim
from src.engine.enums import GameState


class Renderer:
    """Classe contenant le moteur de rendu. On utilise, pour cela la bibliothèque Pygame."""

    def __init__(self, core: 'engine.Engine'):
        self.engine = core
        self.window_type = FULLSCREEN
        self.window_size = (display.Info().current_w, display.Info().current_h) if self.window_type == FULLSCREEN else (600, 600)
        self.window = display.set_mode(self.window_size, self.window_type)
        self.tiles = []
        self.tile_size = 0
        self.animations: dict[str: Anim] = {}

        # Variables utilisées pour les combats de boss
        self.boss_fight_boss_animations: dict[str: Anim] = {}
        self.boss_fight_player_animations: dict[str: Anim] = {}
        self.boss_fight_GUI_container = None

        # Variables utilisées par le menu principal
        self.main_menu_assets: dict[str: Anim] = {}

    def load_main_menu_assets(self, path: str):
        """Charge les assets du menu principal depuis le dossier donné."""

    def load_tile_set(self, file_path: str, tile_size: int):
        """Charge le jeu de tuiles en utilisant le fichier donné et la taille donnée."""
        tile_set = image.load(file_path).convert_alpha()

        self.tile_size = tile_size

        # Scan tout le tile set et le découpe pour créer des tiles de {tile_size} px de hauteur et de largeur
        for y in range(tile_set.get_height() // tile_size):
            for x in range(tile_set.get_width() // tile_size):
                tile = tile_set.subsurface((x * tile_size, y * tile_size, tile_size, tile_size))
                self.tiles.append(tile)

    def update(self, delta: float):
        """Fait le rendu du jeu."""
        self.window.fill((255, 255, 255))

        if self.engine.game_state == GameState.NORMAL:
            # On crée une surface temporaire qui nous permettra de faire le rendu à l'échelle 1:1
            rendered_surface_size = (display.get_window_size()[0] / self.engine.camera.zoom,
                                     display.get_window_size()[1] / self.engine.camera.zoom)
            rendered_surface = surface.Surface(rendered_surface_size)

            # On crée une surface qui sera ajoutée à la fenêtre apres rendered_surface pour pouvoir mettre des GUI
            gui_surface = surface.Surface(display.get_window_size(), SRCALPHA)
            gui_surface.fill((0, 0, 0, 0))

            self.render_layer(0, rendered_surface)
            self.render_layer(1, rendered_surface)
            self.render_entities(rendered_surface, gui_surface, delta)
            self.render_layer(2, rendered_surface)

            # Enfin, on redimensionne notre surface et on la colle sur la fenêtre principale
            self.window.blit(
                transform.scale(rendered_surface, (math.ceil(rendered_surface_size[0] * self.engine.camera.zoom),
                                                   math.ceil(rendered_surface_size[1] * self.engine.camera.zoom))),
                (0, 0))

            self.window.blit(gui_surface, (0, 0))

        elif self.engine.game_state == GameState.BOSS_FIGHT:
            self.window.fill((255, 230, 230))
            self.render_boss_fight_scene(delta)
            self.render_boss_fight_gui()

        # Apres avoir tout rendu, on met à jour l'écran
        display.update()

    def register_animation(self, animation: Anim, name: str):
        """Enregistre une animation."""
        self.animations[name] = animation

    def register_boss_fight_boss_animation(self, animation: Anim, name: str):
        """Ajoute une animation pour le boss lors d'un combat de boss."""
        self.boss_fight_boss_animations[name] = animation

    def register_boss_fight_player_animation(self, animation: Anim, name: str):
        """Ajoute une animation pour le joueur lors d'un combat de boss."""
        self.boss_fight_player_animations[name] = animation

    def render_boss_fight_scene(self, delta: float):
        """Rend les sprites du joueur et du boss lors d'un combat de boss."""

        # On récupère l'image de l'animation du boss
        boss_animation: Anim = self.boss_fight_boss_animations[self.engine.boss_fight_manager.current_boss_animation]
        frame = boss_animation.get_frame(delta)

        # On redimensionne l'image
        frame = transform.scale(frame, (display.get_window_size()[0] / 5, display.get_window_size()[0] / 5))

        # On colle le boss à droite de la fenêtre
        self.window.blit(frame, (display.get_window_size()[0]-frame.get_width()-display.get_window_size()[0]/20,
                                 display.get_window_size()[1]/4-frame.get_height()/2))

        # On récupère l'image de l'animation du joueur
        player_animation = self.boss_fight_player_animations[self.engine.boss_fight_manager.current_player_animation]
        frame = player_animation.get_frame(delta)

        # On redimensionne l'image
        frame = transform.scale(frame, (display.get_window_size()[0] / 5, display.get_window_size()[0] / 5))

        # On colle le joueur à gauche de la fenêtre
        self.window.blit(frame, (display.get_window_size()[0]/20, display.get_window_size()[1]/4-frame.get_height()/2))

    def render_boss_fight_gui(self):
        """Rend la barre d'action en bas de l'écran pendant le combat de boss."""

        resized_container = transform.scale(self.boss_fight_GUI_container, (display.get_window_size()[0], self.boss_fight_GUI_container.get_height()/self.boss_fight_GUI_container.get_width()*display.get_window_size()[0]))
        self.window.blit(resized_container, (0, display.get_window_size()[1]-resized_container.get_height()))

    def render_entities(self, rendered_surface: surface.Surface, gui_surface: surface.Surface, delta: float):
        """Rend toutes les entités."""
        # On calcule le décalage pour centrer la caméra
        x_middle_offset = display.get_window_size()[0] / 2 / self.engine.camera.zoom
        y_middle_offset = display.get_window_size()[1] / 2 / self.engine.camera.zoom

        for entity in self.engine.entity_manager.get_all_entities():
            # On récupère la frame courante de l'animation
            anim: Anim = self.animations[entity.animation_name]
            frame = anim.get_frame(delta)

            # Si l'entité n'apparait pas à l'écran, on passe son rendu
            if (entity.x - self.engine.camera.x + x_middle_offset + frame.get_width() < 0 or
                    entity.x - self.engine.camera.x - x_middle_offset - frame.get_width() > 0 or
                    entity.y - self.engine.camera.y + y_middle_offset + frame.get_height() < 0 or
                    entity.y - self.engine.camera.y - y_middle_offset - frame.get_height() > 0):
                continue

            # On calcule les coordonnées de rendu de l'entité
            entity_dest = (math.floor(entity.x - self.engine.camera.x + x_middle_offset - frame.get_width() / 2),
                           math.floor(entity.y - self.engine.camera.y + y_middle_offset - frame.get_height() / 2))

            # On affiche l'image
            rendered_surface.blit(frame, entity_dest)

            if entity.max_life_points != -1:
                # Rendu de la barre de vie des entités
                life_bar_width = 50
                life_bar_height = 8
                life_bar_y_offset = 5
                life_bar_border = 2

                life_bar_value = entity.life_points / entity.max_life_points
                cooldown_value = entity.damage_cooldown / entity.default_damage_cooldown

                # On calcule où placer la barre de vei sur la surface des GUI
                life_bar_dest = (math.floor((entity.x - self.engine.camera.x + x_middle_offset) * self.engine.camera.zoom -
                                            life_bar_width / 2),
                                 math.floor((entity.y - self.engine.camera.y + y_middle_offset - frame.get_height() / 2) *
                                            self.engine.camera.zoom - life_bar_height - life_bar_y_offset))

                # Contour de la barre de vie
                draw.rect(gui_surface, (20, 0, 0), (life_bar_dest[0] - life_bar_border,
                                                    life_bar_dest[1] - life_bar_border,
                                                    life_bar_width + life_bar_border * 2,
                                                    life_bar_height + life_bar_border * 2))

                # Barre de vie
                draw.rect(gui_surface, (255 - 255 * life_bar_value, 255 * life_bar_value, 0),
                          life_bar_dest + (life_bar_width * life_bar_value, life_bar_height))

                draw.rect(gui_surface, (200, 200, 200),
                          life_bar_dest + (life_bar_width * life_bar_value * cooldown_value, life_bar_height))

            if self.engine.DEBUG_MODE:
                top_let_corner_x = entity.x - self.engine.camera.x + x_middle_offset
                top_let_corner_y = entity.y - self.engine.camera.y + y_middle_offset

                draw.rect(rendered_surface, (255, 0, 0),
                          (top_let_corner_x + entity.collision_rect[0],
                           top_let_corner_y + entity.collision_rect[1],
                           entity.collision_rect[2] - entity.collision_rect[0],
                           entity.collision_rect[3] - entity.collision_rect[1]),
                          width=1)

    def render_main_menu(self):
        """Rend le menu principal du jeu."""

    def render_layer(self, layer_id: int, rendered_surface: surface.Surface):
        """Rend la map."""
        # On calcule le nombre de tiles à mettre sur notre écran en prenant en compte le zoom
        x_map_range = int(display.get_window_size()[0] / self.tile_size / self.engine.camera.zoom) + 2
        y_map_range = int(display.get_window_size()[1] / self.tile_size / self.engine.camera.zoom) + 2

        # On calcule le décalage pour centrer la caméra
        x_middle_offset = display.get_window_size()[0] / 2 / self.engine.camera.zoom
        y_middle_offset = display.get_window_size()[1] / 2 / self.engine.camera.zoom

        # On calcule le décalage du début de rendu des tiles
        x_map_offset = math.floor((self.engine.camera.x - x_middle_offset) / self.tile_size)
        y_map_offset = math.floor((self.engine.camera.y - y_middle_offset) / self.tile_size)

        # On itère pour chaque couche, toutes les tiles visibles par la caméra
        for x in range(x_map_offset, x_map_offset + x_map_range):
            for y in range(y_map_offset, y_map_offset + y_map_range):

                # On récupère l'id de la tile à la position donnée
                tile_id = self.engine.map_manager.get_tile_at(x, y, layer_id)

                # Si l'id est 0, il s'agit de vide donc on saute le rendu
                if tile_id == 0:
                    continue

                # Puis, on cherche à quelle image elle correspond et on la colle sur notre surface
                rendered_surface.blit(self.tiles[tile_id - 1],
                                      (math.floor(x * self.tile_size - self.engine.camera.x + x_middle_offset),
                                       math.floor(y * self.tile_size - self.engine.camera.y + y_middle_offset)))

                if self.engine.DEBUG_MODE and layer_id == 1:
                    draw.rect(rendered_surface, (100, 100, 255),
                              (math.floor(x * self.tile_size - self.engine.camera.x + x_middle_offset),
                               math.floor(y * self.tile_size - self.engine.camera.y + y_middle_offset),
                               self.tile_size, self.tile_size), width=1)
