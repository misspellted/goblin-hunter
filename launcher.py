import pygame

from goblin import Enemy
from player import Player
from positioning import Positioned
from window import Window

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

clock = pygame.time.Clock()

hitSound = pygame.mixer.Sound("audio/sounds/hit.wav")

music = pygame.mixer.music.load('audio/tracks/music.mp3')
pygame.mixer.music.play(-1)

class Text(Positioned):
    def __init__(self, x, y, text, font, color):
        Positioned.__init__(self, x, y)
        self.surface = font.render(text, 1, color)

    def draw(self, surface):
        surface.blit(self.surface, self.position)

#mainloop
window = Window(500, 480)
window.setCaption("First Game")
window.setBackgroundImage("images/environment/bg.jpg")

scoreFont = pygame.font.SysFont("comicsans", 30, True)
hitFont = pygame.font.SysFont("comicsans", 100)

player = Player(0, 410, 64,64)
player.setMinimumLeftPosition(0)
player.setMaximumRightPosition(500 - player.length)

enemies = list()
enemies.append(Enemy(100, 410, 64, 64, 450))
enemies.append(Enemy(200, 410, 64, 64, 450))

bullets = []

hitTextCoolDown = 0
run = True

while run:
    clock.tick(27)

    hitText = None

    player.update()

    for enemy in enemies:
        if enemy.collidesWith(player):
            if player.onAttackedBy(enemy):
                hitTextCoolDown = 200
                hitText = Text(200, 200, "-5", hitFont, (255, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            continue

    for bullet in bullets:
        bulletStillFlying = True

        # Did the bullet impact any enemies?
        for enemy in enemies:
            if bullet.collidesWith(enemy):
                bulletStillFlying = False
                hitSound.play()
                player.score += 1

                # Did the enemy entity die on impact?
                if enemy.hit():
                    enemies.pop(enemies.index(enemy))

            # One bullet, one enemy. For now...
            if not bulletStillFlying:
                break

        # Is the bullet still in the field of battle?
        if bulletStillFlying:
            bulletStillFlying = 0 <= bullet.x <= 500

        if bulletStillFlying:
            bullet.move()
        else:
            bullets.pop(bullets.index(bullet))

    if 0 < hitTextCoolDown:
        hitTextCoolDown -= 1

        if hitTextCoolDown <= 0:
            hitText = None

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        # Only allow a maximum of 5 bullets on screen at any given time.
        if len(bullets) < 5:
            projectile = player.shoot()

            # Of course, the weapon has a cool-down, so it may not fire one immediately.
            if not projectile is None:
                bullets.append(projectile)

    if keys[pygame.K_LEFT]:
        player.turnLeft()
        player.move()
    elif keys[pygame.K_RIGHT]:
        player.turnRight()
        player.move()
    else:
        player.stop()

    if keys[pygame.K_UP]:
        player.jump()

    window.drawItem(Text(350, 10, "Score: " + str(player.score), scoreFont, (0, 0, 0)))

    if not hitText is None:
        window.drawItem(hitText)

    window.drawItem(player)

    for enemy in enemies:
        window.drawItem(enemy)

    for bullet in bullets:
        window.drawItem(bullet)

    window.refresh()

    # Game ends when there are no more enemies (for now).
    if len(enemies) == 0:
        run = False

pygame.quit()
