from __future__ import annotations

from typing import Dict, List, Protocol, overload


class _Block(Protocol):
    name: str
    size: int
    rotate: bool
    sizeOffset: int
    hasPower: bool

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
    def ub(self) -> int: ...
    def bool(self) -> bool: ...
    def f(self) -> float: ...
    def str(self) -> str: ...

class _Fi(Protocol):
    def child(self, name: str) -> _Fi: ...
    def parent(self) -> _Fi: ...
    def reads(self) -> _Reads: ...
    def path(self) -> str: ...
    def mkdirs(self) -> bool: ...


class _JPoint2(Protocol):
    x: int
    y: int
    
    def pack(self) -> int: ...