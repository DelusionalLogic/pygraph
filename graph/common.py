from collections import (
    namedtuple,
)
from enum import (
    Enum,
    auto,
)

from vec import (
    Mat4,
    Vec2,
)


class HDir(Enum):
    LEFT = auto()
    MIDDLE = auto()
    RIGHT = auto()

    def inv(self):
        if self == HDir.LEFT:
            return HDir.RIGHT
        elif self == HDir.MIDDLE:
            return HDir.MIDDLE
        elif self == HDir.RIGHT:
            return HDir.LEFT

    def direction(self):
        if self == HDir.LEFT:
            return -1
        elif self == HDir.MIDDLE:
            return 0
        elif self == HDir.RIGHT:
            return 1

class VDir(Enum):
    BELOW = auto()
    MIDDLE = auto()
    ABOVE = auto()

    def inv(self):
        if self == VDir.BELOW:
            return VDir.ABOVE
        elif self == VDir.MIDDLE:
            return VDir.MIDDLE
        elif self == VDir.ABOVE:
            return VDir.BELOW

    def direction(self):
        if self == VDir.BELOW:
            return 1
        elif self == VDir.MIDDLE:
            return 0
        elif self == VDir.ABOVE:
            return -1

Point = namedtuple("Point", ("position", "halign", "valign"))

def vec_apply(point, f, *args, **kvargs):
    return Point(f(*args, **kvargs), point.halign, point.valign)

def p(x, y, halign=None, valign=None, t=None):
    if t is None:
        t = Mat4.identity()

    t = t * Mat4.translate(x, y)
    return Point(t, halign, valign)

def v2p(vec, halign=None, valign=None):
    return Point(vec, halign, valign)

def adjust(point, adjustment):
    return Point(point.position * Mat4.translate(adjustment[0], adjustment[1]), point.halign, point.valign)

def tpoint(point, transform):
    # We still need to apply the inverse of the new transform
    return vec_apply(point, point.position.affine)

def realign(point, halign=None, valign=None):
    halign = point.halign if halign is None else halign
    valign = point.valign if valign is None else valign
    return Point(point.position, halign, valign)

def _unlist(maybe_list):
    if type(maybe_list) is list:
        return maybe_list, maybe_list[-1]

    return [maybe_list], maybe_list

def path(current, next_):
    current,_ = _unlist(current)

    current.append(next_)
    return current

def path_vh(current, next_):
    current, head = _unlist(current)

    current.append(p(head.position.as_vec().x, next_.position.as_vec().y))
    current.append(next_)
    return current

def path_hv(current, next_):
    current, head = _unlist(current)

    current.append(p(next_.position.as_vec().x, head.position.as_vec().y))
    current.append(next_)
    return current

def path_vhv(current, next_):
    current, head = _unlist(current)

    mid = (next_.position.as_vec().y + head.position.as_vec().y)/2
    current.append(p(head.position.as_vec().x, mid))
    current.append(p(next_.position.as_vec().x, mid))
    current.append(next_)
    return current

def path_hvh(current, next_):
    current, head = _unlist(current)

    mid = (next_.position.as_vec().x + head.position.as_vec().x)/2
    current.append(p(mid, head.position.as_vec().y))
    current.append(p(mid, next_.position.as_vec().y))
    current.append(next_)
    return current
