from dino_runner.utils.constants import HEART, SHIELD_TYPE
from dino_runner.components.power_ups.power_up import PowerUp


class Heart(PowerUp):
    def __init__(self):
        self.image = HEART
        self.type = SHIELD_TYPE
        super().__init__(self.image, self.type)