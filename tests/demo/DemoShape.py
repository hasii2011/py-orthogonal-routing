
from logging import Logger
from logging import getLogger

from pyorthogonalrouting.Rectangle import Rectangle


class DemoShape(Rectangle):

    def __init__(self, left: int, top: int, width: int, height: int):

        super().__init__(left, top, width, height)

        self.logger: Logger = getLogger(__name__)
