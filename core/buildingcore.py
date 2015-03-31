from core import Core
from support.action import Action
from support.messages.quit import Quit
#from stablecore import StableCore

class BuildingCore(Core):
    def __init__(self):
        # No display class here, since this core class only relays
        # to a more specific building class
        pass

    def run(self, building):
        if building.building_type == "Stable" :
            next_ = StableCore()
        else:
            # unimplemented building type
            next_ = None

        choice = next_.run()

        # TODO figure out what to do with the input

        return choice

    def __str__(self):
        return "problem - building hasn't been passed in init"
