from __future__ import annotations
import math

from protocols import _JPoint2

class Point2:
    x: int
    y: int
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
    
    @staticmethod
    def java(value: _JPoint2) -> Point2:
        return Point2.unpack(value.pack())

    @staticmethod
    def unpack(pos: _JPoint2) -> Point2:
        x = (pos >> 16) & 0xFFFF
        y = pos & 0xFFFF
        if x & 0x8000:
            x -= 0x10000
        if y & 0x8000:
            y -= 0x10000
        return Point2(x, y)