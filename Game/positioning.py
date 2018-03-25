class PositionChangedListener(object):
    def onXChanged(self, last, current):
        return NotImplemented

    def onYChanged(self, last, current):
        return NotImplemented

class Positioned(object):
    def __init__(self, x, y):
        self._x = int(x)
        self._y = int(y)
        self.changedListeners = list()

    def addPositionChangedListener(self, listener):
        if not listener is None:
            self.changedListeners.append(listener)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        lastX = self._x
        self._x = int(x)
        for listener in self.changedListeners:
            listener.onXChanged(lastX, self._x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        lastY = self._y
        self._y = int(y)
        for listener in self.changedListeners:
            listener.onYChanged(lastY, self._y)

    @property
    def position(self):
        return (self._x, self._y)
