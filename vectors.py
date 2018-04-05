import unittest

class Vector(object):
    def __init__(self, *values):
        self._values = list(values)

    def __len__(self):
        return len(self._values)

    def __getitem__(self, index):
        return self._values[index]

    def __setitem__(self, index, value):
        self._values[index] = value

    def __add__(self, other):
        return Vector(*[(self[index] + other[index]) for index in range(len(self))])

    def __sub__(self, other):
        return Vector(*[(self[index] - other[index]) for index in range(len(self))])

    def __eq__(self, other):
        equal = False

        if isinstance(other, Vector):
            equal = len(self) == len(other)

            index = 0
            while equal and index < len(self):
                equal = self[index] == other[index]
                index += 1

        return equal

    def __str__(self):
        # Get that nice paranthetical notation.
        return "(" + str(self._values)[1:-1] + ")"

class TestVector(unittest.TestCase):
    def testLengthWithTwoValues(self):
        tested = Vector(1, 2)

        self.assertEqual(len(tested), 2)

    def testGetItemWithTwoValues(self):
        tested = Vector(1, 2)

        self.assertEqual(tested[0], 1)
        self.assertEqual(tested[1], 2)

    def testSetItemWithTwoValues(self):
        tested = Vector(1, 2)

        self.assertEqual(tested[0], 1)
        self.assertEqual(tested[1], 2)

        tested[0] = 2
        tested[1] = 4

        self.assertEqual(tested[0], 2)
        self.assertEqual(tested[1], 4)

    def testAddWithTwoTwoValueVectors(self):
        a = Vector(1, 2)
        b = Vector(3, 4)

        tested = a + b

        self.assertEqual(len(tested), 2)
        self.assertEqual(tested[0], 4)
        self.assertEqual(tested[1], 6)

    def testSubWithTwoTwoValueVectors(self):
        a = Vector(1, 2)
        b = Vector(3, 4)

        tested = a - b

        self.assertEqual(len(tested), 2)
        self.assertEqual(tested[0], -2)
        self.assertEqual(tested[1], -2)

    def testEqWithTwoSameTwoValueVectors(self):
        a = Vector(1, 2)
        b = Vector(1, 2)

        self.assertTrue(a == b)

    def testStrWithTwoValueVector(self):
        tested = Vector(1, 2)

        self.assertEqual(str(tested), "(1, 2)")

class WithX(Vector):
    def __init__(self, *values):
        if len(values) < 1:
            raise ValueError("'values' does not contain enough elements.")
        Vector.__init__(self, *values)

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

class TestWithX(unittest.TestCase):
    def testX(self):
        tested = WithX(1)

        self.assertEqual(tested.x, 1)

        tested.x = 2

        self.assertEqual(tested.x, 2)

class WithY(Vector):
    def __init__(self, *values):
        if len(values) < 2:
            raise ValueError("'values' does not contain enough elements.")
        Vector.__init__(self, *values)

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

class TestWithY(unittest.TestCase):
    def testY(self):
        tested = WithY(1, 2)

        self.assertEqual(tested.y, 2)

        tested.y = 4

        self.assertEqual(tested.y, 4)

class WithZ(Vector):
    def __init__(self, *values):
        if len(values) < 3:
            raise ValueError("'values' does not contain enough elements.")
        Vector.__init__(self, *values)

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, value):
        self[2] = value

class TestWithZ(unittest.TestCase):
    def testZ(self):
        tested = WithZ(1, 2, 3)

        self.assertEqual(tested.z, 3)

        tested.z = 6

        self.assertEqual(tested.z, 6)

class VectorX(WithX):
    def __init__(self, x):
        Vector.__init__(self, x)

# This kind of makes sense... but at the same time, only slightly.
class VectorXY(WithX, WithY):
    def __init__(self, x, y):
        Vector.__init__(self, x, y)

class TestVectorXY(unittest.TestCase):
    def testInstance(self):
        tested = VectorXY(1, 2)

        self.assertEqual(len(tested), 2)
        self.assertEqual(tested.x, 1)
        self.assertEqual(tested.y, 2)

# This kind of makes sense... but at the same time, only slightly.
class VectorXYZ(WithX, WithY, WithZ):
    def __init__(self, x, y, z):
        Vector.__init__(self, x, y, z)

class TestVectorXYZ(unittest.TestCase):
    def testInstance(self):
        tested = VectorXYZ(1, 2, 3)

        self.assertEqual(len(tested), 3)
        self.assertEqual(tested.x, 1)
        self.assertEqual(tested.y, 2)
        self.assertEqual(tested.z, 3)

if __name__ == "__main__":
    unittest.main()
