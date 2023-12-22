from pygame import display, image

import src.engine as engine


class Renderer:
    """Classe contenant le moteur de rendu. On utilise, pour cela la bibliothèque Pygame."""
    def __init__(self, core: 'engine.Engine'):
        self.engine = core
        self.window = display.set_mode((600, 600))
        self.tiles = []

    def load_tile_set(self, file_path: str, tile_size: int):
        """Charge le jeu de tuiles en utilisant le fichier donné et la taille donnée."""
        tile_set = image.load(file_path).convert_alpha()

        # Scan tout le tile set et le découpe pour créer des tiles de {tile_size} px de hauteur et de largeur
        for y in range(tile_set.get_height()//tile_size):
            for x in range(tile_set.get_width()//tile_size):
                tile = tile_set.subsurface((x*tile_size, y*tile_size, tile_size, tile_size))
                self.tiles.append(tile)
        print(self.tiles)

    def update(self):
        """Fait le rendu du jeu."""
        self.window.fill((255, 255, 255))

        self.render_map()

        display.update()

    def render_map(self):
        x_offset = 0
        y_offset = 0

        for i in range(4):
            self.window.blit(self.tiles[i], (i*16, 0))

        self.rendered_surface = None

