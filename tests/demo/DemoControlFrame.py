
from typing import cast

from logging import Logger
from logging import getLogger

from wx import CheckBox
from wx import CommandEvent
from wx import EVT_CHECKBOX
from wx import FONTFAMILY_SWISS
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_BOLD
from wx import Font

from wx import SP_ARROW_KEYS
from wx import SP_WRAP
from wx import SpinCtrlDouble
from wx import StaticText
from wx import Window

from wx.lib.sized_controls import SizedPanel

from tests.demo.DemoEvents import DemoEventType
from tests.demo.IEventEngine import IEventEngine


class DemoControlFrame(SizedPanel):

    def __init__(self, parent: Window):
        super().__init__(parent)

        self.logger: Logger = getLogger(__name__)

        self.SetSizerType('vertical')
        # noinspection PyUnresolvedReferences
        self.SetSizerProps(expand=True)

        self._showRulers:          CheckBox = cast(CheckBox, None)
        self._showMainGrid:        CheckBox = cast(CheckBox, None)
        self._showReferencePoints: CheckBox = cast(CheckBox, None)
        self._showRouteGrid:       CheckBox = cast(CheckBox, None)

        self._shapeAConnectionPosition: SpinCtrlDouble = cast(SpinCtrlDouble, None)
        self._shapeBConnectionPosition: SpinCtrlDouble = cast(SpinCtrlDouble, None)

        self._eventEngine: IEventEngine = cast(IEventEngine, None)

        self._layoutControls(self)
        self._setControlValues()
        self._bindCallbacks(parent=self)

    @property
    def eventEngine(self):
        return

    @eventEngine.setter
    def eventEngine(self, eventEngine: IEventEngine):
        assert self._eventEngine is None, 'You should only set the event engine once'
        self._eventEngine = eventEngine

    def _layoutControls(self, verticalPanel: SizedPanel):
        self._layoutAlgorithmLayers(verticalPanel)
        self._layoutAdjustments(verticalPanel)

    def _layoutAlgorithmLayers(self, sizedPanel: SizedPanel):

        container: SizedPanel = SizedPanel(sizedPanel)
        container.SetSizerType('vertical')
        # (["top", "left", "right"], 6))
        container.SetSizerProps(expand=True, proprtion=1, border=(["top"], 24))

        font: Font = Font(18, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_BOLD)
        title: StaticText = StaticText(container, label='Algorithm Layers')
        title.SetFont(font)

        self._showRulers          = CheckBox(container, label='Rulers')
        self._showMainGrid        = CheckBox(container, label='Main Grid')
        self._showReferencePoints = CheckBox(container, label='Reference Points')
        self._showRouteGrid       = CheckBox(container, label='Route Grid')

    def _layoutAdjustments(self, sizedPanel: SizedPanel):
        container: SizedPanel = SizedPanel(sizedPanel)
        container.SetSizerType('vertical')
        # (["top", "left", "right"], 6))
        container.SetSizerProps(expand=True, proprtion=1, border=(["top"], 24))

        font: Font = Font(18, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_BOLD)
        title: StaticText = StaticText(container, label='Adjustments')
        title.SetFont(font)

        StaticText(container, label='Shape A Connector Position')

        self._shapeAConnectionPosition = SpinCtrlDouble(container,
                                                        initial=0.5, min=0.0, max=1.0,
                                                        size=(200, -1),
                                                        style=SP_ARROW_KEYS | SP_WRAP
                                                        )
        self._shapeAConnectionPosition.SetIncrement(0.1)

        StaticText(container, label='Shape B Connector Position')
        self._shapeBConnectionPosition = SpinCtrlDouble(container,
                                                        initial=0.5, min=0.0, max=1.0,
                                                        size=(200, -1),
                                                        style=SP_ARROW_KEYS | SP_WRAP
                                                        )
        self._shapeBConnectionPosition.SetIncrement(0.1)

    def _setControlValues(self):
        """
        """
        pass

    def _bindCallbacks(self, parent):

        parent.Bind(EVT_CHECKBOX, self._onShowRulers,          self._showRulers)
        parent.Bind(EVT_CHECKBOX, self._onShowMainGrid,        self._showMainGrid)
        parent.Bind(EVT_CHECKBOX, self._onShowReferencePoints, self._showReferencePoints)
        parent.Bind(EVT_CHECKBOX, self._onShowRouteGrid,       self._showRouteGrid)

    def _onShowRulers(self, event: CommandEvent):

        newValue: bool = event.IsChecked()
        self.logger.debug(f'showRulers - {newValue=}')
        self._eventEngine.sendEvent(DemoEventType.SHOW_RULERS, showRulers=newValue)

    def _onShowMainGrid(self, event: CommandEvent):

        newValue: bool = event.IsChecked()
        self.logger.debug(f'showMainGrid - {newValue=}')

    def _onShowReferencePoints(self, event: CommandEvent):

        newValue: bool = event.IsChecked()
        self.logger.debug(f'showReferencePoints - {newValue=}')

        self._eventEngine.sendEvent(DemoEventType.SHOW_REFERENCE_POINTS, showReferencePoints=newValue)

    def _onShowRouteGrid(self, event: CommandEvent):

        newValue: bool = event.IsChecked()
        self.logger.debug(f'showRouteGrid - {newValue=}')
        self._eventEngine.sendEvent(DemoEventType.SHOW_ROUTE_GRID, showRouteGrid=newValue)
