
from enum import Enum


class OrthoMessageType(Enum):
    SHOW_RULERS           = 'ShowRulers'
    SHOW_MAIN_GRID        = 'ShowMainGrid'
    SHOW_REFERENCE_POINTS = 'ShowReferencePoints'
    SHOW_ROUTE_GRID       = 'ShowRouteGrid'

    CONNECTION_SIDE_CHANGED     = 'ConnectionSideChanged'
    CONNECTION_POSITION_CHANGED = 'ConnectionPositionChanged'
    SHAPED_MOVED                = 'ShapedMoved'

    REFRESH_FRAME           = 'RefreshFrame'

    NOT_SET = 'Not Set'
