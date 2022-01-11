from typing import Type

from .shape import *
from .storage import *

from .ellipse import *
from .rectangle import *
from .triangle import *


available_shapes: list[Type[Shape]] = [
    Ellipse,
    Rectangle,
    Triangle,
]
