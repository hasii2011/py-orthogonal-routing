
from enum import Enum

from wx.lib.newevent import NewEvent

#
# The constructor returns a tuple; The first entry is the event,  The second is the binder
#
ShowRulersEvent,          EVT_SHOW_RULERS           = NewEvent()
ShowMainGridEvent,        EVT_SHOW_MAIN_GRID        = NewEvent()
ShowReferencePointsEvent, EVT_SHOW_REFERENCE_POINTS = NewEvent()
ShowRouteGridEvent,       EVT_SHOW_ROUTE_GRID       = NewEvent()

ConnectionSideChangedEvent,     EVT_CONNECTION_SIDE_CHANGED     = NewEvent()
ConnectionPositionChangedEvent, EVT_CONNECTION_POSITION_CHANGED = NewEvent()
ShapeMovedEvent,                EVT_SHAPE_MOVED                 = NewEvent()

RefreshFrameEvent,          EVT_REFRESH_FRAME           = NewEvent()


class DemoEventType(Enum):

    SHOW_RULERS           = 'ShowRulers'
    SHOW_MAIN_GRID        = 'ShowMainGrid'
    SHOW_REFERENCE_POINTS = 'ShowReferencePoints'
    SHOW_ROUTE_GRID       = 'ShowRouteGrid'

    CONNECTION_SIDE_CHANGED     = 'ConnectionSideChanged'
    CONNECTION_POSITION_CHANGED = 'ConnectionPositionChanged'
    SHAPED_MOVED                = 'ShapedMoved'

    REFRESH_FRAME           = 'RefreshFrame'

    NOT_SET = 'Not Set'
