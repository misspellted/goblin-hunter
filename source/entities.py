import pygame

from collision import HitBox
from dimensioning import Dimensioned
from positioning import Positioned
from vectors import VectorXObserver, VectorYObserver

class Entity(Positioned, Dimensioned):
    def __init__(self, x, y, length, height):
        Positioned.__init__(self, x, y)
        Dimensioned.__init__(self, length, height)
        # TODO: Investigate implementing positioning ranges of some sort...
        self.minimumXPosition = None
        self.maximumXPosition = None
        self.minimumYPosition = None
        self.maximumYPosition = None

    def setMinimumXPosition(self, minimumXPosition):
        self.minimumXPosition = minimumXPosition

    def setMaximumXPosition(self, maximumXPosition):
        self.maximumXPosition = maximumXPosition

    def setMinimumYPosition(self, minimumYPosition):
        self.minimumYPosition = minimumYPosition

    def setMaximumYPosition(self, maximumYPosition):
        self.maximumYPosition = maximumYPosition

class CollidableEntity(Entity, VectorXObserver, VectorYObserver):
    def __init__(self, x, y, length, height):
        Entity.__init__(self, x, y, length, height)
        self.addXObserver(self)
        self.addYObserver(self)
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

class EntityContainer(Entity):
    def __init__(self, x, y, length, height):
        Entity.__init__(self, x, y, length, height)
        self.entities = list()

    def addEntity(self, entity):
        if isinstance(entity, Entity) and not entity in self.entities:
            # Set the ranges on the X and Y position components.
            entity.setMinimumXPosition(self.x)
            entity.setMaximumXPosition(self.x + self.length - entity.length)
            entity.setMinimumYPosition(self.y)
            entity.setMaximumYPosition(self.y + self.height - entity.height)

            self.entities.append(entity)

    def removeEntity(self, entity):
        if isinstance(entity, Entity) and entity in self.entities:
            self.entities.remove(entity)
