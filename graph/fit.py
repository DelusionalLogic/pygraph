from vec import Vec2
from common import (
    p,
    VDir,
    HDir,
    Point,
    adjust,
)

class Box():
    def __init__(self, point, width, height):
        self.point = point
        self.width = width
        self.height = height

def containing(elements, pad):
    (pos, size) = elements[0].bbox()
    x_low = pos.x
    y_low = pos.y
    x_high = size.x + x_low
    y_high = size.y + y_low

    for e in elements[1:]:
        (pos, size) = e.bbox()
        x_low = min(x_low, pos.x)
        y_low = min(y_low, pos.y)
        x_high = max(x_high, pos.x + size.x)
        y_high = max(y_high, pos.y + size.y)

    return Box(p(x_low - pad, y_low - pad, HDir.RIGHT, VDir.BELOW), x_high - x_low + pad*2, y_high - y_low + pad*2)


def grow_box(box, distance, direction):
    if type(direction) is VDir:
        box.height += distance
        if box.point.valign.inv() == direction:
            box.point = adjust(box.point, Vec2(0, direction.direction() * distance))
    elif type(direction) is HDir:
        box.width += distance
        if box.point.halign.inv() == direction:
            box.point = adjust(box.point, Vec2(direction.direction() * distance, 0))

def grow_box_to(box, value, direction):
    if type(value) is Point:
        if type(direction) is VDir:
            value = value.position.y
        elif type(direction) is HDir:
            value = value.position.x
        else:
            raise TypeError

    if type(direction) is VDir:
        if box.point.valign.inv() == direction:
            current_value = box.point.position.y
        else:
            current_value = box.point.position.y + (box.height * box.point.valign.direction())
    elif type(direction) is HDir:
        if box.point.halign == direction:
            current_value = box.point.position.x
        else:
            current_value = box.point.position.x + (box.width * box.point.halign.direction())
    else:
        raise TypeError

    grow_box(box, (value - current_value) * direction.direction(), direction)

