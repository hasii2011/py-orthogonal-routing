from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase

from pyorthogonalrouting.ConnectorPoint import ConnectorPoint
from pyorthogonalrouting.OrthogonalConnector import OrthogonalConnector
from pyorthogonalrouting.OrthogonalConnectorOptions import OrthogonalConnectorOptions
from pyorthogonalrouting.Point import Points
from pyorthogonalrouting.Rect import Rect
from pyorthogonalrouting.enumerations.Side import Side


# import the class you want to test here
# from org.pyut.template import template


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

    def tearDown(self):
        super().tearDown()

    # def testBasic(self):
    #
    #     shapeA: Rect = Rect(left=50,  top=50,  width=100, height=100)
    #     shapeB: Rect = Rect(left=200, top=200, width=50,  height=100)
    #
    #     options: OrthogonalConnectorOptions = OrthogonalConnectorOptions()
    #
    #     options.pointA = ConnectorPoint(shape=shapeA, side=Side.BOTTOM, distance=0.5)
    #     options.pointB = ConnectorPoint(shape=shapeB, side=Side.RIGHT,  distance=0.5)
    #     options.shapeMargin        = 10
    #     options.globalBoundsMargin = 10
    #     options.globalBounds       = Rect(left=0, top=0, width=500, height=500)
    #
    #     path: Points = OrthogonalConnector.route(options=options)
    #
    #     self.logger.info(f'{path=}')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestOrthogonalConnector))

    return testSuite


if __name__ == '__main__':
    unitTestMain()