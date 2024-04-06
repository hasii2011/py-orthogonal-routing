
from typing import Dict
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from pyorthogonalrouting.Common import Integers
from pyorthogonalrouting.Point import Points

from pyorthogonalrouting.Rectangle import NO_RECTANGLE
from pyorthogonalrouting.Rectangle import Rectangle
from pyorthogonalrouting.Rectangle import Rectangles

RowNumber    = NewType('RowNumber',    int)
ColumnNumber = NewType('ColumnNumber', int)

RectangleMapRow = NewType('RectangleMapRow', Dict[ColumnNumber, Rectangle])
GridMap         = NewType('GridMap',         Dict[RowNumber, RectangleMapRow])

DEBUG_GRID: bool = False     # TODO:  Make this a runtime flag


class Grid:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._rows: int = 0
        self._cols: int = 0

        self._gridMap: GridMap = GridMap({})

    @classmethod
    def rulersToGrid(cls, verticals: Integers, horizontals: Integers, bounds: Rectangle) -> 'Grid':
        """
        Creates a grid of rectangles from the specified set of rulers, contained on the specified bounds

        Args:
            verticals:
            horizontals:
            bounds:
        Returns:  The newly created Grid
       """
        grid: Grid = Grid()

        verticals.sort()
        horizontals.sort()

        lastX:  int = bounds.left
        lastY:  int = bounds.top
        column: int = 0
        row:    int = 0

        for y in horizontals:
            for x in verticals:
                rectangle: Rectangle = Rectangle.fromLTRB(left=lastX, top=lastY, right=x, bottom=y)
                grid.set(row=RowNumber(row), column=ColumnNumber(column), rectangle=rectangle)
                column += 1
                lastX = x
            #
            # last cell of the row
            rectangle = Rectangle.fromLTRB(lastX, lastY, bounds.right, y)
            grid.set(row=RowNumber(row), column=ColumnNumber(column), rectangle=rectangle)

            lastX  = bounds.left
            lastY  = y
            column = 0
            row    += 1

        lastX = bounds.left

        # last row of cells
        for x in verticals:
            rectangle = Rectangle.fromLTRB(lastX, lastY, x, bounds.bottom)
            grid.set(row=RowNumber(row), column=ColumnNumber(column), rectangle=rectangle)
            column += 1
            lastX = x

        # Last cell of row
        rectangle = Rectangle.fromLTRB(lastX, lastY, bounds.right, bounds.bottom)
        grid.set(row=RowNumber(row), column=ColumnNumber(column), rectangle=rectangle)

        if DEBUG_GRID is True:
            Grid.debugGridMap(grid=grid)

        return grid

    @classmethod
    def gridToSpots(cls, grid: 'Grid', obstacles: Rectangles):

        # obstacleCollision = (p: Point) = > obstacles.filter(o= > o.contains(p)).length > 0;

        gridPoints: Points = Points([])

        for row, data in grid._gridMap.items():
            firstRow: int = row == 0
            lastRow:  int = row == grid.rows -1


    @property
    def rows(self) -> int:
        return self._rows

    @property
    def columns(self) -> int:
        return self._cols

    def rectangles(self) -> Rectangles:

        r: Rectangles = Rectangles([])

        for rr in self._gridMap.values():
            rectangleMapRow: RectangleMapRow = cast(RectangleMapRow, rr)
            for rrr in rectangleMapRow.values():
                rectangle: Rectangle = cast(Rectangle, rrr)
                r.append(rectangle)

        return r

    def set(self, row: RowNumber, column: ColumnNumber, rectangle: Rectangle):

        self._rows = max(self.rows,    row + 1)
        self._cols = max(self.columns, column + 1)

        if row in self._gridMap.keys():
            rectangleMapRow: RectangleMapRow = self._gridMap[row]
        else:
            rectangleMapRow = RectangleMapRow({})
            self._gridMap[row] = rectangleMapRow

        rectangleMapRow[column] = rectangle

    def get(self, row: RowNumber, column: ColumnNumber) -> Rectangle:

        if row in self._gridMap.keys():
            rectangleMapRow: RectangleMapRow = self._gridMap[row]
            if column in rectangleMapRow:
                return rectangleMapRow[column]
            else:
                return NO_RECTANGLE
        else:
            return NO_RECTANGLE

    @classmethod
    def debugGridMap(cls, grid: 'Grid'):

        gridMap: GridMap = grid._gridMap

        lc: str = '{'   # left curly
        rc: str = '}'   # right curly

        print(f'GridMap [{grid.rows}] {lc}')
        for x in gridMap.keys():
            rectangleMapRow: RectangleMapRow = gridMap[x]
            print(f'\t{x} => Map[{len(rectangleMapRow)}] {lc}')
            for y in rectangleMapRow.keys():
                rectangle: Rectangle = gridMap[x][y]
                print(f'\t\t{y} => {rectangle}')
            print(f'\t\t{rc},')

        print(f'{rc}')
