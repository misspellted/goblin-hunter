import pygame

from entities import CollidableEntity
from imaging import Animated, Animation, ImageList
from vectors import VectorXY

class Enemy(CollidableEntity, Animated):
    def __init__(self, x, y, length, height):
        CollidableEntity.__init__(self, x, y, length, height)
        self.adjustHitBox(17, 2, -(length - 31), -(height - 57))

        self.hitSound = pygame.mixer.Sound("audio/sounds/hit.wav")

        Animated.__init__(self)

        self.walkingVelocity = 3
        self.walkingLeftAnimation = Animation.fromDirectory("images/goblin/walkingLeft", 3)
        self.walkingRightAnimation = Animation.fromDirectory("images/goblin/walkingRight", 3)

        self.velocity = VectorXY(0, 0)

        self.health = 10

        self.turnRight()

    def turnLeft(self):
        self.velocity.x = -self.walkingVelocity
        self.setAnimation(self.walkingLeftAnimation)

    def turnRight(self):
        self.velocity.x = self.walkingVelocity
        self.setAnimation(self.walkingRightAnimation)

    def update(self):
        self.move()

        if not self.minimumXPosition is None and self.x <= self.minimumXPosition:
            self.turnRight()

        if not self.maximumXPosition is None and self.maximumXPosition <= self.x:
            self.turnLeft()

        self.updateAnimation()

    def move(self):
        self.x += self.velocity.x
        self.y += self.velocity.y

        if not self.minimumXPosition is None and self.x <= self.minimumXPosition:
            self.x = self.minimumXPosition

        if not self.maximumXPosition is None and self.maximumXPosition <= self.x:
            self.x = self.maximumXPosition

        if not self.minimumYPosition is None and self.y <= self.minimumYPosition:
            self.y = self.minimumYPosition

        if not self.maximumYPosition is None and self.maximumYPosition <= self.y:
            self.y = self.maximumYPosition

    def hit(self):
        self.hitSound.play()

        self.health -= 1

        # Did the enemy die?
        return self.health <= 0

    def draw(self,win):
        image = self.getAnimationFrame()

        if not image is None:
            win.blit(image, self.position)

            pygame.draw.rect(win, (255,0,0), (self.hitBox.x, self.hitBox.y - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitBox.x, self.hitBox.y - 20, 50 - (5 * (10 - self.health)), 10))

#            self.showHitBox(win)
