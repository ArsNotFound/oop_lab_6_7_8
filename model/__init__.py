from typing import Type

from .ellipse import *
from .rectangle import *
from .shape import *
from .storage import *
from .triangle import *

available_shapes: list[Type[Shape]] = [
    Ellipse,
    Rectangle,
    Triangle,
]
