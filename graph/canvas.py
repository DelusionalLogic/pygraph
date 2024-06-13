import math

from vec import (
    Mat4,
    Vec2,
)


def size(bboxes):
    bb_x = math.inf
    bb_y = math.inf
    bb_rx = -math.inf
    bb_by = -math.inf
    for elem in bboxes:
        (pos, (w, h)) = elem

        # The logic here is that we calculate that we find the 4 corners of the
        # bbox, then transform it, and then find the bbox of that new shape.
        # It's not quite precise, but it's enough for now
        ps = [
            Vec2(0, 0, 0),
            Vec2(w, 0, 0),
            Vec2(w, h, 0),
            Vec2(0, h, 0),
        ]

        for i, p in enumerate(ps):
            ps[i] = pos * p

        for p in ps:
            bb_x = min(p.x, bb_x)
            bb_y = min(p.y, bb_y)
            bb_rx = max(p.x, bb_rx)
            bb_by = max(p.y, bb_by)


    bb_w = bb_rx - bb_x
    bb_h = bb_by - bb_y
    return (Mat4.translate(bb_x, bb_y), Vec2(bb_w, bb_h))

def size_and_write_preamble(write, bbox_or_bboxes):
    bbox = size(bbox_or_bboxes)
    write_preamble(write, bbox)

def write_preamble(write, bbox):
    (pos, dim) = bbox

    # Add a margin
    pos *= Mat4.translate(-20, -20)
    dim += 40

    write("<?xml version=\"1.0\" standalone=\"no\"?>\n")
    write(f"<svg viewBox=\"{pos.as_vec().x} {pos.as_vec().y} {dim.x} {dim.y}\" xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\">\n")


def write_tail(write):
    write("</svg>")
