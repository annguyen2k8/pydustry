from __future__ import annotations

from typing import Dict, List, Optional

from PIL import Image

from protocols import _Fi, _Reads
from utils import memoize


class Sprites:
    sprites: Dict[str, Sprite]
    packfile: _Fi
    imagedir: _Fi
    
    def __init__(self, packfile: _Fi, imagedir: _Fi) -> None:
        self.sprites = {}
        
        self.packfile = packfile
        self.imagedir = imagedir
        
        try:
            read: _Reads = packfile.reads()

            for b in b"AATLS":
                if read.b() != b:
                    raise Exception("Invalid binary header. Have you re-packed sprites?")
            
            # discard version
            read.b()
            
            while read.checkEOF() != -1:
                image: str = str(read.str())
                file: _Fi = imagedir.child(image)
                
                read.s()
                read.s()
                
                for i in range(4):
                    read.b()
                
                
                for i in range(read.i()):
                    sprite = Sprites.Sprite()
                    
                    sprite.imagefile = file
                    
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

                    self.sprites[sprite.name] = sprite
        except Exception:
            raise Exception(f"Error reading pack file: {packfile.path()}")

    
    @staticmethod
    def load(packfile: _Fi) -> Sprites:
        return Sprites(packfile, packfile.parent())

    def find(self, name: str, fallback: Optional[str] = None) -> Sprite:
        try:
            return self.sprites[name]
        except KeyError:
            print("Missing sprite name:", name)
        
        return self.find(fallback) if fallback else self.sprites["error"]

    class Sprite:
        imagefile: _Fi
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
        def image(self): 
            return Image.open(str(self.imagefile.path())).crop((self.left, self.top, self.left + self.width, self.top + self.height))