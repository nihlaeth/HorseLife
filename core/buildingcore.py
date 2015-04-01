from core import Core
from support.action import Action
from support.messages.quit import Quit
#from stablecore import StableCore


class BuildingCore(Core):
    def __init__(self, building):
        # No display class here, since this core class only relays
        # to a more specific building class
        self._building = building

    def run(self):
        while True:
            if self._building.building_type == "Stable":
                next_ = StableCore(self._building)
            else:
                # unimplemented building type
                next_ = None

            choice = next_.run()
            if isinstance(choice, Back) or isinstance(choice, Quit):
                return choice
            # Right now there isn't really any other option, but
            # for consistency's sake, this runs in a loop anyway.

    def __str__(self):
        return self._building.name
