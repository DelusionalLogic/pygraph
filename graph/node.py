import math

import canvas
from common import (
    HDir,
    Point,
    VDir,
    p,
    v2p,
)
from vec import (
    Mat4,
    Vec2,
)


def fit(nodes, pad):
    (min, size) = canvas.size([x.bbox() for x in nodes])
    size += pad*2
    return (v2p(min * Mat4.translate(-pad, -pad), HDir.RIGHT, VDir.BELOW), size.x, size.y)

class Color():
    def __init__(self, r, g, b, a = 1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def lerp(self, other, factor):
        r = (1 - factor) * self.r + factor * other.r
        g = (1 - factor) * self.g + factor * other.g
        b = (1 - factor) * self.b + factor * other.b
        a = (1 - factor) * self.a + factor * other.a
        return Color(r, g, b, a)

    def formatHtml(self):
        return f"rgb({self.r}, {self.g}, {self.b})"

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

def square_edge(width, height, theta):
    edges = (
        ((Vec2(0, 0),     width,   0),      HDir.MIDDLE, VDir.ABOVE),
        ((Vec2(width, 0), 0,       height), HDir.RIGHT, VDir.MIDDLE),
        ((Vec2(0, 0),     0,       height), HDir.LEFT, VDir.MIDDLE),
        ((Vec2(0, height), width,  0),      HDir.MIDDLE, VDir.BELOW),
    )

    ray = Vec2(width/2, height/2)
    for edge, align, valign in edges:
        t = line_intersect(*edge, ray, theta)
        if t is None or t < 0 or t > 1:
            continue

        cross = line_intersect_point(*edge, t)
        return v2p(Mat4.translate(cross.x, cross.y), halign=align, valign=valign)

    raise TypeError

def square_anchor(width, height, *args):
    if args == (HDir.RIGHT,) or args == (VDir.MIDDLE, HDir.RIGHT):
        return square_edge(width, height, 0)
    elif args == (VDir.ABOVE, HDir.RIGHT):
        return p(width, 0, halign=HDir.RIGHT, valign=VDir.ABOVE)
    elif args == (VDir.ABOVE,) or args == (VDir.ABOVE, HDir.MIDDLE):
        return square_edge(width, height, math.pi*0.5)
    elif args == (VDir.ABOVE, HDir.LEFT):
        return p(0, 0, halign=HDir.LEFT, valign=VDir.ABOVE)
    elif args == (HDir.LEFT,) or args == (VDir.MIDDLE, HDir.LEFT):
        return square_edge(width, height, math.pi)
    elif args == (VDir.BELOW, HDir.LEFT):
        return v2p(Vec2(0, height), halign=HDir.LEFT, valign=VDir.BELOW)
    elif args == (VDir.BELOW,) or args == (VDir.BELOW, HDir.MIDDLE):
        return square_edge(width, height, math.pi*1.5)
    elif args == (VDir.BELOW, HDir.RIGHT):
        return p(width, height, halign=HDir.RIGHT, valign=VDir.BELOW)
    elif args == (VDir.MIDDLE, HDir.MIDDLE):
        return p(width/2, height/2, halign=HDir.MIDDLE, valign=VDir.MIDDLE)

    if type(args[0]) is int or type(args[0]) is float:
        return square_edge(width, height, args[0])

    raise TypeError

def square_extents(width, height):
    return Mat4.translate(width, height)

def square_write(write, width, height, position, fill, fill_opacity, stroke, stroke_width):
    write(f"<path d=\"")
    p = position * Vec2(0, 0)
    write(f"M {p.x} {p.y} ")
    p = position * Vec2(width, 0)
    write(f"L {p.x} {p.y} ")
    p = position * Vec2(width, height)
    write(f"L {p.x} {p.y} ")
    p = position * Vec2(0, height)
    write(f"L {p.x} {p.y} ")
    write(f"Z")
    write(f"\" fill=\"{fill}\" fill-opacity=\"{fill_opacity}\" stroke=\"{stroke}\" stroke-width=\"{stroke_width}\" ")
    write(" />")

def square_position_point(point, width, height):
    xoff = None
    if point.halign == HDir.MIDDLE:
        xoff = width/2
    elif point.halign == HDir.RIGHT:
        xoff = 0
    elif point.halign == HDir.LEFT:
        xoff = width
    elif point.halign is None:
        xoff = width/2
    else:
        raise NotImplementedError

    yoff = None
    if point.valign == VDir.MIDDLE:
        yoff = height/2
    elif point.valign == VDir.BELOW:
        yoff = 0
    elif point.valign == VDir.ABOVE:
        yoff = height
    elif point.valign is None:
        yoff = height/2
    else:
        raise NotImplementedError

    return point.position * Mat4.translate(-xoff, -yoff)

def center(shape):
    return shape.anchor(VDir.MIDDLE, HDir.MIDDLE)

class Square():
    def __init__(self, pos, w, h, fill=Color(255, 255, 255), stroke="black", stroke_width=1):
        self.pos = square_position_point(pos, w, h)
        self.w = w
        self.h = h
        self.fill = "none" if fill is None else fill.formatHtml()
        self.fill_opacity = "none" if fill is None else fill.a
        self.stroke = stroke
        self.stroke_width = stroke_width

    def bbox(self):
        return (self.pos, (self.w, self.h))

    def center(self):
        return v2p(self.pos * Mat4.translate(self.w/2, self.h/2), halign=HDir.MIDDLE, valign=VDir.MIDDLE)

    def anchor(self, *args):
        point = square_anchor(self.w, self.h, *args)
        if point is None:
            return None

        pos = (self.pos * point.position)
        return v2p(pos, point.halign, point.valign)

    def edge(self, theta):
        point = square_edge(self.w, self.h, theta)
        if point is None:
            return None

        return v2p(self.pos + point.position, point.halign, point.valign)

    def draw(self, write):
        square_write(write, self.w, self.h, self.pos, self.fill, self.fill_opacity, self.stroke, self.stroke_width)

class Circle():
    def __init__(self, pos, r, fill=None, stroke="black", stroke_width=1):
        self.pos = pos.position
        self.r = r
        self.fill = "none" if fill is None else fill.formatHtml()
        self.fill_opacity = "none" if fill is None else fill.a
        self.stroke = stroke
        self.stroke_width = stroke_width

        xoff = 0
        if pos.halign == HDir.RIGHT:
            xoff = -r
        elif pos.halign == HDir.LEFT:
            xoff = r

        yoff = 0
        if pos.valign == VDir.BELOW:
            yoff = r
        elif pos.valign == VDir.ABOVE:
            yoff = -r

        self.pos *= Mat4.translate(-xoff, -yoff)

    def bbox(self):
        return (self.pos * Mat4.translate(-self.r, -self.r), (self.r*2, self.r*2))

    def center(self):
        return v2p(self.pos, halign=HDir.MIDDLE, valign=VDir.MIDDLE)

    def anchor(self, *args):
        if len(args) > 2:
            raise NotImplementedError
        if len(args) <= 0:
            raise NotImplementedError

        if args == (HDir.RIGHT,) or args == (VDir.MIDDLE, HDir.RIGHT):
            return self.edge(0)
        elif args == (VDir.ABOVE, HDir.RIGHT):
            return self.edge(math.pi*0.25)
        elif args == (VDir.ABOVE,) or args == (VDir.ABOVE, HDir.MIDDLE):
            return self.edge(math.pi*0.5)
        elif args == (VDir.ABOVE, HDir.LEFT):
            return self.edge(math.pi*0.75)
        elif args == (HDir.LEFT,) or args == (VDir.MIDDLE, HDir.LEFT):
            return self.edge(math.pi)
        elif args == (VDir.BELOW, HDir.LEFT):
            return self.edge(math.pi*1.25)
        elif args == (VDir.BELOW,) or args == (VDir.BELOW, HDir.MIDDLE):
            return self.edge(math.pi*1.5)
        elif args == (VDir.BELOW, HDir.RIGHT):
            return self.edge(math.pi*1.75)
        elif args == (VDir.MIDDLE, HDir.MIDDLE):
            return self.center()
        elif args == (HDir.MIDDLE,):
            return self.center()
        elif args == (VDir.MIDDLE,):
            return self.center()

        if type(args[0]) is int or type(args[0]) is float:
            return self.edge(args[0])

        raise TypeError

    def edge(self, theta):
        theta = abs(theta) % (math.pi * 2)
        ray = Vec2(math.cos(theta), -math.sin(theta))
        theta /= math.pi

        if theta <= 0.375 or theta >= 1.625:
            align = HDir.RIGHT
        elif theta >= 0.625 and theta <= 1.375:
            align = HDir.LEFT
        else:
            align = HDir.MIDDLE

        if theta >= 0.125 and theta <= 0.875:
            valign = VDir.BELOW
        elif theta >= 1.125 and theta <= 1.875:
            valign = VDir.ABOVE
        else:
            valign = VDir.MIDDLE

        mat = Mat4.translate(ray.x * self.r, ray.y * self.r)
        return v2p(self.pos * mat, halign=align, valign=valign)

    def draw(self, write):
        write(f"<circle r=\"{self.r}\" fill=\"{self.fill}\" fill-opacity=\"{self.fill_opacity}\" stroke=\"{self.stroke}\" stroke-width=\"{self.stroke_width}\" {transform_str(self.pos)} />\n")

def grid_offset(point, hdist=100, vdist=100):
    hdir = point.halign
    vdir = point.valign
    return Point(
        point.position + Vec2(hdist * hdir.direction(), vdist * vdir.direction()),
        point.halign,
        point.valign,
    )

def offset(point, dist=100):
    hdir = point.halign
    vdir = point.valign

    offset = Mat4.translate(hdir.direction() * dist, vdir.direction() * dist)

    return Point(
        point.position * offset,
        point.halign,
        point.valign,
    )

class MultiLine():
    def __init__(self, points, radius=5, stroke="black", stroke_width=1):
        self.points = [p.position.as_vec() for p in points]
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
        return (Mat4.translate(x, y), (w, h))

    def edge(self, segment, t):
        assert segment >= 0
        assert segment < len(self.points)
        assert segment >= 0 and segment <= 100

        start = self.points[segment]
        end = self.points[segment+1]

        line = end - start
        line_len = line.length()
        intended_len = line_len * t

        # @HACK @INCOMPLETE: Right now we aren't doing anything to follow the
        # curve. We should be calculating the same arc as we do when rendering,
        # and using that to control the position. In most cases though, the
        # radius will be so small, so it shouldn't really matter much.

        theta = line.angle()
        part = round((theta / math.tau) * 8)
        (hdir, vdir) = [
            (HDir.MIDDLE, VDir.BELOW),
            (HDir.RIGHT, VDir.BELOW),
            (HDir.RIGHT, VDir.MIDDLE),
            (HDir.LEFT, VDir.BELOW),
            (HDir.MIDDLE, VDir.BELOW),
            (HDir.RIGHT, VDir.BELOW),
            (HDir.RIGHT, VDir.MIDDLE),
            (HDir.LEFT, VDir.BELOW),
        ][part]

        vec = start + line.unit() * intended_len
        mat = Mat4.translate(vec.x, vec.y)
        return v2p(mat, halign=hdir, valign=vdir)

    def draw(self, write):
        write("<defs>\n")
        write("<marker id=\"arrowhead\" markerWidth=\"10\" markerHeight=\"7\" refX=\"0\" refY=\"3.5\" orient=\"auto\">\n")
        write("<polygon points=\"0 0, 10 3.5, 0 7\" />\n")
        write("</marker>\n")
        write("</defs>\n")
        head_length = 10

        cursor = 0

        current = self.points[cursor]
        cursor += 1
        write(f"<path d=\"")
        write(f"M {current.x} {current.y} ")

        if self.radius > 0:
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

                write(f"L {beginround.x} {beginround.y} ")
                write(f"Q {current.x} {current.y} {endround.x} {endround.y} ")
        else:
            while cursor + 1 < len(self.points):
                current = self.points[cursor]
                cursor += 1
                write(f"L {current.x} {current.y} ")

        last = current
        current = self.points[cursor]
        cursor += 1

        delta = current - last
        if delta.length() <= head_length:
            raise Exception("Head is longer than distance between points")
        end = current - delta.unit() * head_length

        write(f"L {end.x} {end.y}")
        write(f"\" fill=\"none\" stroke=\"{self.stroke}\" stroke-width=\"{self.stroke_width}\"\n")
        write(f"marker-end=\"url(#arrowhead)\"\n")
        write(" />")

def _align_to_str(align):
    if align is None:
        return "middle"

    return {
        VDir.ABOVE: "hanging",
        VDir.MIDDLE: "middle",
        VDir.BELOW: "alphabet",

        HDir.LEFT: "end",
        HDir.MIDDLE: "middle",
        HDir.RIGHT: "start",
    }[align]

def transform_str(transform):
    if transform is None:
        return ""

    m = transform.inner
    return f"transform=\"matrix({m[0, 0]} {m[1, 0]} {m[0, 1]} {m[1, 1]} {m[0, 3]} {m[1, 3]})\""

class Text():
    def __init__(self, text, pos, fill="black", transform = Mat4.identity()):
        self.pos = pos.position
        self.text = text
        self.fill = fill
        self.align = _align_to_str(pos.halign)
        self.valign = _align_to_str(pos.valign)

        self.transform = transform

    def bbox(self):
        # @INCOMPLETE
        return (self.pos, (1, 1))

    def draw(self, write):
        write(f"<text fill=\"{self.fill}\" dominant-baseline=\"{self.valign}\" style=\"text-anchor: {self.align};\" {transform_str(self.pos)} >{self.text}</text>\n")
