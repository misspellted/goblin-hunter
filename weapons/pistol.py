import pygame

from weapons import Gun, Projectile

class Pistol(Gun):
    def __init__(self, reloadingDuration):
        Gun.__init__(self, reloadingDuration)
        self.firingSound = pygame.mixer.Sound("audio/sounds/bullet.wav")

    def chamber(self, position, direction):
        x, y = position

        return Projectile(x, y, 6, (0, 0, 0), direction)

    def onBulletFired(self):
        self.firingSound.play()
