from settings import *
import math
from entity import BaseEntity
from bullet import Bullet


class AnotherPlayer(BaseEntity):
    def __init__(self, app, name='player'):
        super().__init__(app, name)
        self.group.change_layer(self, CENTER.y)
        self.rect = self.image.get_rect(center=CENTER)
        self.id=" "
        self.offset = vec2(0)
        self.inc = vec2(0)
        self.prev_inc = vec2(0)
        self.angle = 0
        self.diag_move_corr = 1 / math.sqrt(2)


    def update(self):
        super().update()
