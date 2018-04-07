class Affect(object):
    def __init__(self, coolDown):
        self.coolDown = coolDown

    def isActive(self):
        return 0 < self.coolDown

    def update(self):
        return NotImplemented
