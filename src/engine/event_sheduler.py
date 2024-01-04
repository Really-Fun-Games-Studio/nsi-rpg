from types import FunctionType


class EventSheduler:
    """Gère le lancement d'évenements avec des conditions."""
    def __init__(self):
        self.area_callbacks = []

    def register_area(self, area_rect: tuple[int, int, int, int], callback: FunctionType | classmethod | staticmethod):
        self.area_callbacks.append((area_rect, callback))

    def update(self):
        for area in self.area_callbacks:
            area_rect = area[0]