from dataclasses import dataclass

from protocols import _Block


@dataclass
class TileData:
    block: _Block
    x: int
    y: int
    rotate: int
    config: object
    draw_x: int
    draw_y: int
    draw_size: int