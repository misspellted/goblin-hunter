import pygame

from affects.invincibility import Invincibility
from entities import CollidableEntity
from imaging import Animated, Animation
from vectors import VectorXY
from weapons.pistol import Pistol

class Player(CollidableEntity, Animated):
    def __init__(self, x, y, length, height):
        self.startingPosition = (x, y)

        CollidableEntity.__init__(self, x, y, length, height)
        self.adjustHitBox(17, 11, -(length - 29), -(height - 52))

        self.standingImage = pygame.image.load("images/player/standing.png")

        Animated.__init__(self)

        # Walking information and visuals.
        self.walkingVelocity = 5
        self.walkingLeftAnimation = Animation.fromDirectory("images/player/walkingLeft", 3)
        self.walkingRightAnimation = Animation.fromDirectory("images/player/walkingRight", 3)

        # TODO: Convert jumping into an affect.
        self.isJump = False
        self.jumpCount = 10

        self.weapon = Pistol(3)
        self.weapon.pointRight() # Weapons initially face right, towards the enem(y|ies).

        self.velocity = VectorXY(0, 0)
        self.score = 0

        self.affects = list()

    def turnLeft(self):
        self.velocity.x = -self.walkingVelocity
        self.setAnimation(self.walkingLeftAnimation)
        self.weapon.pointLeft()

    def turnRight(self):
        self.velocity.x = self.walkingVelocity
        self.setAnimation(self.walkingRightAnimation)
        self.weapon.pointRight()

    def stop(self):
        self.velocity.x = 0
        self.setAnimation(None)

    def move(self):
        # TODO: Figure out how to do 'self.position += self.velocity'.
        self.x += self.velocity.x
        self.y += self.velocity.y

        if not self.minimumXPosition is None and self.x < self.minimumXPosition:
            self.x = self.minimumXPosition

        if not self.maximumXPosition is None and self.maximumXPosition < self.x:
            self.x = self.maximumXPosition

        if not self.minimumYPosition is None and self.y < self.minimumYPosition:
            self.y = self.minimumYPosition

        if not self.maximumYPosition is None and self.maximumYPosition < self.y:
            self.y = self.maximumYPosition

    def jump(self):
        startedNewJump = False

        if not self.isJump:
            self.isJump = True
            startedNewJump = True

        return startedNewJump

    def shoot(self):
        bulletFired = None

        # Only shoot if the weapon is available.
        if not self.weapon is None:
            # Shoot from the center of the player.
            position = self.x + self.halfLength, self.y + self.halfHeight

            bulletFired = self.weapon.fire(position)

        return bulletFired

    def update(self):
        self.updateAnimation()

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

        for affect in self.affects:
            if not affect.isActive():
                self.affects.pop(self.affects.index(affect))
            else:
                affect.update()

    def draw(self, win):
        image = self.getAnimationFrame()

        if image is None:
            image = self.standingImage

        win.blit(image, self.position)

#        self.showHitBox(win)

    def onAttackedBy(self, attacker=None):
        """Handles an attack on the entity from another."""
        attackSuccessful = True

        # If the player is invincible, ignore the attack.
        for affect in self.affects:
            if type(affect) is Invincibility:
                attackSuccessful = False
                break

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

            # Apply temporary invincibility affect.
            self.affects.append(Invincibility(200))

        return attackSuccessful

    def hit(self):
        self.onAttack(None)
