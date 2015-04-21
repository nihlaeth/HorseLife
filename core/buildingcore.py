from core import Core
from support.messages.quit import Quit
from support.messages.back import Back
from errors.unknownbuildingtype import UnknownBuildingType
from stablecore import StableCore
from backend.stablebackend import StableBackend


class BuildingCore(Core):
    """ This class just takes some of the processing away from MainCore.
    It determines building type and then refers to the correct core class."""
    def __init__(self, building):
        # No display class here, since this core class only relays
        # to a more specific building class
        self._building = building

    def run(self):
        while True:
            if isinstance(self._building, StableBackend):
                next_ = StableCore(self._building)
            else:
                raise UnknownBuildingType(self._building)

            result = next_.run()
            if isinstance(result, Back) or isinstance(result, Quit):
                return result
            # Right now there isn't really any other option, but
            # for consistency's sake, this runs in a loop anyway.

    def __str__(self):
        return str(self._building)
