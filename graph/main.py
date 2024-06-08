#!/usr/bin/env python3
import math
import sys
from enum import (
    Enum,
    auto,
)

import numpy as np

import canvas
import common
import node
from common import (
    HDir,
    Point,
    VDir,
    p,
    path_hv,
    path_hvh,
    path_vh,
    path_vhv,
    v2p,
)
from node import (
    Circle,
    Square,
)
from vec import (
    Mat3,
)

WHITE = node.Color(255, 255, 255)
RED = node.Color(255, 0, 0)
GREEN = node.Color(0, 255, 0)
BLUE = node.Color(0, 0, 255)
PURPLE = node.Color(255, 0, 255)

w, h = 100, 50
pad = 50
pad_fit = 10

mat = Mat3.identity()
mat = Mat3.roty(theta=math.pi/4) * mat
mat = Mat3.rotz(theta=math.pi/4) * mat

thing_box = Square(p(0, 0), w, h, fill=BLUE.lerp(WHITE, .8), transform=mat)
thing_label = node.Text("Thing", node.center(thing_box))

other_box = Square(node.offset(thing_box.anchor(VDir.MIDDLE, HDir.RIGHT), dist=pad), w, h, fill=RED.lerp(WHITE, .8))
other_label = node.Text("Other", other_box.center())

(fitpos, fitw, fith) = node.fit((thing_box, other_box), 0)
large_box = Square(v2p(fitpos.position + (0, fith + pad)), fitw, fith, fill=PURPLE.lerp(WHITE, .8))
large_label = node.Text("Large", large_box.center())

(fitpos, fitw, fith) = node.fit((thing_box, other_box, large_box), pad_fit)
container = Square(fitpos, fitw, fith)

below_box = Square(p(large_box.pos.x, container.pos.y + container.h + pad), w, h)
below_box = Circle(node.offset(other_box.anchor(VDir.MIDDLE, HDir.RIGHT), dist=pad+pad_fit), h/2, fill=GREEN.lerp(WHITE, .8))
below_label = node.Text("Below", node.offset(below_box.anchor(VDir.BELOW), 4))

tl_l = node.MultiLine(path_vh(thing_box.anchor(VDir.BELOW), large_box.anchor(VDir.ABOVE))[:-1], 0)
ol_l = node.MultiLine(path_vh(other_box.anchor(VDir.BELOW), large_box.anchor(VDir.ABOVE))[:-1], 0)

tl_l = node.MultiLine(path_vhv(thing_box.anchor(VDir.BELOW), large_box.anchor(VDir.ABOVE)), 10)
ol_l = node.MultiLine(path_vhv(other_box.anchor(VDir.BELOW), large_box.anchor(VDir.ABOVE)), 10)

lb_l = node.MultiLine(path_hvh(large_box.anchor(HDir.RIGHT), below_box.anchor(HDir.LEFT)), 10)
lb_l_label = node.Text("End it!", node.offset(lb_l.edge(1, 50), 2))

g = (
    container,
    thing_box,
    thing_label,
    other_box,
    other_label,
    large_box,
    large_label,
    below_box,
    below_label,
    tl_l,
    ol_l,
    lb_l,
    lb_l_label,
)

bboxes = [x.bbox() for x in g]
canvas.size_and_write_preamble(sys.stdout.write, bboxes)

for elem in g:
    elem.draw(sys.stdout.write)

canvas.write_tail(sys.stdout.write)

sys.stdout.flush()

