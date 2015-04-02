from core import Core
from support.messages.quit import Quit
from support.messages.back import Back
from errors.unknownbuildingtype import UnknownBuildingType
from stablecore import StableCore
from models.stable import Stable


class BuildingCore(Core):
    def __init__(self, building):
        # No display class here, since this core class only relays
        # to a more specific building class
        self._building = building

    def run(self):
        while True:
            if isinstance(self._building, Stable):
                next_ = StableCore(self._building)
            else:
                raise UnknownBuildingType(self._building.building_type)

            result = next_.run()
            if isinstance(result, Back) or isinstance(result, Quit):
                return result
            # Right now there isn't really any other option, but
            # for consistency's sake, this runs in a loop anyway.

    def __str__(self):
        return str(self._building)
