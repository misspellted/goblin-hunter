import pygame

from dimensioning import Dimensioned
from positioning import Positioned

class HitBox(Positioned, Dimensioned):
    def __init__(self, x, y, length, height):
        Positioned.__init__(self, x, y)
        Dimensioned.__init__(self, length, height)

    def collidesWith(self, hitBox):
        xCollides = False
        yCollides = False

        if not hitBox is None:
            xCollides = self.x < hitBox.x + hitBox.length and hitBox.x < self.x + self.length
            yCollides = self.y < hitBox.y + hitBox.height and hitBox.y < self.y + self.height

        return xCollides and yCollides

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.length, self.height), 2)
