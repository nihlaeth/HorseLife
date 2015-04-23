from sqlalchemy import create_engine

import backend.session as s
from core.loadcore import LoadCore
from core.maincore import MainCore
from support.messages.newgame import NewGame
from support.messages.savedgame import SavedGame
from support.messages.quit import Quit
from support.messages.timestamp import TimeStamp
from models.base import Base
from models.stable import Stable
from models.stableitem import StableItem
from models.horse import Horse
from models.setting import Setting
from generators.stablegenerator import StableGenerator
from generators.horsegenerator import HorseGenerator
from generators.settinggenerator import SettingGenerator
from backend.stablebackend import StableBackend
from backend.horsebackend import HorseBackend
from backend.time import time


class HorseLife():
    def __init__(self):
        # figure out which interface to use - for now there's only cli
        # later on, the default will be ncurses or opengl. This can
        # be overwritten with a command-line argument
        # self.gui = "cli"
        # if(self.gui == "cli"):
        #    from interface.cli.main import Main
        # elif(self.gui == "ncurses"):
        #    from interface.ncurses.main import Maine
        # elif(self.gui == "opengl"):
        #    from interface.opengl.main import Main
        # else:
        #    self.error("Invalid interface, available modules are "
        #    "'cli', 'ncurses' and 'opengl'")
        #    self.quit()

        # now get some user input about which db to load
        l = LoadCore()
        choice = l.run()

        if isinstance(choice, NewGame):
            self.loadGame(choice.file_name, True)
        elif isinstance(choice, SavedGame):
            self.loadGame(choice.file_name)
        elif isinstance(choice, Quit):
            self.quit()

    def loadGame(self, database, new=False):
        # load database
        # when we're done testing, put in a permanent database,
        # and allow the user to pick
        # a db (savegame)
        self.engine = create_engine('sqlite:///:memory:', echo=False)
        s.Session.configure(bind=self.engine)

        Base.metadata.create_all(self.engine)

        if new:
            with s.SessionScope() as session:
                stables = StableGenerator().gen_many(session, 1, "Shed")
                horses = HorseGenerator().gen_many(session, 1, "Mixed breed")
                stables[0].horses = [horses[0]]
                # Generate events for these objects
                StableBackend(1).get_events(session, TimeStamp(0, 0))
                HorseBackend(1).get_events(session, TimeStamp(0, 0))
                SettingGenerator.gen_many(
                        session,
                        {
                            "Date": [0, ""],
                            "Time": [0, ""]})
                time.pass_time(session, TimeStamp(0, 420))

        m = MainCore()
        choice = m.run()

        if isinstance(choice, Quit):
            self.quit()

    def error(self, text):
        """Error handling - print them, write them to a log, whatever!"""
        print "Error: " + text
        self.quit()

    def quit(self):
        pass


game = HorseLife()
