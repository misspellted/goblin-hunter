import fnmatch
import pygame
import os

class ImageList(object):
    def __init__(self, *imagePaths):
        self.images = list()
        if not imagePaths is None:
            for imagePath in imagePaths:
                self.images.append(pygame.image.load(imagePath))

    def __getitem__(self, index):
        return self.images[index]

    @staticmethod
    def fromDirectory(path, pattern=None):
        """Loads the images from a directory as an ImageList."""
        imagePaths = list()

        if pattern is None:
            for root, directories, files in os.walk(path):
                for fileName in files:
                    imagePaths.append(os.path.join(root, fileName))
        else:
            for root, directories, files in os.walk(path):
                for fileName in files:
                    if fnmatch.fnmatch(fileName, pattern):
                        imagePaths.append(os.path.join(root, fileName))

        imageList = None

        if 0 < len(imagePaths):
            imageList = ImageList(*imagePaths)

        return imageList
