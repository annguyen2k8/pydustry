from __future__ import annotations

import sys
import time
from typing import Any, Callable, List

import jpype
import jpype.imports
from PIL import Image

classpath: str = "./build/Mindustry.jar"

if not jpype.isJVMStarted():
    jpype.startJVM(
        jpype.getDefaultJVMPath(),
        "--enable-native-access=ALL-UNNAMED",
        classpath=classpath
    )

from arc.files import Fi
from mindustry import Vars
from mindustry.content import Blocks, Items, Liquids
from mindustry.core import ContentLoader, Version
from mindustry.ctype import ContentType
from mindustry.game import Schematics

from models import TileData
from protocols import _Schematic
from render import Renders
from renders import *
from variables import *


def main(*args: Any) -> int:
    Version.enabled = False

    Vars.content = ContentLoader()
    
    # only necessary content
    Items.load()
    Liquids.load()
    Blocks.load()
    
    for ctype in ContentType.all:
        for content in Vars.content.getBy(ctype):
            try:
                content.init()
            except:
                pass

    
    schem: _Schematic = Schematics.read(Fi(args[1]))
    
    ts = time.time()
    
    image: Image.Image = Image.new("RGBA", (schem.width * tilesize, schem.height * tilesize))
    
    
    tiles: List[TileData] = tuple(map(
        lambda tile: TileData(
                tile.block, tile.x, tile.y, 
                tile.rotation * 90 if tile.block.rotate else 0,
                tile.config,
                int((tile.x + tile.block.sizeOffset) * tilesize),
                int((schem.height - tile.y - tile.block.size - tile.block.sizeOffset) * tilesize),
                tile.block.size * tilesize
            ),
        schem.tiles
        ))
    
    
    renders: Renders = Renders()
    
    def foreach_tile(callback: Callable[[BlockRender, TileData], None]):
        for tile in tiles:
            render = renders.get_render(tile.block, BlockRender)
            
            if render:
                callback(render, tile)
    
    def draw_default(render: BlockRender, tile: TileData):
        render.draw_default(image, tile, tiles)
    
    def draw_top_config(render: BlockRender, tile: TileData):
        render.draw_config_top(image, tile, tiles)
    
    foreach_tile(draw_default)
    foreach_tile(draw_top_config)
    
    print("Done in" , f"{round(time.time() - ts)}ms")
    
    image.show() 
    
    return 0

if __name__ == "__main__":
    exit(main(*sys.argv))
