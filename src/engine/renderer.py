import math
import random

from pygame import display, image, surface, transform, draw, font
from pygame.locals import RESIZABLE, SRCALPHA, FULLSCREEN

import src.engine.engine as engine
from src.engine.animation import Anim
from src.engine.enums import GameState
from src.engine.menu_manager import Label, Button


class Renderer:
    """Classe contenant le moteur de rendu. On utilise, pour cela la bibliothèque Pygame."""

    def __init__(self, core: 'engine.Engine'):
        self.engine = core
        self.window_type = RESIZABLE
        self.window_size = (display.Info().current_w, display.Info().current_h) if self.window_type == FULLSCREEN else (
        600, 600)
        self.window = display.set_mode(self.window_size, self.window_type)
        self.tiles = []
        self.tile_size = 0
        self.animations: dict[str: Anim] = {}

        # Variables utilisées pour les combats de boss
        self.boss_fight_boss_animations: dict[str: Anim] = {}
        self.boss_fight_player_animations: dict[str: Anim] = {}
        self.boss_fight_GUI_container = None

        # Boite de dialogue
        self.dialogs_box = None

        # Ombres d'entités
        self.shadows = {}

        # Particules affichées
        self.particles = []

    def emit_particles(self, x: int, y: int, w: int, h: int, count: int, min_size: int, max_size: int,
                       min_speed: float, max_speed: float, min_life_time: float, max_life_time: float,
                       color: tuple[int, int, int]):
        """Emmet des particules aux coordonnées données dans un rectangle de demi-largeur {w} et de demi-hauteur {h}."""
        for _ in range(count):
            # On choisit la taille de la particule
            part_size = random.randint(min_size, max_size)

            # On choisit sa vitesse en x et en y
            part_speed_x = random.uniform(min_speed, max_speed)

            # On inverse la vitesse de manière aléatoire
            if random.randint(0, 1) == 1:
                part_speed_x = - part_speed_x
            part_speed_y = random.uniform(min_speed, max_speed)
            if random.randint(0, 1) == 1:
                part_speed_y = - part_speed_y

            # On choisit sa position dans le rectangle
            part_x = random.randint(x - w, x + w - part_size)
            part_y = random.randint(y - h, y + h - part_size)

            # On choisit la durée de vie
            part_life_time = random.uniform(min_life_time, max_life_time)

            # On ajoute la particule dans la liste des particules
            # Le 0 correspond au temps de vie depuis la création de la particule
            self.particles.append([part_x, part_y, part_size, part_speed_x, part_speed_y, 0., part_life_time, color])

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
            self.render_particles(rendered_surface, delta)
            self.render_layer(2, rendered_surface)
            self.render_debug_area(rendered_surface)

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

        # Rend les menus
        self.render_menus()

        # Conteur de FPS en mode DEBUG
        if self.engine.DEBUG_MODE:
            self.window.blit(font.SysFont("Arial", 20).render(f"FPS: {self.engine.clock.get_fps()}", True, (255, 0, 0)),
                             (0, 0))
            player = self.engine.entity_manager.get_by_name('player')
            self.window.blit(font.SysFont("Arial", 20).render(f"X: {player.x} Y:{player.y}",
                                                              True, (255, 0, 0)), (0, 30))
            self.window.blit(font.SysFont("Arial", 20).render(f"Zoom: {self.engine.camera.zoom}",
                                                              True, (255, 0, 0)), (0, 60))

            # On rend maintenant toutes les zones de détection de la fenêtre
            for area in self.engine.event_handler.buttons_area:
                window_size = display.get_window_size()
                if area[2] == 0:
                    draw.rect(self.window, (255, 255, 0),
                              (area[0][0] * window_size[0], area[0][1] * window_size[0],
                               area[0][2] * window_size[0], area[0][3] * window_size[0]), width=1)
                elif area[2] == 1:
                    draw.rect(self.window, (255, 255, 0),
                              (area[0][0] * window_size[1], area[0][1] * window_size[1],
                               area[0][2] * window_size[1], area[0][3] * window_size[1]), width=1)
                elif area[2] == 2:
                    draw.rect(self.window, (255, 255, 0),
                              (area[0][0] * window_size[0], area[0][1] * window_size[1],
                               area[0][2] * window_size[0], area[0][3] * window_size[1]), width=1)
                else:
                    draw.rect(self.window, (255, 255, 0),
                              area[0], width=1)

        # Rendu présent dans tous les types de jeu
        self.render_dialogs_box()

        # Apres avoir tout rendu, on met à jour l'écran
        display.update()

    def render_menus(self):
        """Rend le menu enregistré comme visible."""
        window_size = display.get_window_size()

        # Si un menu est affiché, on itère dans tous ses widgets
        if self.engine.menu_manager.active_menu is not None:
            for widget in self.engine.menu_manager.active_menu.widgets:
                # On multiplie les coordonnées par la taille de la fenetre si besoin
                if widget.is_window_relative == 0:
                    x = widget.x * window_size[0]
                    y = widget.y * window_size[0]
                elif widget.is_window_relative == 1:
                    x = widget.x * window_size[1]
                    y = widget.y * window_size[1]
                elif widget.is_window_relative == 2:
                    x = widget.x * window_size[0]
                    y = widget.y * window_size[1]
                else:
                    x = widget.x
                    y = widget.y

                # On vérifie quel est le widget
                if isinstance(widget, Label):
                    # On multiplie la taille du texte si besoin
                    if widget.is_window_relative == 0:
                        size = widget.size*window_size[0]
                    elif widget.is_window_relative == 1:
                        size = widget.size*window_size[1]
                    elif widget.is_window_relative == 2:
                        size = widget.size*min(window_size[0], window_size[1])
                    else:
                        size = widget.size

                    text_font = font.SysFont("Arial", round(size))
                    rendered_text = text_font.render(widget.text, True, widget.color)
                    if widget.centered:
                        self.window.blit(rendered_text, (x-rendered_text.get_width()//2,
                                                         y-rendered_text.get_height()//2))
                    else:
                        self.window.blit(rendered_text, (x, y))
                elif isinstance(widget, Button):
                    # On multiplie la taille du texte si besoin
                    if widget.is_window_relative == 0:
                        size = widget.size*window_size[0]
                    elif widget.is_window_relative == 1:
                        size = widget.size*window_size[1]
                    elif widget.is_window_relative == 2:
                        size = widget.size*min(window_size[0], window_size[1])
                    else:
                        size = widget.size

                    text_font = font.SysFont("Arial", round(size))

                    rendered_text = text_font.render(widget.text, True, widget.color)

                    if widget.hovered:
                        btn_image = widget.base_image
                    else:
                        btn_image = widget.hover_image
                    btn_image = transform.scale(btn_image, (btn_image.get_width()*window_size[0]/self.window_size[0],
                                                            btn_image.get_height()*window_size[0]/self.window_size[0]))

                    # On affiche l'image du boutton
                    if widget.centered:
                        self.window.blit(btn_image, (x-btn_image.get_width()//2,
                                                     y-btn_image.get_height()//2))

                        self.window.blit(rendered_text, (x-rendered_text.get_width()//2,
                                                         y-rendered_text.get_height()//2))

                    else:
                        self.window.blit(btn_image, (x, y))

                        self.window.blit(rendered_text, (x, y))

    def render_dialogs_box(self):
        """Rend la boite de dialogue lorsqu'un dialogue est lancé."""

        # Rend le conteneur des dialogues
        if self.engine.dialogs_manager.reading_dialog:
            resized_box = transform.scale(self.dialogs_box,
                                          (display.get_window_size()[0],
                                           self.dialogs_box.get_height() / self.dialogs_box.get_width() *
                                           display.get_window_size()[0]))
            self.window.blit(resized_box, (0, display.get_window_size()[1] - resized_box.get_height()))

            # Rend le texte

            # On récupère le texte
            sentence = self.engine.dialogs_manager.get_current_dialog_sentence()

            # On crée la font qui permettra de faire le rendu du texte après
            text_font = font.SysFont("Arial", display.get_window_size()[0]//30)

            # On calcule la taille du décalage puis on calcule la largeur maximale que peut faire une ligne
            x_border = display.get_window_size()[0]/30
            max_width = display.get_window_size()[0]-2*x_border

            # On passe le texte dans un algorithme qui coupe le texte entre les espaces pour empecher de dépacer la
            # taille maximale de la ligne
            lines = []
            current_line = ""
            for i in sentence:
                current_line += i
                # Si on déplace de la ligne, on ajoute la ligne jusqu'au dernier mot
                if text_font.size(current_line)[0] > max_width:
                    lines.append(current_line[:current_line.rfind(" ")])
                    current_line = current_line[current_line.rfind(" "):]

            # Si la ligne est incomplète, on ajoute la ligne
            lines.append(current_line)

            # On itère dans les lignes avec un enumerate pour avoir sont index
            for i in enumerate(lines):
                # On récupère le texte et s'il commence par un espace, on le retire
                text = i[1]
                if len(text) > 0 and text[0] == " ":
                    text = text[1:]

                # On rend la ligne au bon endroit sur l'écran
                rendered_text = text_font.render(text, True, (0, 0, 0))
                self.window.blit(rendered_text,
                                 (x_border,
                                  display.get_window_size()[1] - resized_box.get_height() +
                                  display.get_window_size()[0]/30 +
                                  (text_font.get_height()+display.get_window_size()[0]/200)*i[0]))

    def render_debug_area(self, rendered_surface: surface.Surface):
        """Rend les zones de collisions et de détections quand le mode DEBUG est activé."""

        # On calcule le décalage pour centrer la caméra
        x_middle_offset = display.get_window_size()[0] / 2 / self.engine.camera.zoom
        y_middle_offset = display.get_window_size()[1] / 2 / self.engine.camera.zoom

        # On itère et on rend toutes les zones de détection
        for area in self.engine.event_sheduler.area_callbacks:
            area_rect = area[0]
            draw.rect(rendered_surface, (200, 100, 0),
                      (math.floor(x_middle_offset + area_rect[0] - self.engine.camera.x),
                       math.floor(y_middle_offset + area_rect[1] - self.engine.camera.y),
                       math.floor(area_rect[2]), math.floor(area_rect[3])), width=1)

    def register_shadow(self, file_path: str, name: str):
        """Enregistre une image d'ombre utilisée pour le rendu des entités."""
        shadow = image.load(file_path).convert_alpha()
        self.shadows[name] = shadow

    def register_animation(self, animation: Anim, name: str):
        """Enregistre une animation."""
        self.animations[name] = animation

    def register_boss_fight_boss_animation(self, animation: Anim, name: str):
        """Ajoute une animation pour le boss lors d'un combat de boss."""
        self.boss_fight_boss_animations[name] = animation

    def register_boss_fight_player_animation(self, animation: Anim, name: str):
        """Ajoute une animation pour le joueur lors d'un combat de boss."""
        self.boss_fight_player_animations[name] = animation

    def render_particles(self, rendered_surface: surface.Surface, delta: float):
        """Update et rend les particules."""
        x_middle_offset = display.get_window_size()[0] / 2 / self.engine.camera.zoom
        y_middle_offset = display.get_window_size()[1] / 2 / self.engine.camera.zoom

        for part in self.particles.copy():
            part_dest = (math.floor(part[0] - self.engine.camera.x + x_middle_offset),
                         math.floor(part[1] - self.engine.camera.y + y_middle_offset))

            draw.rect(rendered_surface, part[7], part_dest + (part[2], part[2]))
            part[5] += delta
            part[0] += part[3]
            part[1] += part[4]
            if part[5] > part[6]:
                self.particles.remove(part)

    def render_boss_fight_scene(self, delta: float):
        """Rend les sprites du joueur et du boss lors d'un combat de boss."""

        # On récupère l'image de l'animation du boss
        boss_animation: Anim = self.boss_fight_boss_animations[self.engine.boss_fight_manager.current_boss_animation]
        frame = boss_animation.get_frame(delta)

        # On redimensionne l'image
        frame = transform.scale(frame, (display.get_window_size()[0] / 5, display.get_window_size()[0] / 5))

        # On colle le boss à droite de la fenêtre
        self.window.blit(frame, (display.get_window_size()[0] - frame.get_width() - display.get_window_size()[0] / 20,
                                 display.get_window_size()[1] / 4 - frame.get_height() / 2))

        # On récupère l'image de l'animation du joueur
        player_animation = self.boss_fight_player_animations[self.engine.boss_fight_manager.current_player_animation]
        frame = player_animation.get_frame(delta)

        # On redimensionne l'image
        frame = transform.scale(frame, (display.get_window_size()[0] / 5, display.get_window_size()[0] / 5))

        # On colle le joueur à gauche de la fenêtre
        self.window.blit(frame,
                         (display.get_window_size()[0] / 20, display.get_window_size()[1] / 4 - frame.get_height() / 2))

    def render_boss_fight_gui(self):
        """Rend la barre d'action en bas de l'écran pendant le combat de boss."""

        resized_container = transform.scale(self.boss_fight_GUI_container,
                                            (display.get_window_size()[0],
                                             self.boss_fight_GUI_container.get_height() / self.boss_fight_GUI_container.get_width() *
                                             display.get_window_size()[0]))
        self.window.blit(resized_container, (0, display.get_window_size()[1] - resized_container.get_height()))

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

            # On flip l'image horizontalement si l'entité est retournée
            if entity.direction == 1:
                frame = transform.flip(frame, True, False)

            # On calcule les coordonnées de rendu de l'entité
            entity_dest = (math.floor(entity.x - self.engine.camera.x + x_middle_offset - frame.get_width() / 2),
                           math.floor(entity.y - self.engine.camera.y + y_middle_offset - frame.get_height() / 2))

            # On récupert l'ombre de l'entité
            if entity.shadow is not None:
                shadow_image = self.shadows[entity.shadow]
                # On rend l'ombre
                rendered_surface.blit(shadow_image, entity_dest)

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
                life_bar_dest = (
                math.floor((entity.x - self.engine.camera.x + x_middle_offset) * self.engine.camera.zoom -
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

        # On précalcule le décallage des tiles sur l'écran
        tile_x_offset = - self.engine.camera.x + x_middle_offset
        tile_y_offset = - self.engine.camera.y + y_middle_offset

        # On itère pour chaque couche, toutes les tiles visibles par la caméra
        for x in range(x_map_offset, x_map_offset + x_map_range):
            # On précalcule les coordonnées en x
            tile_render_x = math.floor(x * self.tile_size + tile_x_offset)
            for y in range(y_map_offset, y_map_offset + y_map_range):

                # On récupère l'id de la tile à la position donnée
                tile_id = self.engine.map_manager.get_tile_at_quick(x, y, layer_id)

                # Si l'id est 0, il s'agit de vide donc on saute le rendu
                if tile_id == 0:
                    continue

                # Puis, on cherche à quelle image elle correspond et on la colle sur notre surface
                rendered_surface.blit(self.tiles[tile_id - 1],
                                      (tile_render_x,
                                       math.floor(y * self.tile_size + tile_y_offset)))

                if self.engine.DEBUG_MODE and layer_id == 1:
                    draw.rect(rendered_surface, (100, 100, 255),
                              (math.floor(x * self.tile_size - self.engine.camera.x + x_middle_offset),
                               math.floor(y * self.tile_size - self.engine.camera.y + y_middle_offset),
                               self.tile_size, self.tile_size), width=1)
