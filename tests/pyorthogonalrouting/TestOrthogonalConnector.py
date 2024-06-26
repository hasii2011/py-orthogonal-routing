import json
from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.ResourceManager import ResourceManager
from codeallybasic.UnitTestBase import UnitTestBase

from pyorthogonalrouting.ConnectorPoint import ConnectorPoint
from pyorthogonalrouting.OrthogonalConnector import OrthogonalConnector
from pyorthogonalrouting.OrthogonalConnectorOptions import OrthogonalConnectorOptions
from pyorthogonalrouting.Point import Point

from pyorthogonalrouting.Point import Points
from pyorthogonalrouting.Rect import Rect
from pyorthogonalrouting.enumerations.Side import Side
from tests.ProjectTestBase import ProjectTestBase


class TestOrthogonalConnector(UnitTestBase):
    """
    Auto generated by the one and only:
        Gato Malo – Humberto A. Sanchez II
        Generated: 07 April 2024
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

        self._options: OrthogonalConnectorOptions = OrthogonalConnectorOptions()

        shapeA: Rect = Rect(left=50,  top=50,  width=100, height=100)
        shapeB: Rect = Rect(left=200, top=200, width=50,  height=100)

        self._options.pointA = ConnectorPoint(shape=shapeA, side=Side.BOTTOM, distance=0.5)
        self._options.pointB = ConnectorPoint(shape=shapeB, side=Side.RIGHT,  distance=0.5)
        self._options.shapeMargin        = 10
        self._options.globalBoundsMargin = 10
        self._options.globalBounds       = Rect(left=0, top=0, width=500, height=500)

    def tearDown(self):
        super().tearDown()

    def testBasic(self):

        path: Points = OrthogonalConnector.route(options=self._options)

        self.logger.debug(f'{path=}')

        self.assertEqual(5, len(path), 'Point path is not correct')

    def testReferencePoints(self):

        path: Points = OrthogonalConnector.route(options=self._options)
        self.logger.debug(f'{path=}')

        spots: Points = OrthogonalConnector.byProduct.spots
        self.logger.debug(f'{spots=}')
        goldenReferencePoints: Points = self._loadReferencePoints()

        self.assertEqual(len(goldenReferencePoints), len(spots), 'Should be identical ')
        for goldenPoint in goldenReferencePoints:
            self.assertIn(goldenPoint, spots, 'This point is not in')

    def _loadReferencePoints(self) -> Points:
        fqFileName: str = ResourceManager.retrieveResourcePath(bareFileName='referencePoints.json',
                                                               resourcePath=ProjectTestBase.RESOURCES_TEST_DIRECTORY,
                                                               packageName=ProjectTestBase.RESOURCES_TEST_PACKAGE_NAME)

        self.logger.debug(f'{fqFileName=}')
        with open(fqFileName, "r") as fp:
            jsonString: str = fp.read()

        referencePointList = json.loads(jsonString)
        self.logger.debug(f'{referencePointList=}')

        points: Points = Points([])
        for jsonPt in referencePointList:
            self.logger.debug(f'{jsonPt=}')
            x: int = int(jsonPt['x'])
            y: int = int(jsonPt['y'])
            point: Point = Point(x=x, y=y)

            points.append(point)

        return points


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestOrthogonalConnector))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
