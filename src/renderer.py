import math

from pygame import display, image, surface, transform, draw
from pygame.locals import RESIZABLE

import src.engine as engine
from src.animation import Anim


class Renderer:
    """Classe contenant le moteur de rendu. On utilise, pour cela la bibliothèque Pygame."""

    def __init__(self, core: 'engine.Engine'):
        self.engine = core
        self.window = display.set_mode((600, 600), RESIZABLE)
        self.tiles = []
        self.tile_size = 0
        self.animations: dict[str: Anim] = {}

    def load_tile_set(self, file_path: str, tile_size: int):
        """Charge le jeu de tuiles en utilisant le fichier donné et la taille donnée."""
        tile_set = image.load(file_path).convert_alpha()

        self.tile_size = tile_size

        # Scan tout le tile set et le découpe pour créer des tiles de {tile_size} px de hauteur et de largeur
        for y in range(tile_set.get_height() // tile_size):
            for x in range(tile_set.get_width() // tile_size):
                tile = tile_set.subsurface((x * tile_size, y * tile_size, tile_size, tile_size))
                self.tiles.append(tile)

    def update(self):
        """Fait le rendu du jeu."""
        self.window.fill((255, 255, 255))

        # On crée une surface temporaire qui nous permettra de faire le rendu à l'échelle 1:1
        rendered_surface_size = (display.get_window_size()[0] / self.engine.camera.zoom,
                                 display.get_window_size()[1] / self.engine.camera.zoom)
        rendered_surface = surface.Surface(rendered_surface_size)

        self.renderer_layer(0, rendered_surface)
        self.render_entities(rendered_surface)
        self.renderer_layer(1, rendered_surface)
        self.renderer_layer(2, rendered_surface)

        # Enfin, on redimensionne notre surface et on la colle sur la fenêtre principale
        self.window.blit(
            transform.scale(rendered_surface, (math.ceil(rendered_surface_size[0] * self.engine.camera.zoom),
                                               math.ceil(rendered_surface_size[1] * self.engine.camera.zoom))),
            (0, 0))

        # Apres avoir tout rendu, on met à jour l'écran
        display.update()

    def register_animation(self, animation: Anim, name: str):
        """Enregistre une animation."""
        self.animations[name] = animation

    def render_entities(self, rendered_surface: surface.Surface):
        """Rend toutes les entités."""
        # On calcule le décalage pour centrer la caméra
        x_middle_offset = display.get_window_size()[0] / 2 / self.engine.camera.zoom
        y_middle_offset = display.get_window_size()[1] / 2 / self.engine.camera.zoom

        for entity in self.engine.entity_manager.get_all_entities():
            # On récupère la frame courante de l'animation
            anim: Anim = self.animations[entity.animation_name]
            frame = anim.get_frame(0.01666667)

            # On calcule les coordonnées de rendu de l'entité
            player_dest = (entity.x - self.engine.camera.x + x_middle_offset - frame.get_width() / 2,
                           entity.y - self.engine.camera.y + y_middle_offset - frame.get_height() / 2)

            # On affiche l'image
            rendered_surface.blit(frame, player_dest)

            if self.engine.DEBUG_MODE:
                top_let_corner_x = entity.x - self.engine.camera.x + x_middle_offset
                top_let_corner_y = entity.y - self.engine.camera.y + y_middle_offset

                draw.rect(rendered_surface, (255, 0, 0),
                          (top_let_corner_x + entity.collision_rect[0],
                           top_let_corner_y + entity.collision_rect[1],
                           entity.collision_rect[2] - entity.collision_rect[0],
                           entity.collision_rect[3] - entity.collision_rect[1]),
                          width=1)

    def renderer_layer(self, layer_id: int, rendered_surface: surface.Surface):
        """Rend la map."""
        # On calcule le nombre de tiles à mettre sur notre écran en prenant en compte le zoom
        x_map_range = int(display.get_window_size()[0] / self.tile_size / self.engine.camera.zoom) + 2
        y_map_range = int(display.get_window_size()[1] / self.tile_size / self.engine.camera.zoom) + 2

        # On calcule le décalage pour centrer la caméra
        x_middle_offset = display.get_window_size()[0] / 2 / self.engine.camera.zoom
        y_middle_offset = display.get_window_size()[1] / 2 / self.engine.camera.zoom

        # On calcule le décalage du début de rendu des tiles
        x_map_offset = int((self.engine.camera.x - x_middle_offset) / self.tile_size)
        y_map_offset = int((self.engine.camera.y - y_middle_offset) / self.tile_size)

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
