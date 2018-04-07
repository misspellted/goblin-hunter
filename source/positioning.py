from vectors import VectorXY

class Positioned(VectorXY):
    def __init__(self, x, y):
        VectorXY.__init__(self, x, y)

    @property
    def position(self):
        return (self.x, self.y)
