
from typing import cast

from codeallybasic.ConfigurationProperties import ConfigurationNameValue
from codeallybasic.ConfigurationProperties import ConfigurationProperties
from codeallybasic.ConfigurationProperties import PropertyName
from codeallybasic.ConfigurationProperties import Section
from codeallybasic.ConfigurationProperties import SectionName
from codeallybasic.ConfigurationProperties import Sections
from codeallybasic.ConfigurationProperties import configurationGetter
from codeallybasic.ConfigurationProperties import configurationSetter

from codeallybasic.SingletonV3 import SingletonV3

from pyorthogonalrouting.Rect import Rect

DEFAULT_SHAPE_MARGIN:              str  = '20'
DEFAULT_GLOBAL_BOUNDS_MARGIN:      str  = '50'
DEFAULT_SOURCE_EDGE_DISTANCE:      str  = '0.5'
DEFAULT_DESTINATION_EDGE_DISTANCE: str  = '0.5'
DEFAULT_GLOBAL_BOUNDS:             Rect = Rect(left=0, top=0, width=500, height=500)

SECTION_MAIN: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('shapeMargin'),             defaultValue=DEFAULT_SHAPE_MARGIN),
        ConfigurationNameValue(name=PropertyName('globalBoundsMargin'),      defaultValue=DEFAULT_GLOBAL_BOUNDS_MARGIN),
        ConfigurationNameValue(name=PropertyName('globalBounds'),            defaultValue=DEFAULT_GLOBAL_BOUNDS.__str__()),
        ConfigurationNameValue(name=PropertyName('sourceEdgeDistance'),      defaultValue=DEFAULT_SOURCE_EDGE_DISTANCE),
        ConfigurationNameValue(name=PropertyName('destinationEdgeDistance'), defaultValue=DEFAULT_DESTINATION_EDGE_DISTANCE),
    ]
)


MAIN_SECTION_NAME:    SectionName = SectionName('Main')

PY_ORTHOGONAL_ROUTING_SECTIONS: Sections = Sections(
    {
        MAIN_SECTION_NAME: SECTION_MAIN,
    }
)


class Configuration(ConfigurationProperties, metaclass=SingletonV3):
    def __init__(self):
        super().__init__(baseFileName='pyorthogonalrouting.ini', moduleName='pyorthogonalrouting', sections=PY_ORTHOGONAL_ROUTING_SECTIONS)

        self._configParser.optionxform = self._toStr    # type: ignore
        self._loadConfiguration()

    def _toStr(self, optionString: str) -> str:
        """
        Override base method

        Args:
            optionString:

        Returns: The option string unchanged
        """
        return optionString

    @property
    @configurationGetter(sectionName=MAIN_SECTION_NAME, deserializeFunction=int)
    def shapeMargin(self) -> int:
        return 0

    @shapeMargin.setter
    @configurationSetter(sectionName=MAIN_SECTION_NAME)
    def shapeMargin(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=MAIN_SECTION_NAME, deserializeFunction=int)
    def globalBoundsMargin(self) -> int:
        return 0

    @globalBoundsMargin.setter
    @configurationSetter(sectionName=MAIN_SECTION_NAME)
    def globalBoundsMargin(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=MAIN_SECTION_NAME, deserializeFunction=Rect.deSerialize)
    def globalBounds(self) -> Rect:
        return cast(Rect, None)

    @globalBounds.setter
    @configurationSetter(sectionName=MAIN_SECTION_NAME)
    def globalBounds(self, newValue: Rect):
        pass

    @property
    @configurationGetter(sectionName=MAIN_SECTION_NAME, deserializeFunction=float)
    def sourceEdgeDistance(self) -> float:
        return 0.0

    @sourceEdgeDistance.setter
    @configurationSetter(sectionName=MAIN_SECTION_NAME)
    def sourceEdgeDistance(self, newValue: float):
        pass

    @property
    @configurationGetter(sectionName=MAIN_SECTION_NAME, deserializeFunction=float)
    def destinationEdgeDistance(self) -> float:
        return 0.0

    @destinationEdgeDistance.setter
    @configurationSetter(sectionName=MAIN_SECTION_NAME)
    def destinationEdgeDistance(self, newValue: float):
        pass
