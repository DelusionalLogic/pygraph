#!/usr/bin/env python3
import math
import click
from enum import (Enum, auto)

def line_intersect(pos, w, h, ray, ray_theta):
    # Calculate a unit vector for the ray. The length doesn't actually matter,
    # since we only care about the sign of the intercept for the ray
    ray_w = math.cos(ray_theta)
    ray_h = -math.sin(ray_theta)

    coeff = (h * ray_w - ray_h * w)
    # The lines are parallel
    if coeff == 0:
        return None

    # Make sure the intercept is in front of the ray
    u = -(w * (pos.y - ray.y) + h * ray.x - h * pos.x) / coeff
    if u < 0:
        return None

    t = -(ray_w * (pos.y - ray.y) + ray_h * ray.x - ray_h * pos.x) / coeff

    return t

def line_intersect_point(pos, w, h, t):
    return pos + Vec2(w, h) * t

class Point():
    __slots__ = ["x", "y", "align", "valign"]
    def __init__(self, x, y, align=None, valign=None):
        self.x = x
        self.y = y
        self.align = align
        self.valign = valign

    def __add__(self, other):
        if type(other) is Point:
            (ox, oy) = (other.x, other.y)
            return Point(self.x + ox, self.y + oy, self.align, self.valign)

        if type(other) is tuple:
            (ox, oy) = other
            return Point(self.x + ox, self.y + oy, self.align, self.valign)

        return NotImplemented

    def __sub__(self, other):
        if type(other) is Point:
            (ox, oy) = (other.x, other.y)
            return Point(self.x - ox, self.y - oy, self.align, self.valign)

        if type(other) is tuple:
            (ox, oy) = other
            return Point(self.x - ox, self.y - oy, self.align, self.valign)

        return NotImplemented

    def __iter__(self):
        yield from [self.x, self.y]

def p(x, y):
    return Point(x, y)

def _coerce(other):
    if type(other) is Vec2:
        return (other.x, other.y)

    if type(other) is int:
        return (other, other)

    if type(other) is float:
        return (other, other)

    return None

class Vec2():
    __slots__ = ["x", "y"]
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        other = _coerce(other)
        if other is None:
            return NotImplemented

        (ox, oy) = other
        return Vec2(self.x + ox, self.y + oy)

    def __sub__(self, other):
        other = _coerce(other)
        if other is None:
            return NotImplemented

        (ox, oy) = other
        return Vec2(self.x - ox, self.y - oy)

    def __truediv__(self, other):
        other = _coerce(other)
        if other is None:
            return NotImplemented

        (ox, oy) = other
        return Vec2(self.x / ox, self.y / oy)

    def __mul__(self, other):
        other = _coerce(other)
        if other is None:
            return NotImplemented

        (ox, oy) = other
        return Vec2(self.x * ox, self.y * oy)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def unit(self):
        return self / self.length()

    def dot(self, other):
        other = _coerce(other)
        if other is None:
            return NotImplemented

        (ox, oy) = other
        return self.x * ox + self.y * oy

def p2v(point):
    return Vec2(point.x, point.y)

def v2p(vec, **kwargs):
    return Point(vec.x, vec.y, **kwargs)

class Square():
    def __init__(self, pos, w, h, fill="gray", stroke="black", stroke_width=1):
        self.pos = p2v(pos)
        self.w = w
        self.h = h
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width

    def bbox(self):
        return (self.pos, Vec2(self.w, self.h))

    def center(self):
        return v2p(self.pos + Vec2(self.w/2, self.h/2), align="middle", valign="middle")

    def left(self):
        return self.edge(math.pi)

    def right(self):
        return self.edge(0)

    def edge(self, theta):
        edges = (
            ((self.pos,                   self.w,  0), "middle", "alphabet"),
            ((self.pos + Vec2(self.w, 0), 0,       self.h), "start", "middle"),
            ((self.pos,                   0,       self.h), "end", "middle"),
            ((self.pos + Vec2(0, self.h), self.w,  0), "middle", "hanging"),
        )

        ray = p2v(self.center())
        for edge, align, valign in edges:
            t = line_intersect(*edge, ray, theta)
            if t is None or t < 0 or t > 1:
                continue

            return v2p(line_intersect_point(*edge, t), align=align, valign=valign)

        return None

    def draw(self):
        print(f"<rect x=\"{self.pos.x}\" y=\"{self.pos.y}\" width=\"{self.w}\" height=\"{self.h}\" fill=\"{self.fill}\" stroke=\"{self.stroke}\" stroke-width=\"{self.stroke_width}\" />")

