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
    path_hvh,
    path_vh,
    path_vhv,
    realign,
    tpoint,
)
from node import (
    Circle,
)
from vec import (
    Mat4,
    Vec2,
)


def draw(render):
    # @HACK since text doesn't have a bounding box
    (fitp, w, h) = node.fit(render, 40)
    canvas.write_preamble(sys.stdout.write, (fitp.position, Vec2(w, h)))

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
# r1()

def r2():
    rot45 = Mat4.rotz(math.pi * 0.25)

    n1 = Circle(p(0, 0, HDir.MIDDLE, VDir.MIDDLE), 20)
    renderable.append(n1)
    n1_label = node.Text("Opened", push(n1.anchor(0), 0))
    renderable.append(n1_label)

    n2 = Circle(adjust(n1.anchor(VDir.BELOW), (0, 20)), 20)
    renderable.append(n2)
    n2_label = node.Text("Applied", push(n2.anchor(math.pi/4), 0))
    renderable.append(n2_label)

    renderable.append(a1 := node.MultiLine(path(n1.anchor(VDir.BELOW), n2.anchor(VDir.ABOVE)), 10))
    renderable.append(node.Text("Apply", push(realign(a1.edge(0, .5), HDir.LEFT, VDir.MIDDLE), 5)))

    below2 = push(n2.anchor(VDir.BELOW), 30)

    n3 = Circle(realign(adjust(below2, (20, 0)), HDir.RIGHT), 20)
    renderable.append(n3)
    renderable.append(Circle(n3.center(), 15))
    n3_label = node.Text("Effectuated", push(n3.anchor(HDir.RIGHT), 0))
    renderable.append(n3_label)

    into = node.MultiLine(path_hv(n2.anchor(HDir.RIGHT), n3.anchor(VDir.ABOVE)), 5)
    renderable.append(into)
    renderable.append(node.Text("Eff. Last", push(realign(into.edge(1, .7), HDir.RIGHT, VDir.MIDDLE), 5)))

    partly = Circle(realign(adjust(below2, (-20, 0)), HDir.LEFT), 20)
    renderable.append(partly)
    partly_label = node.Text("Part Eff.", push(partly.anchor(VDir.BELOW, HDir.LEFT), 0))
    renderable.append(partly_label)

    into = node.MultiLine(path_hv(n2.anchor(HDir.LEFT), partly.anchor(VDir.ABOVE)), 5)
    renderable.append(into)
    renderable.append(node.Text("Eff. Part", push(realign(into.edge(1, .7), HDir.RIGHT, VDir.MIDDLE), 5)))
    renderable.append(partly_loop := node.MultiLine(path(partly.anchor(math.pi*1.4), push(partly.anchor(math.pi*1.4), 20), push(partly.anchor(math.pi*1.6), 20), partly.anchor(math.pi*1.6)), 5))
    renderable.append(node.Text("Eff. Part", push(realign(partly_loop.edge(1, .5), HDir.MIDDLE, VDir.ABOVE), 5)))

    partly_n3 = node.MultiLine(path(partly.anchor(HDir.RIGHT), n3.anchor(HDir.LEFT)), 5)
    renderable.append(partly_n3)
    renderable.append(node.Text("Eff. Last", tpoint(adjust(realign(partly_n3.edge(0, .5), HDir.RIGHT, VDir.ABOVE), (0, 5)), rot45)))

    end = Circle(push(n2.anchor(HDir.LEFT), 60), 20)
    renderable.append(end)
    renderable.append(Circle(end.center(), 15))
    end_label = node.Text("Cancelled", push(end.anchor(VDir.ABOVE), 0))
    renderable.append(end_label)

    apply_end = node.MultiLine(path(n2.anchor(HDir.LEFT), end.anchor(HDir.RIGHT)), 5)
    renderable.append(apply_end)
    renderable.append(node.Text("Cancel", push(realign(apply_end.edge(0, .5), HDir.MIDDLE, VDir.BELOW), 5)))

    partly_end = node.MultiLine(path_hv(partly.anchor(HDir.LEFT), end.anchor(VDir.BELOW)), 5)
    renderable.append(partly_end)
    renderable.append(node.Text("Cancel", push(realign(partly_end.edge(1, .5), HDir.LEFT, VDir.MIDDLE), 5)))

    # The starting line
    into1 = adjust(n1.anchor(VDir.ABOVE), (0, -20))
    renderable.append(lin1 := node.MultiLine(path(into1, n1.anchor(VDir.ABOVE)), 10))
    renderable.append(node.Text("Open", push(realign(lin1.edge(0, .5), HDir.LEFT, VDir.MIDDLE), 5)))
r2()

def r3():
    rot45 = Mat4.rotz(math.pi * 0.25)

    renderable.append(n1 := Circle(p(200, 0, HDir.MIDDLE, VDir.MIDDLE), 20))
    renderable.append(node.Text("Pending", push(n1.anchor(0), 0)))

    into1 = adjust(n1.anchor(VDir.ABOVE), (0, -20))
    renderable.append(lin1 := node.MultiLine(path(into1, n1.anchor(VDir.ABOVE)), 10))
    renderable.append(node.Text("Eff. Last", push(realign(lin1.edge(0, .5), HDir.LEFT, VDir.MIDDLE), 5)))

    renderable.append(n2 := Circle(adjust(n1.anchor(VDir.BELOW), (0, 20)), 20))
    renderable.append(node.Text("Complete", push(n2.anchor(0), 0)))
    renderable.append(Circle(n2.center(), n1.r - 5))

    renderable.append(a1 := node.MultiLine(path(n1.anchor(VDir.BELOW), n2.anchor(VDir.ABOVE)), 10))
    renderable.append(node.Text("Cleaned", push(realign(a1.edge(0, .5), HDir.LEFT, VDir.MIDDLE), 5)))

    renderable.append(manual := Circle(push(n2.anchor(HDir.LEFT), 20), 20))
    renderable.append(node.Text("Manual", push(manual.anchor(math.pi), 0)))

    renderable.append(pending_manual := node.MultiLine(path_hv(n1.anchor(HDir.LEFT), manual.anchor(VDir.ABOVE)), 10))
    renderable.append(node.Text("Fail", push(realign(pending_manual.edge(0, .5), HDir.MIDDLE, VDir.BELOW), 5)))

    renderable.append(manual_n2 := node.MultiLine(path(manual.anchor(HDir.RIGHT), n2.anchor(HDir.LEFT)), 10))
    renderable.append(node.Text("Resolve", tpoint(adjust(realign(manual_n2.edge(0, .5), HDir.RIGHT, VDir.ABOVE), (0, 5)), rot45)))
r3()

draw(renderable)
