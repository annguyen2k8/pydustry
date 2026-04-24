import math
from typing import List, Type

from arc.math import Angles
from arc.math.geom import Point2 as JPoint2
from jpype import JArray
from mindustry.world import Block
from mindustry.world.blocks.power import PowerNode

from geom import Point2
from models import TileData
from renders.block import BlockRender
from variables import *


class PowerNodeRender(BlockRender):
    target: Type[Block] = PowerNode
    
    current_find_x: int
    current_find_y: int
    current_tile: TileData
    
    def tile_finder(self, other: TileData) -> bool:
        return (
            self.current_find_x >= other.x - ((other.block.size - 1) / 2) and
            self.current_find_y >= other.y - ((other.block.size - 1) / 2) and
            self.current_find_x <= other.x + other.block.size / 2 and
            self.current_find_y <= other.y + other.block.size / 2 and
            other != self.current_tile and
            other.block.hasPower
            )
    
    def draw_config_top(self, image, tile, tiles):
        if isinstance(tile.config, JArray(JPoint2)):
            ps: List[Point2] = map(Point2.java ,tile.config)
            for pos in ps:
                
                self.current_find_x = tile.x + pos.x
                self.current_find_y = tile.y + pos.y
                self.current_tile = tile
                
                other_tile = self.find_tile(tiles, self.tile_finder, self.current_find_x, self.current_find_y)
                
                if other_tile is None:
                    continue
                
                ...
            
    
    def draw_lazer(self, x1: float, y1: float, x2: float, y2: float, size1: int, size2: int, light: bool = True) -> None:
        
        angle1: float = Angles.angle(x1, y1, x2, y2)
        vx: float = math.cos(math.radians(angle1))
        vy: float = math.sin(math.radians(angle1))
        len1: float = size1 * tilesize / 2 - 1.5
        len2: float = size2 * tilesize / 2 - 1.5
        
        