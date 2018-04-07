import fnmatch
import pygame
import os

class ImageList(object):
    def __init__(self, *imagePaths):
        self.images = list()
        if not imagePaths is None:
            for imagePath in imagePaths:
                self.images.append(pygame.image.load(imagePath))

    def __len__(self):
        return len(self.images)

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

class Animation(object):
    def __init__(self, imageList, updatesBetweenFrames):
        self.imageList = imageList
        self.updatesBetweenFrames = updatesBetweenFrames
        self.reset()

    def reset(self):
        self.updates = 0
        self.imageIndex = 0

    def getImage(self):
        return self.imageList[self.imageIndex]

    def update(self):
        self.updates += 1

        if self.updatesBetweenFrames <= self.updates:
            self.updates = 0
            self.imageIndex += 1

        # Wrap around.
        if self.imageIndex == len(self.imageList):
            self.imageIndex = 0

    @staticmethod
    def fromDirectory(path, updatesBetweenFrames, pattern=None):
        imageList = ImageList.fromDirectory(path, pattern)

        return None if imageList is None else Animation(imageList, updatesBetweenFrames)

class Animated(object):
    def __init__(self):
        self.animation = None

    def setAnimation(self, animation):
        if isinstance(animation, Animation):
            self.animation = animation
        else:
            self.animation = None

    def updateAnimation(self):
        if not self.animation is None:
            self.animation.update()

    def getAnimationFrame(self):
        return None if self.animation is None else self.animation.getImage()
