from __future__ import annotations

import sys
import time
from typing import Any

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
from mindustry.core import ContentLoader, Version
from mindustry.ctype import ContentType
from mindustry.game import Schematics
from mindustry.content import Blocks, Items, Liquids

from protocols import _Schematic
from sprites import Sprites

tilesize: int = 32
assets: str = "./assets/"


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

    sprites = Sprites.load(Fi(assets + "sprites/sprites.aatls"))

    
    schem: _Schematic = Schematics.read(Fi(args[1]))
    
    # print(f"{schem.name()=}")
    # print(f"{schem.description()=}")
    
    # print(f"{schem.powerProduction()=}")
    # print(f"{schem.powerConsumption()=}")
    
    # requirements = schem.requirements()
    
    # for stack in requirements:
    #     stack: _ItemStack
    #     print(stack.item.name, stack.amount)
    
    ts = time.time()
    
    image: Image.Image = Image.new("RGBA", (schem.width * tilesize, schem.height * tilesize))
    
    for tile in schem.tiles:
        block = tile.block
        
        rotate: float = tile.rotation * 90 if block.rotate else 0
        offset = block.sizeOffset
        draw_x = int((tile.x + offset) * tilesize)
        draw_y = int((schem.height - tile.y - block.size - offset) * tilesize)
        draw_size = block.size * tilesize
        
        image.paste(sprites.get_sprite(block.name).image().resize((draw_size, draw_size)).rotate(rotate), (draw_x, draw_y))
        
    
    print("Done in" , f"{round(time.time() - ts)}ms")
    
    image.show()
    
    return 0

if __name__ == "__main__":
    exit(main(*sys.argv))

