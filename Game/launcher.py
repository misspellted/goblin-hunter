import pygame

from characters import Player, Enemy
from entities import CollidableEntity
from positioning import Positioned
from window import Window

pygame.init()

char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('bullet.mp3')
hitSound = pygame.mixer.Sound('hit.mp3')

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

class Projectile(CollidableEntity):
    def __init__(self, x, y, radius, color, facing):
        diameter = radius * 2
        CollidableEntity.__init__(self, x, y, diameter, diameter)
        self.adjustHitBox(-radius, -radius, 0, 0)

        self.radius = radius
        self.diameter = radius * 2
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def move(self):
        bullet.x += bullet.vel

    def draw(self,win):
        pygame.draw.circle(win, self.color, (int(self.x),int(self.y)), int(self.radius))

#        self.showHitBox(win)

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

    man.update()

    if goblin.visible == True:
        if goblin.collidesWith(man):
            man.hit()
            man.score -= 5
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
        if bullet.collidesWith(goblin):
            bullets.pop(bullets.index(bullet))
            goblin.hit()
            hitSound.play()
            man.score += 1
        elif 0 < bullet.x < 500:
            bullet.move()
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

        if keys[pygame.K_UP]:
            if man.jump():
                man.right = False
                man.left = False
                man.walkCount = 0

    window.drawItem(Text(350, 10, "Score: " + str(man.score), scoreFont, (0, 0, 0)))

    if not hitText is None:
        window.drawItem(hitText)

    window.drawItem(man)
    window.drawItem(goblin)

    for bullet in bullets:
        window.drawItem(bullet)

    window.refresh()

pygame.quit()
