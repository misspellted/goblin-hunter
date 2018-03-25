import pygame

from entities import CollidableEntity
from imaging import ImageList

class Player(CollidableEntity):
    def __init__(self, x, y, length, height):
        CollidableEntity.__init__(self, x, y, length, height)
        self.adjustHitBox(17, 11, -(64 - 29), -(64 - 52))

        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkLeft = ImageList("L1.png", "L2.png", "L3.png", "L4.png", "L5.png", "L6.png", "L7.png", "L8.png", "L9.png")
        self.walkRight = ImageList("R1.png", "R2.png", "R3.png", "R4.png", "R5.png", "R6.png", "R7.png", "R8.png", "R9.png")
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.score = 0

    def jump(self):
        startedNewJump = False

        if not self.isJump:
            self.isJump = True
            startedNewJump = True

        return startedNewJump

    def update(self):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            self.walkCount += 1

        if self.isJump:
            if -10 <= self.jumpCount:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount ** 2) * 0.5 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10

    def draw(self, win):
        image = None

        if self.standing:
            image = (self.walkRight if self.right else self.walkLeft)[0]
        else:
            imageIndex = self.walkCount // 3
            image = self.walkLeft[imageIndex] if self.left else self.walkRight[imageIndex] if self.right else None

        if not image is None:
            win.blit(image, self.position)

#        self.showHitBox(win)

    def hit(self):
        self.standing = True
        self.isJump = False
        self.jumpCount = 10
        self.x = 100
        self.y = 410
        self.walkCount = 0

class Enemy(CollidableEntity):
    def __init__(self, x, y, length, height, end):
        CollidableEntity.__init__(self, x, y, length, height)
        self.adjustHitBox(17, 2, -(64 - 31), -(64 - 57))

        self.end = end
        self.path = [self.x, self.end]
        self.walkLeft = ImageList("L1E.png", "L2E.png", "L3E.png", "L4E.png", "L5E.png", "L6E.png", "L7E.png", "L8E.png", "L9E.png", "L10E.png", "L11E.png")
        self.walkRight = ImageList("R1E.png", "R2E.png", "R3E.png", "R4E.png", "R5E.png", "R6E.png", "R7E.png", "R8E.png", "R9E.png", "R10E.png", "R11E.png")
        self.walkCount = 0
        self.vel = 3
        self.health = 10
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:
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

#            self.showHitBox(win)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')
