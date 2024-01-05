import json


class DialogsManager:
    """Classe qui gère la lecture des dialogues."""
    def __init__(self):
        self.current_dialogs = []
        self.current_dialog_id = -1
        self.dialogs = {}
        self.reading_dialog = False

    def next_dialog(self):
        """Passe au dialogue suivant. Renvoie True si le dialogue est fini."""
        self.current_dialog_id += 1
        if self.current_dialog_id == len(self.current_dialogs):
            self.current_dialogs = []
            self.current_dialog_id = -1
            self.reading_dialog = False

    def start_dialog(self, name: str):
        """Lance le dialogue au nom donné."""
        if not self.reading_dialog:
            self.current_dialogs = self.dialogs[name]
            self.current_dialog_id = 0

            print(self.current_dialogs)

            self.reading_dialog = True

    def get_current_dialog_sentence(self) -> str:
        """Renvoie la phrase actuelle du dialogue."""
        return self.current_dialogs[self.current_dialog_id]

    def load_dialogs(self, file_path: str):
        """Charge les dialogues du jeu grave au fichier json donné."""
        with open(file_path, "r", encoding="utf-8") as file:
            self.dialogs = json.loads(file.read())
