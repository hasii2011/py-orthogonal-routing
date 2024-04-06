
from typing import cast
from typing import Dict
from typing import List
from typing import NewType

from dataclasses import dataclass
from dataclasses import field

from pyorthogonalrouting.Common import INT_MAX
from pyorthogonalrouting.Point import NO_POINT
from pyorthogonalrouting.Point import Point

Distance = NewType('Distance', int)

PointNodes    = NewType('PointNodes',    List['PointNode'])
PointNodesMap = NewType('PointNodesMap', Dict['PointNode', Distance])


def pointNodesFactory() -> PointNodes:
    return PointNodes([])


def pointNodesMapFactory() -> PointNodesMap:
    return PointNodesMap({})


@dataclass
class PointNode:
    """
    Represents a node in a graph, whose data is a Point
    """
    distance:      int           = INT_MAX
    shortestPath:  PointNodes    = field(default_factory=pointNodesFactory)
    adjacentNodes: PointNodesMap = field(default_factory=pointNodesMapFactory)
    data:          Point         = NO_POINT

    def __hash__(self) -> int:
        return hash((self.distance, self.data.x, self.data.y))


NO_POINT_NODE: PointNode = cast(PointNode, None)
