from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Callable, List, Optional, Type

from mindustry.world import Block
from PIL import Image

from models import TileData
from sprites import Sprites

if TYPE_CHECKING:
    from render import Renders

from render import BaseRender
from variables import *


class BlockRender(BaseRender):
    target: Type[Block] = Block
    texture: Image.Image
    
    
    def __init__(self):
        super().__init__()
        
        self.texture = Image.Image()
    
    
    @staticmethod
    def load_sprite(name: str = "texture", *, value: str = "@", fallback: Optional[str] = None) -> Callable:
        def decoration(func: Callable):
            @wraps(func)
            def wrapper(render: BlockRender, image: Image.Image, tile: TileData, *args, **kwargs) -> Callable:
                sprite: Sprites.Sprite = sprites.find(value.replace("@", str(tile.block.name)), fallback)
                
                if name in render.__dict__:
                    setattr(render, name, sprite.image())
                
                return func(render, image, tile, *args, **kwargs)
            
            return wrapper
        return decoration
    
    @load_sprite()
    def draw_default(self, image: Image.Image, tile: TileData, tiles: List[TileData]):
        image.paste(
            self.texture.resize((tile.draw_size, tile.draw_size)).rotate(tile.rotate), 
            (tile.draw_x, tile.draw_y)
            )
        
        self.draw_config(image, tile, tiles)

    def draw_config(self, image: Image.Image, tile: TileData, tiles: List[TileData]):
        ...
        
    def draw_config_top(self, image: Image.Image, tile: TileData, tiles: List[TileData]):
        ...
    
    @staticmethod
    def find_tile(tiles: List[TileData], predicate: Callable[[TileData, ], bool], x:int, y: int, size: int = 1) -> Optional[TileData]:
        for tile in tiles:
            if (tile.x == x and tile.y == y) and tile.block.size == size:
                if not predicate(tile):
                    continue
                
                return tile
        
        return None