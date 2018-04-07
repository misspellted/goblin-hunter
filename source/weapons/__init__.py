import pygame

from affects import Affect
from entities import CollidableEntity
from vectors import VectorXY

class Projectile(CollidableEntity):
    def __init__(self, x, y, radius, color, facing, source=None):
        diameter = radius * 2

        CollidableEntity.__init__(self, x, y, diameter, diameter)
        self.adjustHitBox(-radius, -radius, 0, 0)

        self.radius = radius
        self.color = color

        self.velocity = VectorXY(8 * facing, 0)

        self.source = source

    def move(self):
        self.x += self.velocity.x
        self.y += self.velocity.y

    def draw(self,win):
        # pygame.draw.circle requires integer positioning (at least, on Ubuntu 17.10/Python 2.7/PyGame 1.9.3)
        position = (int(self.x), int(self.y))
        pygame.draw.circle(win, self.color, position, self.radius)

#        self.showHitBox(win)

class Reloading(Affect):
    def __init__(self, duration):
        Affect.__init__(self, duration)

    def update(self):
        if self.isActive():
            self.coolDown -= 1

class Gun(object):
    def __init__(self, reloadingDuration):
        self.reloading = None
        self.reloadingDuration = reloadingDuration

    def pointLeft(self):
        self.direction = -1

    def pointRight(self):
        self.direction = 1

    def chamber(self, position):
        return NotImplemented

    def onBulletFired(self):
        pass

    def fire(self, position, source=None):
        projectile = None

        if self.reloading is None:
            self.reloading = Reloading(self.reloadingDuration)
            projectile = self.chamber(position, source)
            self.onBulletFired()

        return projectile

    def update(self):
        if not self.reloading is None:
            self.reloading.update()

            # Remove the reloading affect if the reloading is complete.
            if not self.reloading.isActive():
                self.reloading = None
