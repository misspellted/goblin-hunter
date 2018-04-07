from affects import Affect

class Invincibility(Affect):
    def __init__(self, coolDown):
        Affect.__init__(self, coolDown)

    def update(self):
        if self.isActive():
            self.coolDown -= 1
