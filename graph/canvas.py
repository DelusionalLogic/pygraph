import math

from vec import Vec2

def size(bboxes):
    bb_x = math.inf
    bb_y = math.inf
    bb_rx = -math.inf
    bb_by = -math.inf
    for elem in bboxes:
        (pos, size) = elem
        bb_x = min(pos.x, bb_x)
        bb_y = min(pos.y, bb_y)
        bb_rx = max((pos + size).x, bb_rx)
        bb_by = max((pos + size).y, bb_by)

    bb_w = bb_rx - bb_x
    bb_h = bb_by - bb_y
    return (Vec2(bb_x, bb_y), Vec2(bb_w, bb_h))

def size_and_write_preamble(write, bbox_or_bboxes):
    bbox = size(bbox_or_bboxes)
    write_preamble(write, bbox)

def write_preamble(write, bbox):
    (pos, dim) = bbox

    # Add a margin
    pos -= 20
    dim += 40

    write("<?xml version=\"1.0\" standalone=\"no\"?>\n")
    write(f"<svg viewBox=\"{pos.x} {pos.y} {dim.x} {dim.y}\" xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\">\n")


def write_tail(write):
    write("</svg>")
