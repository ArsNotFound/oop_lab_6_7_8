from typing import Type

from model import Shape
from .ellipse import Ellipse
from .rectangle import Rectangle
from .triangle import Triangle

available_shapes: list[Type[Shape]] = [
    Ellipse,
    Rectangle,
    Triangle,
]
