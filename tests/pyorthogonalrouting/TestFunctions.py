from collections import Counter
from typing import Any
from typing import List
from typing import Tuple

from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase

from pyorthogonalrouting.Common import Integers
from pyorthogonalrouting.Common import integerListFactory
from pyorthogonalrouting.ConnectorPoint import ConnectorPoint

from pyorthogonalrouting.Functions import distance
from pyorthogonalrouting.Functions import extrudeConnectorPoint
from pyorthogonalrouting.Functions import getBendDirection
from pyorthogonalrouting.Functions import isVerticalSide
from pyorthogonalrouting.Functions import reducePoints
from pyorthogonalrouting.Functions import simplifyPaths

from pyorthogonalrouting.Point import Point
from pyorthogonalrouting.Point import Points
from pyorthogonalrouting.PointNode import PointNode
from pyorthogonalrouting.Rect import Rect
from pyorthogonalrouting.enumerations.BendDirection import BendDirection

from pyorthogonalrouting.enumerations.Side import Side


class TestFunctions(UnitTestBase):
    """
    Auto generated by the one and only:
        Gato Malo – Humberto A. Sanchez II
        Generated: 01 April 2024
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testGetBendNorth(self):
        a: Point = Point(0, 100)
        b: Point = Point(55, 100)
        c: Point = Point(55, 0)

        bendDirection: BendDirection = getBendDirection(a, b, c)

        self.assertEqual(BendDirection.NORTH, bendDirection, '')

    def testGetBendSouth(self):
        a: Point = Point(0, 100)
        b: Point = Point(55, 100)
        c: Point = Point(55, 200)

        bendDirection: BendDirection = getBendDirection(a, b, c)

        self.assertEqual(BendDirection.SOUTH, bendDirection, '')

    def testGetBendEast(self):
        a: Point = Point(100, 100)
        b: Point = Point(100, 200)
        c: Point = Point(400, 200)

        bendDirection: BendDirection = getBendDirection(a=a, b=b, c=c)

        self.assertEqual(BendDirection.EAST, bendDirection, '')

    def testGetBendWest(self):
        a: Point = Point(100, 100)
        b: Point = Point(100, 200)
        c: Point = Point(50, 200)

        bendDirection: BendDirection = getBendDirection(a=a, b=b, c=c)

        self.assertEqual(BendDirection.WEST, bendDirection, '')

    def testSimplifyPaths(self):

        a:  Point = Point(100, 100)
        b:  Point = Point(200, 101)
        b1: Point = Point(200, 200)
        c:  Point = Point(400, 200)

        points: Points = Points([a, b, b1, c])

        simplePath: Points = simplifyPaths(points)

        self.logger.debug(f'{simplePath=}')

        self.assertNotIn(b, simplePath, 'Funky one should be eliminated')

    def testExtrudeConnectorPoint(self):

        rect: Rect           = Rect(left=100, top=200, width=100, height=100)
        cp:   ConnectorPoint = ConnectorPoint(shape=rect, side=Side.RIGHT, distance=5)

        expectedExtrudedPoint: Point = Point(x=205, y=700)
        extrudedPoint:         Point = extrudeConnectorPoint(cp=cp, margin=5)

        self.assertEqual(expectedExtrudedPoint, extrudedPoint, 'Antennas do not match')

        self.logger.debug(f'{extrudedPoint}')

    def testReducePoints(self):
        duplicatePoints: Points = Points(
            [
                Point(555, 555), Point(100, 100), Point(22, 22),
                Point(111, 111), Point(220, 220), Point(22, 22),
                Point(111, 111), Point(666, 666), Point(555, 555),
            ]
        )
        reducedPoints: Points = reducePoints(points=duplicatePoints)
        self.logger.debug(f'{reducedPoints=}')
        self.assertFalse(self._hasDuplicates(reducedPoints), 'Wowza, there should be no duplicates')

    def testDistance(self):

        ptA: Point = Point(x=477, y=260)
        ptB: Point = Point(x=477, y=360)

        howFar: int = distance(a=ptA, b=ptB)

        self.assertEqual(100, howFar, 'My computation is incorrect')

    def testIsVerticalSideTop(self):
        self.assertTrue(isVerticalSide(Side.TOP))

    def testIsVerticalSideBottom(self):
        self.assertTrue(isVerticalSide(Side.BOTTOM))

    def testIsVerticalSideRight(self):
        self.assertFalse(isVerticalSide(Side.RIGHT))

    def testIsVerticalSideLeft(self):
        self.assertFalse(isVerticalSide(Side.LEFT))

    def testSort(self):
        verticals: Integers = integerListFactory()
        verticals.append(500)
        verticals.append(77)
        verticals.append(23)
        verticals.append(100)
        verticals.append(5)

        self.logger.debug(f'Before {verticals=}')
        verticals.sort()
        self.logger.debug(f'after {verticals=}')

    def testTSEmulation(self):

        verticals, horizontals = self._runAppendComputation(sideAVertical=False, sideBVertical=False)
        self.assertTrue(len(verticals) == 0)
        self.assertIn(2, horizontals)
        self.assertIn(4, horizontals)

        verticals, horizontals = self._runAppendComputation(sideAVertical=True, sideBVertical=True)
        self.assertTrue(len(horizontals) == 0)
        self.assertIn(1, verticals)
        self.assertIn(3, verticals)

        verticals, horizontals = self._runAppendComputation(sideAVertical=True, sideBVertical=False)
        self.assertIn(1, verticals)
        self.assertIn(4, horizontals)

        verticals, horizontals = self._runAppendComputation(sideAVertical=False, sideBVertical=True)
        self.assertIn(3, verticals)
        self.assertIn(2, horizontals)

    def testTSForEmulation(self):
        integers: Integers = Integers([100, 200, 300])

        for i in range(len(integers)):
            self.logger.debug(f'integers[{i}]={integers[i]}')

    def testTSSets(self):
        pointNode1: PointNode = PointNode(distance=2052, data=Point(x=30, y=220))
        pointNode2: PointNode = PointNode(distance=1061, data=Point(x=30, y=190))

        bumSet = set()
        bumSet.add(pointNode1)
        bumSet.add(pointNode2)

        bumSet.remove(pointNode2)

        self.logger.debug(f'{bumSet}')

    def _runAppendComputation(self, sideAVertical: bool, sideBVertical: bool) -> Tuple[Integers, Integers]:

        verticals:   Integers = integerListFactory()
        horizontals: Integers = integerListFactory()

        originA: Point = Point(x=1, y=2)
        originB: Point = Point(x=3, y=4)

        if sideAVertical is True:
            verticals.append(originA.x)
        else:
            horizontals.append(originA.y)
        if sideBVertical is True:
            verticals.append(originB.x)
        else:
            horizontals.append(originB.y)

        self.logger.debug(f'{verticals=} {horizontals=}')

        return verticals, horizontals

    def _hasDuplicates(self, genericList: List[Any]) -> bool:
        """

        Args:
            genericList:

        Returns: `True` if the list has duplicates, else `False`
        """

        return any(value > 1 for value in Counter(genericList).values())


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestFunctions))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