class Group():
    def __init__(self, elems):
        self.elems = elems

    def bbox(self):
        bb_x = math.inf
        bb_y = math.inf
        bb_rx = -math.inf
        bb_by = -math.inf
        for elem in self.elems:
            (pos, size) = elem.bbox()
            bb_x = min(pos.x, bb_x)
            bb_y = min(pos.y, bb_y)
            bb_rx = max((pos + size).x, bb_rx)
            bb_by = max((pos + size).y, bb_by)

        bb_w = bb_rx - bb_x
        bb_h = bb_by - bb_y
        return (Vec2(bb_x, bb_y), Vec2(bb_w, bb_h))

    def draw(self):
        (pos, size) = self.bbox()

        # Add a margin
        pos -= 20
        size += 40

        print("<?xml version=\"1.0\" standalone=\"no\"?>")
        print(f"<svg viewBox=\"{pos.x} {pos.y} {size.x} {size.y}\" xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\">")

        for elem in self.elems:
            elem.draw()

        print("<\\svg>")

def proj(p1, p2, p3):
    (p1x, p1y) = p1
    (p2x, p2y) = p2
    (p3x, p3y) = p3
    p3x -= p1x
    p3y -= p1y
    p2x -= p1x
    p2y -= p1y

    p2l = math.sqrt(p2x ** 2 + p2y ** 2)
    up2x = p2x / p2l
    up2y = p2y / p2l

    dot = p3x * up2x + p3y * up2y
    dot = max(0, min(1, dot))
    return ((up2x * dot) + p1x, (up2y * dot) + p1y)

def vec_len(x, y):
    return math.sqrt(x ** 2 + y ** 2)

def dist(x1, y1, x2, y2):
    (p1x, p1y) = x1, y1
    (p2x, p2y) = x2, y2

    return vec_len(p2x-p1x, p2y-p1y)

def vec_unit(x, y):
    l = vec_len(x, y)
    return (x / l, y / l)

class MultiLine():
    def __init__(self, points, radius=5, stroke="black", stroke_width=1):
        self.points = [p2v(p) for p in points]
        self.radius = radius
        self.stroke = stroke
        self.stroke_width = stroke_width

    def bbox(self):
        xs = [p.x for p in self.points]
        ys = [p.y for p in self.points]
        x = min(xs)
        y = min(ys)
        w = max(xs) - x
        h = max(ys) - y
        return (Vec2(x, y), Vec2(w, h))

    def draw(self):
        cursor = 0

        current = self.points[cursor]
        cursor += 1
        print(f"<path d=\"", end="")
        print(f"M {current.x} {current.y}", end=" ")

        while cursor + 1 < len(self.points):
            # Get the current point and the 2 surrounding points
            last = current
            current = self.points[cursor]
            cursor += 1
            next_ = self.points[cursor]

            # Find the relative vectors from the current point to the
            # surrounders
            last -= current
            next_ -= current

            # Find the angle of the tangent. Since the curve is symmetrical,
            # it's the same for both
            # Start by finding the angle between the 3 points
            dot = next_.dot(last)
            angle = math.acos(dot / (next_.length() * last.length()))
            # The angle relative to the circle is then the complementary of
            # that
            angle = math.pi - angle
            angle /= 2

            # Now we just have to multiply the unit vector towards each
            # surrounder with the length of the tangent to find the curve start
            # and end
            unit_last = last.unit()
            unit_next = next_.unit()
            tanl = math.tan(angle) * self.radius
            beginround = current + unit_last * tanl
            endround = current + unit_next * tanl

            print(f"L {beginround.x} {beginround.y}", end=" ")
            print(f"Q {current.x} {current.y} {endround.x} {endround.y}", end=" ")

        current = self.points[cursor]
        cursor += 1
        print(f"L {current.x} {current.y}", end="")
        print(f"\" fill=\"none\" stroke=\"{self.stroke}\" stroke-width=\"{self.stroke_width}\" />")

class Text():
    def __init__(self, text, pos, fill="black", align=None, valign=None):
        self.pos = p2v(pos)
        self.text = text
        self.fill = fill

        if align is None:
            align = pos.align
        if align is None:
            align = "start"
        self.align = align

        if valign is None:
            valign = pos.valign
        if valign is None:
            valign = "middle"
        self.valign = valign

    def bbox(self):
        # @HACK We need to do some text shaping stuff here. Currently this
        # doesn't cover the whole text
        return (self.pos, Vec2(0, 0))

    def draw(self):
        print(f"<text x=\"{self.pos.x}\" y=\"{self.pos.y}\" fill=\"{self.fill}\" dominant-baseline=\"{self.valign}\" style=\"text-anchor: {self.align};\">{self.text}</text>")


@click.command()
def main():
    w, h = 100, 50
    n1 = Square(p(100, 100), w, h)
    n2 = Square(p(300, 200), w, h)
    l = MultiLine((n1.edge(0), n1.edge(0) + p(20, 0), p(250, 225), n2.edge(math.pi)), 10)

    t = Text("Hello World", n1.center())
    t2 = Text("Hello World", n1.edge(math.pi*1.5))

    g = Group((n1, n2, l, t, t2))
    g.draw()

if __name__ == '__main__':
    main()

