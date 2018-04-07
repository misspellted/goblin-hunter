import pygame

from weapons import Gun, Projectile

class Pistol(Gun):
    def __init__(self, reloadingDuration, direction=1):
        Gun.__init__(self, reloadingDuration)
        self.firingSound = pygame.mixer.Sound("audio/sounds/bullet.wav")
        self.direction = direction

    def pointLeft(self):
        self.direction = -1

    def pointRight(self):
        self.direction = 1

    def chamber(self, position):
        x, y = position

        return Projectile(x, y, 6, (0, 0, 0), self.direction)

    def onBulletFired(self):
        self.firingSound.play()
