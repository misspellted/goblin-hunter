import pygame

from entities import CollidableEntity
from imaging import ImageList
from weapons import Gun

class Player(CollidableEntity):
    def __init__(self, x, y, length, height):
        CollidableEntity.__init__(self, x, y, length, height)
        self.adjustHitBox(17, 11, -(64 - 29), -(64 - 52))

        self.standing = True
        self.left = False
        self.right = False

        self.minimumLeftPosition = None
        self.maximumRightPosition = None

        self.walkLeft = ImageList.fromDirectory("images/player/walkingLeft")
        self.walkRight = ImageList.fromDirectory("images/player/walkingRight")
        self.walkCount = 0

        self.isJump = False
        self.jumpCount = 10

        self.weapon = Gun(3)

        self.vel = 5
        self.score = 0

    def setMinimumLeftPosition(self, minimumLeftPosition):
        self.minimumLeftPosition = minimumLeftPosition

    def setMaximumRightPosition(self, maximumRightPosition):
        self.maximumRightPosition = maximumRightPosition

    def turnLeft(self):
        self.left = True
        self.right = False
        self.standing = False

    def turnRight(self):
        self.left = False
        self.right = True
        self.standing = False

    def stop(self):
        self.standing = True
        self.walkCount = 0

    def move(self):
        if self.left:
            self.x -= self.vel
            if not self.minimumLeftPosition is None:
                if self.x < self.minimumLeftPosition:
                    self.x = self.minimumLeftPosition
        elif self.right:
            self.x += self.vel
            if not self.maximumRightPosition is None:
                print("Current X: " + str(self.x) + ", Maximum X: " + str(self.maximumRightPosition))
                if self.maximumRightPosition < self.x:
                    self.x = self.maximumRightPosition

    def jump(self):
        startedNewJump = False

        if not self.isJump:
            self.isJump = True
            startedNewJump = True
            self.left = False
            self.right = False
            self.walkCount = 0

        return startedNewJump

    def shoot(self):
        bulletFired = None

        if not self.weapon is None:
            # Shoot from the center of the player.
            position = self.x + self.halfLength, self.y + self.halfHeight

            bulletFired = self.weapon.fire(position, -1 if self.left else 1)

        return bulletFired

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

        if not self.weapon is None:
            self.weapon.update()

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
        self.health -= 1

        # Did the enemy die?
        return self.health <= 0
