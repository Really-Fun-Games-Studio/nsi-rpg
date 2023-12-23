from pygame import display, image, surface, transform
from pygame.locals import RESIZABLE

import src.engine as engine


class Renderer:
    """Classe contenant le moteur de rendu. On utilise, pour cela la bibliothèque Pygame."""
    def __init__(self, core: 'engine.Engine'):
        self.engine = core
        self.window = display.set_mode((600, 600), RESIZABLE)
        self.tiles = []
        self.tile_size = 0

    def load_tile_set(self, file_path: str, tile_size: int):
        """Charge le jeu de tuiles en utilisant le fichier donné et la taille donnée."""
        tile_set = image.load(file_path).convert_alpha()

        self.tile_size = tile_size

        # Scan tout le tile set et le découpe pour créer des tiles de {tile_size} px de hauteur et de largeur
        for y in range(tile_set.get_height()//tile_size):
            for x in range(tile_set.get_width()//tile_size):
                tile = tile_set.subsurface((x*tile_size, y*tile_size, tile_size, tile_size))
                self.tiles.append(tile)
        #print(self.tiles)

    def update(self):
        """Fait le rendu du jeu."""
        self.window.fill((255, 255, 255))

        self.render_map()

        display.update()

    def render_map(self):
        # On calcule le nombre de tiles à mettre sur notre écran en prenant en compte le zoom
        x_map_range = int(display.get_window_size()[0] / 16 / self.engine.camera.zoom) + 2
        y_map_range = int(display.get_window_size()[1] / 16 / self.engine.camera.zoom) + 2

        # On calcule le décalage pour centrer la caméra
        x_middle_offset = display.get_window_size()[0] / 2 / self.engine.camera.zoom
        y_middle_offset = display.get_window_size()[0] / 2 / self.engine.camera.zoom

        # On calcule le décalage du début de rendu des tiles
        x_map_offset = int((self.engine.camera.x - x_middle_offset) / self.tile_size)
        y_map_offset = int((self.engine.camera.y - y_middle_offset) / self.tile_size)

        # On crée une surface temporaire qui nous permettra de la redimensionner
        rendered_surface_size = (x_map_range * self.tile_size, y_map_range * self.tile_size)
        rendered_surface = surface.Surface(rendered_surface_size)

        # On itère pour chaque couche, toutes les tiles visibles par la caméra
        for i in range(len(self.engine.map_manager.map_layers)):
            for x in range(x_map_offset, x_map_offset + x_map_range):
                for y in range(y_map_offset, y_map_offset + y_map_range):

                    # On récupère l'id de la tile à la position donnée
                    tile_id = self.engine.map_manager.get_tile_at(x, y, i)

                    # Si l'id est 0, il s'agit de vide donc on saute le rendu
                    if tile_id == 0:
                        continue

                    # Puis, on cherche à quelle image elle correspond et on la colle sur notre surface
                    rendered_surface.blit(self.tiles[tile_id-1],
                                          ((x*self.tile_size-self.engine.camera.x+x_middle_offset),
                                           (y*self.tile_size-self.engine.camera.y+y_middle_offset)))

        # Enfin, on redimensionne notre surface et on la colle sur la fenêtre principale
        self.window.blit(transform.scale(rendered_surface, (rendered_surface_size[0]*self.engine.camera.zoom, rendered_surface_size[1]*self.engine.camera.zoom)), (0, 0))

