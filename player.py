import pygame

from entities import CollidableEntity
from imaging import ImageList
from weapons import Gun

class Player(CollidableEntity):
    def __init__(self, x, y, length, height):
        CollidableEntity.__init__(self, x, y, length, height)
        self.adjustHitBox(17, 11, -(64 - 29), -(64 - 52))

        self.startingPosition = (x, y)

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

        self.startingInvincibilityCoolDown = 200
        self.invincibilityCoolDown = 0

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

        if 0 < self.invincibilityCoolDown:
            self.invincibilityCoolDown -= 1

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

    def onAttackedBy(self, attacker=None):
        """Handles an attack on the entity from another."""

        # If the player is not invincible, handle the attack.
        attackSuccessful = self.invincibilityCoolDown <= 0

        if attackSuccessful:
            # Reset jumping.
            self.isJump = False
            self.jumpCount = 10

            # "Respawn the player" (move them to their starting position).
            self.x, self.y = self.startingPosition

            # Stop moving
            self.stop()

            # Decrease the score:
            self.score -= 5

            # Activate temporary invincibility.
            self.invincibilityCoolDown = self.startingInvincibilityCoolDown

        return attackSuccessful

    def hit(self):
        self.onAttack(None)
