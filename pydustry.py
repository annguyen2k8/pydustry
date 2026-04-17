from __future__ import annotations

import sys
import time
from functools import wraps
from typing import Any, Dict, List, Protocol
import traceback

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
from arc.util.io import Reads
from mindustry import Vars
from mindustry.core import ContentLoader, Version
from mindustry.ctype import ContentType
from mindustry.game import Schematics
from java.io import UTFDataFormatException


class _Block(Protocol):
    name: str
    size: int
    rotate: bool
    sizeOffset: int

class _Color(Protocol):
    r: float
    g: float
    b: float
    a: float


class _Item(Protocol):
    name: str
    color: _Color

class _ItemStack(Protocol):
    item: _Item
    amount: int = 0

class _Schematic(Protocol):
    tiles: List[_Stile]
    labels: List[str]
    tags: Dict[str, str]
    width: int
    height: int

    def powerProduction(self) -> float: ...
    def powerConsumption(self) -> float: ...
    def requirements(self) -> List[_ItemStack]: ...
    def name(self) -> str: ...
    def description(self) -> str: ...

    class _Stile(Protocol):
        block: _Block
        x: int
        y: int
        config: object
        rotation: bytes

class _Reads(Protocol):
    def checkEOF(self) -> int: ...
    def l(self) -> int: ...
    def i(self) -> int: ...
    def s(self) -> int: ...
    def b(self) -> bytes: ...
    def b(self, length: int) -> List[bytes]: ...    
    def b(self, array: List[bytes]) -> List[bytes]: ...
    def b(self, array: List[bytes], offset: int, length: int) -> List[bytes]: ...
    def ub(self) -> int: ...
    def bool(self) -> bool: ...
    def f(self) -> float: ...
    def str(self) -> str: ...
    ...

class _Fi(Protocol):
    def child(self, name: str) -> _Fi: ...
    def parent(self) -> _Fi: ...
    def reads(self) -> Reads: ...
    def path(self) -> str: ...
    def mkdirs(self) -> bool: ...
    

def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper

class Sprite:
    image: _Fi
    name: str
    offset_x: float
    offset_y: float
    original_width: int
    original_height: int
    rotate: bool
    left: int
    top: int
    width: int
    height: int
    splits: List[int]
    pads: List[int]
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())})"
    
    @memoize
    def load_image(self): 
        return Image.open(str(self.image.path())).crop((self.left, self.top, self.left + self.width, self.top + self.height))



tilesize: int = 32
assets: str = "./assets/"


def main(*args: Any) -> int:
    Version.enabled = False

    Vars.content = ContentLoader()
    Vars.content.createBaseContent()
    
    for ctype in ContentType.all:
        for content in Vars.content.getBy(ctype):
            try:
                content.init()
            except:
                pass


    pack_file: _Fi = Fi(assets + "sprites/sprites.aatls")
    image_dir: _Fi = pack_file.parent()
    sprites: Dict[str, Sprite] = {}
    
    try:
        try:
            read: _Reads = pack_file.reads()

            for b in b"AATLS":
                if read.b() != b:
                    raise Exception("Invalid binary header. Have you re-packed sprites?")
            
            # discard version
            read.b()
            
            while read.checkEOF() != -1:
                image: str = str(read.str())
                file: _Fi = image_dir.child(image)
                
                read.s()
                read.s()
                
                for i in range(4):
                    read.b()
                
                
                for i in range(read.i()):
                    sprite: Sprite = Sprite()
                    
                    sprite.image = file
                    
                    sprite.name = str(read.str())
                    sprite.left = read.s()
                    sprite.top = read.s()
                    sprite.width = read.s()
                    sprite.height = read.s()
                    
                    if read.bool():
                        sprite.offset_x = read.s()
                        sprite.offset_y = read.s()
                        sprite.original_width = read.s()
                        sprite.original_height = read.s()
                    
                    if read.bool():
                        sprite.splits = [read.s(), read.s(), read.s(), read.s()]
                    
                    if read.bool():
                        sprite.pads = [read.s(), read.s(), read.s(), read.s()]

                    sprites[sprite.name] = sprite

        except Exception:
            raise Exception("Error reading pack file: ", pack_file.path())
            
    
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
        
        image: Image.Image = Image.new("RGBA", (schem.width * 32, schem.height * 32))
        
        for tile in schem.tiles:
            
            block = tile.block
            
            if block.name not in sprites:
                print(f"Missing sprite for block: \"{block.name}\"")
            
            sprite = sprites.get(block.name, sprites["error"])
            
            rotate: float = tile.rotation * 90 if block.rotate else 0
            
            offset = block.sizeOffset
            draw_x = int((tile.x + offset) * tilesize)
            draw_y = int((schem.height - tile.y - block.size - offset) * tilesize)
            
            image.paste(sprite.load_image().rotate(rotate), (draw_x, draw_y))
        
        print("Done in" , f"{round(time.time() - ts)}ms")
        
        image.show()
        
    except Exception:
        traceback.print_exc(); return 1
    
    return 0

if __name__ == "__main__":
    exit(main(*sys.argv))

