from typing import Type

from model.shape import Shape
from .ellipse import Ellipse
from .rectangle import Rectangle
from .triangle import Triangle

available_shapes: list[Type[Shape]] = [
    Ellipse,
    Rectangle,
    Triangle,
]


def get_shapes_dict() -> dict[str, Type[Shape]]:
    d: dict[str, Type[Shape]] = {}
    for shape in available_shapes:
        d[shape.name()] = shape

    return d
