
from typing import Dict
from typing import NewType
from typing import Set
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from copy import deepcopy

from pyorthogonalrouting.Common import INT_MAX
from pyorthogonalrouting.Functions import distance

from pyorthogonalrouting.Point import Point
from pyorthogonalrouting.PointNode import NO_POINT_NODE
from pyorthogonalrouting.PointNode import PointNode
from pyorthogonalrouting.PointNode import PointNodes

from pyorthogonalrouting.enumerations.Direction import Direction

XStr = NewType('XStr', str)
YStr = NewType('YStr', str)

YToPointNodeDict = NewType('YToPointNodeDict', Dict[YStr, PointNode])
XToYDict         = NewType('XToYDict',         Dict[XStr, YToPointNodeDict])

PointNodeSet     = Set[PointNode]


class PointNotFoundException(Exception):
    pass


class PointGraph:
    """
    Represents a Graph of Point nodes
    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._index: XToYDict = XToYDict({})

    def add(self, p: Point):

        xs, ys = self._pointToString(p=p)

        if xs not in self._index.keys():
            self._index[xs] = YToPointNodeDict({})

        yToPointNodeDict: YToPointNodeDict = self._index[xs]
        if ys not in yToPointNodeDict.keys():
            yToPointNodeDict[ys] = PointNode(data=p)

        self.logger.debug(f'Add of {p=} complete {self._index=}')

    def has(self, p: Point) -> bool:

        xs, ys = self._pointToString(p=p)

        return xs in self._index and ys in self._index[xs]

    def connect(self, a: Point, b: Point):
        """

        Args:
            a:
            b:
        """
        nodeA: PointNode = self.get(p=a)
        nodeB: PointNode = self.get(p=b)
        if nodeA == NO_POINT_NODE:
            raise PointNotFoundException(f'No Point a: {a=}')
        if nodeB == NO_POINT_NODE:
            raise PointNotFoundException(f'No Point b: {b=}')

        nodeA.adjacentNodes[nodeB] = distance(a=a, b=b)

    def get(self, p: Point) -> PointNode:
        """
        Retrieve the PointNode associated with the Point

        Args:
            p:

        Returns:  May return None
        """
        xs, ys = self._pointToString(p=p)
        if self.has(p) is True:
            return self._index[xs][ys]

        return NO_POINT_NODE

    def calculateShortestPathFromSource(self, graph: 'PointGraph', source: PointNode) -> 'PointGraph':

        source.distance = 0
        settledNodes:   PointNodeSet = set()
        unSettledNodes: PointNodeSet = set()

        unSettledNodes.add(source)
        while len(unSettledNodes) != 0:
            currentNode: PointNode = self._getLowestDistanceNode(unSettledNodes)
            unSettledNodes.remove(currentNode)

            for adjacentNode, edgeWeight in currentNode.adjacentNodes.items():
                if adjacentNode not in settledNodes:
                    self._calculateMinimumDistance(evaluationNode=adjacentNode, edgeWeight=edgeWeight, sourceNode=currentNode)
                    unSettledNodes.add(adjacentNode)
            settledNodes.add(currentNode)

        return graph

    def _inferPathDirection(self, node: PointNode) -> Direction:
        if len(node.shortestPath) == 0:
            return Direction.UNKNOWN

        return self._directionOfNodes(a=node.shortestPath[len(node.shortestPath) - 1], b=node)

    def _directionOfNodes(self, a: PointNode, b: PointNode) -> Direction:
        return self._directionOf(a=a.data, b=b.data)

    def _directionOf(self, a: Point, b: Point) -> Direction:
        """
        In the original JS version this method return None
        Args:
            a:
            b:

        Returns: Vertical or Horizontal;  May return unknown

        """
        if a.x == b.x:
            return Direction.HORIZONTAL
        elif a.y == b.y:
            return Direction.VERTICAL
        else:
            return Direction.UNKNOWN

    def _getLowestDistanceNode(self, unSettledNodes: PointNodeSet) -> PointNode:

        lowestDistanceNode: PointNode = PointNode()
        lowestDistance:     int       = INT_MAX
        for n in unSettledNodes:
            node:         PointNode = cast(PointNode, n)
            nodeDistance: int       = node.distance
            if nodeDistance < lowestDistance:
                lowestDistance     = nodeDistance
                lowestDistanceNode = node

        return lowestDistanceNode

    def _calculateMinimumDistance(self, evaluationNode: PointNode, edgeWeight: int, sourceNode: PointNode):

        sourceDistance:    int       = sourceNode.distance
        comingDirection:   Direction = self._inferPathDirection(sourceNode)
        goingDirection:    Direction = self._directionOfNodes(sourceNode, evaluationNode)
        #
        # Rewrite the following in a simpler to understand mechanism
        # const changingDirection = comingDirection && goingDirection && comingDirection != goingDirection;
        # extraWeigh = changingDirection ? Math.pow(edgeWeigh + 1, 2) : 0;
        if comingDirection == Direction.UNKNOWN or goingDirection == Direction.UNKNOWN:
            changingDirection: bool = False
        else:
            if comingDirection == goingDirection:
                changingDirection = False
            else:
                changingDirection = True
        if changingDirection is True:
            extraWeight: int = pow(edgeWeight + 1, 2)
        else:
            extraWeight = 0

        if sourceDistance + edgeWeight + extraWeight < evaluationNode.distance:

            evaluationNode.distance  = sourceDistance + edgeWeight + extraWeight
            # shortestPath: PointNode[] = [...sourceNode.shortestPath]
            shortestPath: PointNodes = deepcopy(sourceNode.shortestPath)
            shortestPath.append(sourceNode)
            evaluationNode.shortestPath = shortestPath

    def _pointToString(self, p: Point) -> Tuple[XStr, YStr]:

        xs: XStr = XStr(str(p.x))
        ys: YStr = YStr(str(p.y))

        return xs, ys
