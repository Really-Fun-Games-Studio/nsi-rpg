import json


class MapManager:
    """Stocke les cartes du jeu."""
    def __init__(self):
        # structure : [layers{chunks[x, y][data]}
        self.map_layers = []
        self.chunk_width = 16
        self.chunk_height = 16

    def load_new(self, file_path: str):
        """Charge une map infinie au format tiled."""
        with open(file_path, "r") as file:
            data = json.loads(file.read())
            for layer in data["layers"]:
                chunks = {}
                for chunk in layer["chunks"]:
                    chunks[(chunk["x"]//self.chunk_width, chunk["y"]//self.chunk_height)] = chunk["data"]
                self.map_layers.append(chunks)

        print(self.map_layers)

    def get_tile_at(self, x: int, y: int, layer_id: int):
        """Donne l'id de la tile aux coordonnées données et à la couche choisie."""

        # On récupère la couche demandée
        layer = self.map_layers[layer_id]

        # On calcule les coordonées du chunk
        coordinates = (x//self.chunk_width, y//self.chunk_height)

        # On transforme les coordonnées globales en coordonnées dans le chunk
        x %= 16
        y %= 16

        if coordinates not in layer:
            return 0

        chunk = layer[coordinates]

        # On vérifie que la tile demandée existe sinon on répond "vide"
        if x >= self.chunk_width or x < 0 or y >= self.chunk_height or y < 0:
            return 0

        # On calcule l'index et on renvoie la tile
        return chunk[x+y*self.chunk_width]
