import pygame

from weapons import Gun, Projectile

class Ammo(Projectile):
    def __init__(self, position, direction):
        x, y = position
        Projectile.__init__(self, x, y, 6, (0, 0, 0), direction)

class Pistol(Gun):
    def __init__(self, reloadingDuration):
        Gun.__init__(self, reloadingDuration)

        self.firingSound = pygame.mixer.Sound("audio/sounds/bullet.wav")

    def chamber(self, position, source):
        return Ammo(position, self.direction)

    def onBulletFired(self):
        self.firingSound.play()
