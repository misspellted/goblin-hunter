import pygame

class ImageList(object):
    def __init__(self, *imagePaths):
        self.images = list()
        if not imagePaths is None:
            for imagePath in imagePaths:
                self.images.append(pygame.image.load(imagePath))

    def __getitem__(self, index):
        return self.images[index]
