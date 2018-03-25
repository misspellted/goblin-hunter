import pygame

from dimensioning import Dimensioned
from images import ImageList
from positioning import Positioned, PositionChangedListener
from window import Window

pygame.init()

char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('bullet.mp3')
hitSound = pygame.mixer.Sound('hit.mp3')

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

score = 0

class Player(Positioned, Dimensioned):
    def __init__(self, x, y, length, height):
        Positioned.__init__(self, x, y)
        Dimensioned.__init__(self, length, height)

        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkLeft = ImageList("L1.png", "L2.png", "L3.png", "L4.png", "L5.png", "L6.png", "L7.png", "L8.png", "L9.png")
        self.walkRight = ImageList("R1.png", "R2.png", "R3.png", "R4.png", "R5.png", "R6.png", "R7.png", "R8.png", "R9.png")
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        image = None

        if self.standing:
            image = (self.walkRight if self.right else self.walkLeft)[0]
        else:
            images = None

            if self.left:
                images = self.walkLeft
            elif self.right:
                images = self.walkRight

            if not images is None:
                image = images[self.walkCount // 3]
                self.walkCount += 1

        if not image is None:
            win.blit(image, (self.x, self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def hit(self):
        self.standing = True
        self.isJump = False
        self.jumpCount = 10
        self.x = 100
        self.y = 410
        self.walkCount = 0

class Projectile(Positioned):
    def __init__(self, x, y, radius, color, facing):
        Positioned.__init__(self, x, y)

        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (int(self.x),int(self.y)), int(self.radius))

class Enemy(Positioned, Dimensioned):
    def __init__(self, x, y, length, height, end):
        Positioned.__init__(self, x, y)
        Dimensioned.__init__(self, length, height)

        self.end = end
        self.path = [self.x, self.end]
        self.walkLeft = ImageList("L1E.png", "L2E.png", "L3E.png", "L4E.png", "L5E.png", "L6E.png", "L7E.png", "L8E.png", "L9E.png", "L10E.png", "L11E.png")
        self.walkRight = ImageList("R1E.png", "R2E.png", "R3E.png", "R4E.png", "R5E.png", "R6E.png", "R7E.png", "R8E.png", "R9E.png", "R10E.png", "R11E.png")
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
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

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

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

class Text(Positioned):
    def __init__(self, x, y, text, font, color):
        Positioned.__init__(self, x, y)
        self.surface = font.render(text, 1, color)

    def draw(self, surface):
        surface.blit(self.surface, self.position)

#mainloop
window = Window(500, 480)
window.setCaption("First Game")
window.setBackgroundImage("bg.jpg")

scoreFont = pygame.font.SysFont("comicsans", 30, True)
hitFont = pygame.font.SysFont("comicsans", 100)

man = Player(200, 410, 64,64)
goblin = Enemy(100, 410, 64, 64, 450)
shootLoop = 0
bullets = []
hitCoolDown = 0
run = True

while run:
    clock.tick(27)

    hitText = None

    if goblin.visible == True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5
                hitCoolDown = 200
                hitText = Text(200, 200, "-5", hitFont, (255, 0, 0))

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                hitSound.play()
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # Punish the player if they got hit by not processing any input.
    if 0 < hitCoolDown:
        pygame.time.delay(10)
        hitCoolDown -= 1

        if hitCoolDown <= 0:
            # Don't forget to hide the message.
            hitText = None
    else:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and shootLoop == 0:
            facing = -1 if man.left else 1

            if len(bullets) < 5:
                bulletSound.play()
                bullets.append(Projectile(round(man.x + man.length //2), round(man.y + man.height//2), 6, (0,0,0), facing))

            shootLoop = 1

        if keys[pygame.K_LEFT] and man.x > man.vel:
            man.x -= man.vel
            man.left = True
            man.right = False
            man.standing = False
        elif keys[pygame.K_RIGHT] and man.x < 500 - man.length - man.vel:
            man.x += man.vel
            man.right = True
            man.left = False
            man.standing = False
        else:
            man.standing = True
            man.walkCount = 0

        if not(man.isJump):
            if keys[pygame.K_UP]:
                man.isJump = True
                man.right = False
                man.left = False
                man.walkCount = 0
        else:
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
                man.y -= (man.jumpCount ** 2) * 0.5 * neg
                man.jumpCount -= 1
            else:
                man.isJump = False
                man.jumpCount = 10

    window.drawItem(Text(350, 10, "Score: " + str(score), scoreFont, (0, 0, 0)))

    if not hitText is None:
        window.drawItem(hitText)

    window.drawItem(man)
    window.drawItem(goblin)

    for bullet in bullets:
        window.drawItem(bullet)

    window.refresh()

pygame.quit()
