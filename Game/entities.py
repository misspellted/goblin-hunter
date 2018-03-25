import pygame

from collision import HitBox
from dimensioning import Dimensioned
from positioning import Positioned, PositionChangedListener

class Entity(Positioned, Dimensioned):
    def __init__(self, x, y, length, height):
        Positioned.__init__(self, x, y)
        Dimensioned.__init__(self, length, height)

class CollidableEntity(Entity, PositionChangedListener):
    def __init__(self, x, y, length, height):
        Entity.__init__(self, x, y, length, height)
        PositionChangedListener.__init__(self)
        self.addPositionChangedListener(self)
        self.hitBox = HitBox(x, y, length, height)

    def adjustHitBox(self, xOffset, yOffset, lengthOffset, heightOffset):
        self.hitBox.x += xOffset
        self.hitBox.y += yOffset
        self.hitBox.length += lengthOffset
        self.hitBox.height += heightOffset

    def onXChanged(self, last, current):
        self.hitBox.x += current - last

    def onYChanged(self, last, current):
        self.hitBox.y += current - last

    def collidesWith(self, collidableEntity):
        collides = False

        if not collidableEntity is None:
            collides = self.hitBox.collidesWith(collidableEntity.hitBox)

        return collides

    def showHitBox(self, surface):
        self.hitBox.draw(surface)
