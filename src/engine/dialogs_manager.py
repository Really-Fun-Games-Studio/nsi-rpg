import json


class DialogsManager:
    """Classe qui gère la lecture des dialogues."""
    def __init__(self):
        self.current_dialog = []
        self.dialogs = {}

    def load_dialogs(self, file_path: str):
        """Charge les dialogues du jeu grave au fichier json donné."""
        with open(file_path, "r") as file:
            self.dialogs = json.loads(file.read())
