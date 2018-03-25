class Dimensioned(object):
    def __init__(self, length, height):
        self.length = length
        self.height = height

    @property
    def halfLength(self):
        return self.length // 2

    @property
    def halfHeight(self):
        return self.height // 2

    @property
    def dimension(self):
        return (self.length, self.height)
