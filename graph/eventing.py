import math
import sys

import canvas
import node
from common import (
    HDir,
    VDir,
    adjust,
    p,
    path,
    path_hv,
    path_vh,
    realign,
)
from node import (
    Circle,
    Square,
)
from vec import (
    Mat4,
    Vec2,
)

WHITE = node.Color(255, 255, 255)
BLUE = node.Color(0, 0, 255)

def draw(render):
    bboxes = [x.bbox() for x in render]
    canvas.size_and_write_preamble(sys.stdout.write, bboxes)

    for elem in render:
        elem.draw(sys.stdout.write)

    canvas.write_tail(sys.stdout.write)

sys.stdout.flush()

renderable = []

def push(pos, dist):
    (xoff, yoff) = (0, 0)

    if pos.valign is  VDir.BELOW:
        yoff = -dist
    elif pos.valign is  VDir.ABOVE:
        yoff = dist

    # This seems wrong
    if pos.halign is  HDir.LEFT:
        xoff = -dist
    elif pos.halign is  HDir.RIGHT:
        xoff = dist

    return adjust(pos, (xoff, yoff))

def r1():
    n1 = Circle(p(0, 0, HDir.MIDDLE, VDir.MIDDLE), 20)
    renderable.append(n1)
    renderable.append(Circle(n1.center(), 15))
    n2 = Circle(adjust(n1.anchor(VDir.BELOW), (0, 20)), 20)
    renderable.append(n2)
    n3 = Circle(adjust(n2.anchor(VDir.BELOW), (0, 20)), 20)
    renderable.append(n3)

    into1 = adjust(n1.anchor(VDir.ABOVE), (0, -20))
    leftof1 = adjust(n1.anchor(HDir.LEFT), (-20, 0))

    lin1 = node.MultiLine(path(into1, n1.anchor(VDir.ABOVE)), 10)
    renderable.append(lin1)
    a1 = node.MultiLine(path(n1.anchor(VDir.BELOW), n2.anchor(VDir.ABOVE)), 10)
    renderable.append(a1)
    a2 = node.MultiLine(path(n2.anchor(VDir.BELOW), n3.anchor(VDir.ABOVE)), 10)
    renderable.append(a2)
    aback = node.MultiLine(path(path_hv(n3.anchor(HDir.LEFT), leftof1), n1.anchor(HDir.LEFT)), 5)
    renderable.append(aback)

    n1_label = node.Text("A=1;B=0", push(n1.anchor(0), 5))
    renderable.append(n1_label)
    n2_label = node.Text("A=2;B=0", push(n2.anchor(0), 5))
    renderable.append(n2_label)
    n3_label = node.Text("A=1;B=1", push(n3.anchor(0), 5))
    renderable.append(n3_label)

    a1_label = node.Text("A++", push(realign(a1.edge(0, .5), HDir.RIGHT, VDir.MIDDLE), 5))
    renderable.append(a1_label)
    a2_label = node.Text("A--;B++", push(realign(a2.edge(0, .5), HDir.RIGHT, VDir.MIDDLE), 5))
    renderable.append(a2_label)
    a3_label = node.Text("B--", push(realign(aback.edge(1, .5), HDir.LEFT, VDir.MIDDLE), 5))
    renderable.append(a3_label)
r1()

draw(renderable)
