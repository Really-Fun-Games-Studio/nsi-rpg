import json


class DialogsManager:
    """Classe qui gère la lecture des dialogues."""
    def __init__(self):
        self.current_dialogs = []
        self.current_dialog_id = -1
        self.dialogs = {}
        self.reading_dialog = False
        self.current_dialogue_letter_id = 0
        self.writing_dialog = False

        self.LETTER_WRITING_DELAY = 0.02
        self.letter_timer = 0

    def next_signal(self):
        """Fonction exécutée lorsque l'utilisateur demande de passer au prochain dialogue. Si un dialogue est en
        train d'être écrit, il écrit tout d'un coup."""

        if self.writing_dialog:
            self.current_dialogue_letter_id = len(self.current_dialogs[self.current_dialog_id])
            self.writing_dialog = False
        else:
            self.next_dialog()

    def next_dialog(self):
        """Passe au dialogue suivant. Renvoie True si le dialogue est fini."""
        self.current_dialog_id += 1
        if self.current_dialog_id == len(self.current_dialogs):
            self.current_dialogs = []
            self.current_dialog_id = -1
            self.writing_dialog = False
            self.reading_dialog = False

    def start_dialog(self, name: str):
        """Lance le dialogue au nom donné."""
        if not self.reading_dialog:
            self.current_dialogs = self.dialogs[name]
            self.current_dialog_id = 0

            self.reading_dialog = True

    def get_current_dialog_sentence(self, progressive=True) -> str:
        """Renvoie la phrase actuelle du dialogue."""
        if progressive:
            return self.current_dialogs[self.current_dialog_id][:self.current_dialogue_letter_id]
        else:
            return self.current_dialogs[self.current_dialog_id]

    def load_dialogs(self, file_path: str):
        """Charge les dialogues du jeu grave au fichier json donné."""
        with open(file_path, "r", encoding="utf-8") as file:
            self.dialogs = json.loads(file.read())

    def update(self, delta: float):
        """Met à jour e gestionnaire de dialogues."""
        if self.reading_dialog:
            self.letter_timer -= delta

            self.writing_dialog = True

            if self.letter_timer <= 0:
                self.letter_timer = self.LETTER_WRITING_DELAY
                self.current_dialogue_letter_id += 1
                if self.current_dialogue_letter_id > len(self.current_dialogs[self.current_dialog_id]):
                    self.current_dialogue_letter_id -= 1
                    self.writing_dialog = False

