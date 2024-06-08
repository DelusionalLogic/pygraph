import math

import numpy as np


def _coerce(other, size):
    if isinstance(other, Vec):
        return other

    if type(other) is tuple:
        return Vec(*other)

    if type(other) is int:
        return Vec(*(other, ) * size)

    if type(other) is float:
        return Vec(*(other, ) * size)

    return None

class Vec():
    __slots__ = ["inner"]

    def __init__(self, *args):
        self.inner = args

    def __add__(self, other):
        other = _coerce(other, len(self.inner))
        if other is None:
            return NotImplemented

        if len(self.inner) != len(other.inner):
            raise NotImplemented

        return self.__class__(*map(lambda i: i[0] + i[1], zip(self.inner, other.inner)))

    def __sub__(self, other):
        other = _coerce(other, len(self.inner))
        if other is None:
            return NotImplemented

        if len(self.inner) != len(other.inner):
            raise NotImplemented

        return self.__class__(*map(lambda i: i[0] - i[1], zip(self.inner, other.inner)))

    def __truediv__(self, other):
        other = _coerce(other, len(self.inner))
        if other is None:
            return NotImplemented

        if len(self.inner) != len(other.inner):
            raise NotImplemented

        return self.__class__(*map(lambda i: i[0] / i[1], zip(self.inner, other.inner)))

    def __mul__(self, other):
        if type(other) is Mat3:
            return self.__class__(*np.dot(self.inner + (0, ), other.inner)[:-1])

        other = _coerce(other, len(self.inner))
        if other is None:
            return NotImplemented

        if len(self.inner) != len(other.inner):
            raise NotImplemented

        return self.__class__(*map(lambda i: i[0] * i[1], zip(self.inner, other.inner)))

    def __rmul__(self, other):
        return self.__mul__(other)

    def length(self):
        return math.sqrt(sum(map(lambda i: i ** 2, self.inner)))

    def unit(self):
        return self / _coerce(self.length(), len(self.inner))

    def angle(self):
        if len(self.inner) != 2:
            raise NotImplemented

        if self.inner[0] == 0:
            return math.tau / 4 if self.inner[1] > 0 else math.tau / 4 * 3

        return math.tan(self.inner[1]/self.inner[0])

    def dot(self, other):
        if len(self.inner) != len(other.inner):
            raise NotImplemented

        return sum(map(lambda i: i[0] * i[1], zip(self.inner, other.inner)))

    @property
    def x(self):
        return self.inner[0]

    @property
    def y(self):
        return self.inner[1]

    @property
    def z(self):
        return self.inner[2]

class Vec2(Vec):
    pass

class Mat3():
    __slots__ = ["inner"]

    @staticmethod
    def identity():
        return Mat3(np.array([
            [ 1,  0,  0],
            [ 0,  1,  0],
            [ 0,  0,  1],
        ]))

    @staticmethod
    def translate(dx=0, dy=0):
        return Mat3(np.array([
            [ 1,  0, 0],
            [ 0,  1, 0],
            [dx, dy, 1],
        ]))

    @staticmethod
    def scale(sx=1.0, sy=1.0):
        return Mat3(np.array([
            [sx,  0, 0],
            [ 0, sy, 0],
            [ 0,  0, 1],
        ]))

    @staticmethod
    def skew(ax=0.0, ay=0.0):
        return Mat3(np.array([
            [ 1,ax, 0],
            [ay, 1, 0],
            [ 0, 0, 1],
        ]))

    @staticmethod
    def roty(theta=0.0):
        return Mat3(np.array([
            [ math.cos(theta),0, math.sin(theta)],
            [0, 1, 0],
            [-math.sin(theta), 0, math.cos(theta)],
        ]))

    @staticmethod
    def rotz(theta=0.0):
        return Mat3(np.array([
            [ math.cos(theta),math.sin(theta), 0],
            [-math.sin(theta), math.cos(theta), 0],
            [0, 0, 1],
        ]))

    def __init__(self, mat):
        self.inner = mat

    def __mul__(self, other):
        return Mat3(np.dot(self.inner, other.inner))
