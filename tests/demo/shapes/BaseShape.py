
from typing import List
from typing import NewType

from abc import ABCMeta
from abc import abstractmethod

from tests.demo.shapes.ShapeEventHandler import ShapeEventHandler


class MyMetaShapeEventHandler(ABCMeta, type(ShapeEventHandler)):        # type: ignore
    """
    I have no idea why this works:
    https://stackoverflow.com/questions/66591752/metaclass-conflict-when-trying-to-create-a-python-abstract-class-that-also-subcl
    """
    pass


class BaseShape(ShapeEventHandler, metaclass=MyMetaShapeEventHandler):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def inside(self, x, y) -> bool:
        pass


BaseShapes = NewType('BaseShapes', List[BaseShape])