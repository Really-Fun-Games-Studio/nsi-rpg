from src.engine.entity import Entity
from src.engine.mobs_AI import MobAI


class WolfAI(MobAI):
    def __init__(self, entity: Entity):
        super().__init__(entity)

    def update(self):
        self.entity.x += 1
