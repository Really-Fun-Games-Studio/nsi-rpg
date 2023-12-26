from enum import Enum


class GameState(Enum):
    """Enumération utilisée pour définir l'état actuel du jeu."""
    NONE = 0
    NORMAL = 1
    BOSS_FIGHT = 2
    MAIN_MENU = 3
    # AJouter si besoin, mais à utiliser de préférence avec parsimony
