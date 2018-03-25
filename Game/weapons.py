import pygame

from entities import CollidableEntity

class Projectile(CollidableEntity):
    def __init__(self, x, y, radius, color, facing):
        diameter = radius * 2
        CollidableEntity.__init__(self, x, y, diameter, diameter)
        self.adjustHitBox(-radius, -radius, 0, 0)

        self.radius = radius
        self.diameter = radius * 2
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def move(self):
        self.x += self.vel

    def draw(self,win):
        # pygame.draw.circle requires integer positioning (at least, on Ubuntu 17.10/Python 2.7/PyGame 1.9.3)
        position = (int(self.x), int(self.y))
        pygame.draw.circle(win, self.color, position, self.radius)

#        self.showHitBox(win)

class Gun(object):
    def __init__(self, coolDown):
        self.firingSound = pygame.mixer.Sound("bullet.wav")
        self.startingCoolDown = coolDown
        self.coolDown = 0

    def fire(self, position, direction):
        projectile = None

        if self.coolDown == 0:
            self.coolDown = self.startingCoolDown
            x, y = position
            projectile = Projectile(x, y, 6, (0, 0, 0), direction)
            self.firingSound.play()

        return projectile

    def update(self):
        if 0 < self.coolDown:
            self.coolDown -= 1
