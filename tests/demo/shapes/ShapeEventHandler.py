from typing import List
from typing import NewType

from wx import MouseEvent


class ShapeEventHandler:
    """
    This is a marker interface.  It lets a shape
    receive events
    """
    def __init__(self):
        pass

    def onLeftDown(self, event: MouseEvent):
        """
        Subclasses should override this method for their own behavior
        Args:
            event:
        """
        event.Skip()

    def onLeftUp(self, event: MouseEvent):
        """
        Subclasses should override this method for their own behavior
        Args:
            event:
        """
        event.Skip()


ShapeEventHandlers = NewType('ShapeEventHandlers', List[ShapeEventHandler])
