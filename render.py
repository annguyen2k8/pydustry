from __future__ import annotations

from typing import Dict, List, Optional, Type

from sprites import Sprites


class Renders:
    registered_renders: List[Type[BaseRender]] = []
    renders: Dict[str, BaseRender]
    
    
    def __init__(self):
        self.renders = {}
        for render_cls in self.registered_renders:
            self.renders[render_cls.target.__name__] = render_cls()
    
    @classmethod
    def register(cls, render_cls: Type[BaseRender]) -> None:
        print("Imported render:", render_cls.__name__)
        cls.registered_renders.append(render_cls)
    
    
    def get_render(self, target: object, default_cls: Optional[Type[BaseRender]]) -> Optional[BaseRender]:
        default_render: BaseRender = None
        if default_cls:
            default_render = default_cls()
        
        return self.renders.get(target.__class__.__name__.replace("$Anonymous", ""), default_render)
    
class BaseRender:
    target: Type
    sprites: Sprites
    
    def __init_subclass__(cls):
        Renders.register(cls)