from anabel import interface
from typing import Sequence

@interface
class SimpleMaterial:
    E : float = None
    fy: float = None

    Hi: float = None
    Hk: float = None

    Hir: float = None
    Hkr: float = None

@interface
class SimpleMesh:
    yi: Sequence
    dA: Sequence
    Qm: Sequence

@interface
class SimpleShape:
    A : float = None #: Cross-sectional area, in.2 (mm2)
    Ix: float = None
    Zx: float = None

    I : float = None
    Z : float = None

    def __post_init__(self):
        if self.I is not None:
            self.Ix = self.I
        if self.Z is not None:
            self.Zx = self.Z

@interface
class SimpleSection( SimpleShape, SimpleMaterial):
    """A homogeneous shape with material properties"""
    pass