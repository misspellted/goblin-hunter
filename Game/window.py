import pygame

class Window(object):
    def __init__(self, length, height):
        if not pygame.display.get_init():
            pygame.display.init()

        self.window = pygame.display.set_mode((length, height))
        self.backgroundColor = None
        self.backgroundImage = None
        self.itemsToDraw = list()

    def setCaption(self, caption):
        pygame.display.set_caption("First Game")

    def setBackgroundColor(self, color):
        self.backgroundColor = color

    def setBackgroundImage(self, imagePath):
        self.backgroundImage = pygame.image.load(imagePath)

    def drawItem(self, item):
        """Adds an item to be drawn. This item must have a draw(pygame.Surface) method defined!"""
        self.itemsToDraw.append(item)

    def refresh(self):
        if not self.backgroundImage is None:
            self.window.blit(self.backgroundImage, (0, 0))
        elif not self.backgroundColor is None:
            self.window.fill(self.backgroundColor)

        for itemToDraw in self.itemsToDraw:
            itemToDraw.draw(self.window)

        pygame.display.update()

        del self.itemsToDraw[:]
