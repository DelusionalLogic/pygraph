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

    def __init__(self, x, y, z = 0.0):
        self.inner = np.array((x, y, z), dtype=np.double)

    def __add__(self, other):
        other = _coerce(other, 3)
        if other is None:
            return NotImplemented

        return self.__class__(*map(lambda i: i[0] + i[1], zip(self.inner, other.inner)))

    def __sub__(self, other):
        other = _coerce(other, 3)
        if other is None:
            return NotImplemented

        return self.__class__(*map(lambda i: i[0] - i[1], zip(self.inner, other.inner)))

    def __truediv__(self, other):
        other = _coerce(other, 3)
        if other is None:
            return NotImplemented

        return self.__class__(*map(lambda i: i[0] / i[1], zip(self.inner, other.inner)))

    def __mul__(self, other):
        other = _coerce(other, 3)
        if other is None:
            return NotImplemented

        return self.__class__(*map(lambda i: i[0] * i[1], zip(self.inner, other.inner)))

    def __rmul__(self, other):
        return self.__mul__(other)

    def length(self):
        return math.sqrt(sum(map(lambda i: i ** 2, self.inner)))

    def unit(self):
        len = self.length()
        if len == 0:
            return self
        return self / _coerce(len, 3)

    def angle(self):
        return math.atan2(self.inner[1], self.inner[0])

    def dot(self, other):
        return sum(map(lambda i: i[0] * i[1], zip(self.inner, other.inner)))

    def is_zero(self):
        return not np.any(self.inner)

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

class Mat4():
    __slots__ = ["inner"]

    @staticmethod
    def identity():
        return Mat4(np.array([
            [ 1,  0,  0, 0],
            [ 0,  1,  0, 0],
            [ 0,  0,  1, 0],
            [ 0,  0,  0, 1],
        ], dtype=np.double))

    @staticmethod
    def translate(dx=0., dy=0., dz=0.):
        return Mat4(np.array([
            [ 1,  0, 0, dx],
            [ 0,  1, 0, dy],
            [ 0,  0, 1, dz],
            [ 0,  0, 0,  1],
        ], dtype=np.double))

    @staticmethod
    def scale(sx=1.0, sy=1.0, sz=1.0):
        return Mat4(np.array([
            [sx,  0,  0, 0],
            [ 0, sy,  0, 0],
            [ 0,  0, sz, 0],
            [ 0,  0,  0, 1],
        ], dtype=np.double))

    @staticmethod
    def rotx(theta=0.0):
        return Mat4(np.array([
            [1, 0, 0, 0],
            [0, math.cos(theta), -math.sin(theta), 0],
            [0, math.sin(theta), math.cos(theta), 0],
            [ 0, 0, 0, 1],
        ], dtype=np.double))

    @staticmethod
    def roty(theta=0.0):
        return Mat4(np.array([
            [ math.cos(theta), 0, math.sin(theta), 0],
            [0, 1, 0, 0],
            [-math.sin(theta), 0, math.cos(theta), 0],
            [0, 0, 0, 1],
        ], dtype=np.double))

    @staticmethod
    def rotz(theta=0.0):
        return Mat4(np.array([
            [ math.cos(theta), -math.sin(theta), 0, 0],
            [ math.sin(theta),  math.cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ], dtype=np.double))

    def __init__(self, mat):
        self.inner = mat

    def __mul__(self, other):
        if isinstance(other, Vec):
            return other.__class__(*np.dot(self.inner, np.array((*other.inner, 1)))[:3])

        return Mat4(np.dot(self.inner, other.inner))

    def linear(self):
        new = np.copy(self.inner)
        new[0:3, 3] = 0
        new[3, 3] = 1
        return Mat4(new)

    def affine(self):
        new = np.copy(self.inner)
        new[0:3, 0:3] = np.identity(3)
        new[3, 0:3] = 0
        return Mat4(new)

    def as_vec(self):
        return Vec(*self.inner[0:3, 3])
