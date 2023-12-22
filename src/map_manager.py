import json


class MapManager:
    """Stocke les cartes du jeu."""
    def __init__(self):
        # structure : [layers[chunks[x, y]{width, height, data [tiles id]}]
        self.map_layers = []

    def load_new(self, file_path: str):
        """Charge une map infinie au format tiled."""
        with open(file_path, "r") as file:
            data = json.loads(file.read())
            for layer in data["layers"]:
                self.map_layers.append(layer["chunks"])

        print(self.map_layers)

    def get_tile_at(self, x: int, y: int, layer: int):
        """Done l'id de la tile aux coordonnées données et à la couche choisie."""
        return