
from typing import List
from typing import NewType

from dataclasses import dataclass
from typing import cast

from pyorthogonalrouting.Common import NOT_SET_INT
from pyorthogonalrouting.Rect import NO_RECT
from pyorthogonalrouting.Rect import Rect
from pyorthogonalrouting.enumerations.Side import Side


@dataclass
class ConnectorPoint:
    """
    Represents a connection point on a routing request
    """
    shape:    Rect = NO_RECT
    side:     Side = Side.NOT_SET
    distance: int  = NOT_SET_INT


ConnectorPoints = NewType('ConnectorPoints', List[ConnectorPoint])

NO_CONNECTOR_POINT: ConnectorPoint = cast(ConnectorPoint, None)
