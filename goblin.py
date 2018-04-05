import pygame

from entities import CollidableEntity
from imaging import ImageList

class Enemy(CollidableEntity):
    def __init__(self, x, y, length, height):
        CollidableEntity.__init__(self, x, y, length, height)
        self.adjustHitBox(17, 2, -(length - 31), -(height - 57))

        self.hitSound = pygame.mixer.Sound("audio/sounds/hit.wav")

        self.walkLeft = ImageList.fromDirectory("images/goblin/walkingLeft")
        self.walkRight = ImageList.fromDirectory("images/goblin/walkingRight")
        self.walkCount = 0
        self.vel = 3
        self.health = 10
        self.visible = True

    def draw(self,win):
        self.move()

        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
            self.walkCount += 1

        pygame.draw.rect(win, (255,0,0), (self.hitBox.x, self.hitBox.y - 20, 50, 10))
        pygame.draw.rect(win, (0,128,0), (self.hitBox.x, self.hitBox.y - 20, 50 - (5 * (10 - self.health)), 10))

#        self.showHitBox(win)

    def move(self):
        self.x += self.vel

        if self.x < self.minimumXPosition:
            self.x = self.minimumXPosition
            self.vel = self.vel * -1
            self.walkCount = 0
        elif self.maximumXPosition < self.x:
            self.x = self.maximumXPosition
            self.vel = self.vel * -1
            self.walkCount = 0

    def hit(self):
        self.hitSound.play()

        self.health -= 1

        # Did the enemy die?
        return self.health <= 0
