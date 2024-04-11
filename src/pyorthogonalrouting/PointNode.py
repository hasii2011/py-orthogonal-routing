
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

    def __eq__(self, other) -> bool:
        """

        Args:
            other:

        Returns:  True if the defined PointNodes are 'functionally' equal
        """
        ans: bool = False

        if isinstance(other, PointNode) is False:
            pass
        else:
            if self.distance == other.distance and self.data == other.data:
                ans = True

        return ans

    def __hash__(self) -> int:
        return hash((self.distance, self.data.x, self.data.y))

    def __str__(self) -> str:
        return f'distance={self.distance} Point={self.data}'

    def __repr__(self) -> str:
        return self.__str__()


NO_POINT_NODE: PointNode = cast(PointNode, None)
