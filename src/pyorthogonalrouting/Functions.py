
from math import sqrt
from typing import Dict
from typing import cast

from pyorthogonalrouting.ConnectorPoint import ConnectorPoint
from pyorthogonalrouting.Point import Point
from pyorthogonalrouting.Point import Points
from pyorthogonalrouting.PointNode import Distance
from pyorthogonalrouting.Rectangle import Rectangle
from pyorthogonalrouting.Rectangle import Rectangles
from pyorthogonalrouting.enumerations.Side import Side


def distance(a: Point, b: Point) -> Distance:

    intDistance: int = round(sqrt(pow(b.x - a.x, 2) + pow(b.y - a.y, 2)))

    return Distance(intDistance)


def isVerticalSide(side: Side) -> bool:
    """

    Args:
        side:

    Returns: 'True' if the side belongs on the vertical axis, else it returns 'False'
    """
    return side == Side.TOP or side == Side.BOTTOM


def makePt(x: int, y: int) -> Point:
    """
    Utility Point creator

    Args:
        x:
        y:

    Returns:

    """
    return Point(x=x, y=y)


def computePt(p: ConnectorPoint) -> Point:
    """

    Args:
        p:  Gets the actual point of the connector based on the distance parameter

    Returns:

    """
    b: Rectangle = Rectangle.fromRect(p.shape)

    match p.side:
        case Side.BOTTOM:
            return makePt(b.left + b.width * p.distance, b.bottom)
        case Side.TOP:
            return makePt(b.left + b.width * p.distance, b.top)
        case Side.LEFT:
            return makePt(b.left, b.top + b.height * p.distance)
        case Side.RIGHT:
            return makePt(b.right, b.top + b.height * p.distance)
        case _:
            assert False, f'Unknown side {p.side}'


def reducePoints(points: Points) -> Points:
    """

    Args:
        points:

    Returns: Returns a list without repeated points
    """

    result: Points = Points(list(dict.fromkeys(points)))

    return result
