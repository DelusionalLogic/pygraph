import math

import vec

def canvas_size(bboxes):
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
