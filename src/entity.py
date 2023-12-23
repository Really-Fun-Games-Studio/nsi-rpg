class Entity:
    """Classe permettant de gérer les entités. Créée automatiquement par `EntityManager.register_entity()`"""
    def __init__(self, name: str):
        self.x = 8
        self.y = 8

        # Time utilisé pour les IA
        self.time = 0

        self.name = name

        self.animation_name = None

    def update(self, delta: float):
        """Met à jour l'entité."""
        # self.x += 1

        self.time += delta

    def link_animation(self, name: str):
        self.animation_name = name
