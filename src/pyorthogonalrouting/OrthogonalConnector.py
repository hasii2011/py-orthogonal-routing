
from logging import Logger
from logging import getLogger

from pyorthogonalrouting.Common import Integers
from pyorthogonalrouting.Common import integerListFactory

from pyorthogonalrouting.Functions import computePt
from pyorthogonalrouting.Functions import isVerticalSide
from pyorthogonalrouting.Functions import makePt

from pyorthogonalrouting.ConnectorPoint import ConnectorPoint

from pyorthogonalrouting.OrthogonalConnectorOptions import OrthogonalConnectorOptions

from pyorthogonalrouting.Grid import Grid
from pyorthogonalrouting.Point import Point
from pyorthogonalrouting.Point import Points
from pyorthogonalrouting.Point import pointsFactory

from pyorthogonalrouting.Rectangle import Rectangle
from pyorthogonalrouting.Rectangle import Rectangles
from pyorthogonalrouting.enumerations.Side import Side


class OrthogonalConnector:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    @classmethod
    def route(cls, options: OrthogonalConnectorOptions) -> Points:

        pointA:             ConnectorPoint = options.pointA
        pointB:             ConnectorPoint = options.pointB
        globalBoundsMargin: int            = options.globalBoundsMargin

        spots:       Points   = pointsFactory()
        verticals:   Integers = integerListFactory()
        horizontals: Integers = integerListFactory()

        sideA: Side = pointA.side
        sideB: Side = pointB.side

        sideAVertical: bool = isVerticalSide(sideA)
        sideBVertical: bool = isVerticalSide(sideB)

        originA: Point = computePt(pointA)
        originB: Point = computePt(pointB)

        shapeA:    Rectangle = Rectangle.fromRect(r=pointA.shape)
        shapeB:    Rectangle = Rectangle.fromRect(r=pointB.shape)
        bigBounds: Rectangle = Rectangle.fromRect(r=options.globalBounds)

        shapeMargin: int = options.shapeMargin

        inflatedA: Rectangle = shapeA.inflate(horizontal=shapeMargin, vertical=shapeMargin)
        inflatedB: Rectangle = shapeB.inflate(horizontal=shapeMargin, vertical=shapeMargin)

        # Check bounding boxes collision

        if inflatedA.intersects(rectangle=inflatedB):
            shapeMargin = 0
            inflatedA = shapeA
            inflatedB = shapeB

        inflatedBounds = inflatedA.union(inflatedB).inflate(globalBoundsMargin, globalBoundsMargin)

        # Curated bounds to stick to
        bounds: Rectangle = Rectangle.fromLTRB(
            left=max(inflatedBounds.left, bigBounds.left),
            top=max(inflatedBounds.top, bigBounds.top),
            right=max(inflatedBounds.right, bigBounds.right),
            bottom=max(inflatedBounds.bottom, bigBounds.bottom)
        )

        # Add edges to rulers
        for b in [inflatedA, inflatedB]:
            verticals.append(b.left)
            verticals.append(b.right)
            horizontals.append(b.top)
            horizontals.append(b.bottom)

        # Rulers at origins of shapes
        # (sideAVertical ? verticals : horizontals).push(sideAVertical ? originA.x : originA.y);
        # (sideBVertical ? verticals : horizontals).push(sideBVertical ? originB.x : originB.y);
        # Typescript is too cute

        if sideAVertical is True:
            verticals.append(originA.x)
        else:
            horizontals.append(originA.y)
        if sideBVertical is True:
            verticals.append(originB.x)
        else:
            horizontals.append(originB.y)

        # const add = (dx: number, dy: number) => spots.push(makePt(p.x + dx, p.y + dy));
        def add(p: Point, dx: int, dy: int):
            spots.append(makePt(p.x + dx, p.y + dy))

        # Points of shape antennas
        for connectorPt in [pointA, pointB]:
            p: Point = computePt(p=connectorPt)
            match connectorPt.side:
                case Side.TOP:
                    add(p, dx=0, dy=-shapeMargin)
                case Side.RIGHT:
                    add(p, dx=shapeMargin, dy=0)
                case Side.BOTTOM:
                    add(p, dx=0, dy=shapeMargin)
                case Side.LEFT:
                    add(p, dx=-shapeMargin, dy=0)
                case _:
                    assert False, f'I do not understand that side {connectorPt.side=}'

        # Sort rulers
        verticals.sort()
        horizontals.sort()

        # Create grid
        grid:       Grid   = Grid.rulersToGrid(verticals=verticals, horizontals=horizontals, bounds=bounds)
        gridPoints: Points = Grid.gridToSpots(grid=grid, obstacles=Rectangles([inflatedA, inflatedB]))

