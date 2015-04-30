"""Provides a loading mechanism for the game and creates an instance."""
from sqlalchemy import create_engine

import backend.session as s
from core.loadcore import LoadCore
from core.maincore import MainCore
from support.messages.newgame import NewGame
from support.messages.savedgame import SavedGame
from support.messages.quit import Quit
from support.messages.timestamp import TimeStamp
from models.base import BASE
# The imports below appear unused, but are necessary to create the
# models in the database, so we have pylint ignore them.
# pylint: disable=unused-import
from models.stable import Stable
from models.stableitem import StableItem
from models.horse import Horse
from models.setting import Setting
from models.person import Person
from models.story import Story
from generators.stablegenerator import StableGenerator
from generators.horsegenerator import HorseGenerator
from generators.settinggenerator import SettingGenerator
from generators.storygenerator import StoryGenerator
from backend.stablebackend import StableBackend
from backend.horsebackend import HorseBackend
from backend.time import Time


class HorseLife(object):

    """Loading mechanism for the game."""

    def __init__(self):
        """Start the load screen to determine which database to use.

        Also load an interface (unimplemented to date).
        """
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
        choice = LoadCore().run()

        if isinstance(choice, NewGame):
            self.load_game(choice.file_name, True)
        elif isinstance(choice, SavedGame):
            self.load_game(choice.file_name)
        elif isinstance(choice, Quit):
            self.quit()

    def load_game(self, database, new=False):
        """Load and populate database, then load Main screen."""
        if database != ":memory:":
            database = "".join(["saves/", database])
        self.engine = create_engine('sqlite:///%s' % database, echo=False)
        s.SESSION.configure(bind=self.engine)

        BASE.metadata.create_all(self.engine)

        if new:
            with s.SessionScope() as session:
                stables = StableGenerator().gen_many(session, 1, "Shed")
                horses = HorseGenerator().gen_many(session, 1, "Mixed breed")
                stables[0].horses = [horses[0]]
                # Generate events for these objects
                StableBackend(1).get_events(session, TimeStamp(0, 0))
                HorseBackend(1).get_events(session, TimeStamp(0, 0))
                StoryGenerator().gen_many(session)
                SettingGenerator.gen_many(
                    session,
                    {
                        "Date": [0, ""],
                        "Time": [0, ""]})
                Time(session).pass_time(session, TimeStamp(0, 420))

        choice = MainCore().run()

        if isinstance(choice, Quit):
            self.quit()

    def error(self, text):
        """Error handling - print them, write them to a log, whatever."""
        print "Error: " + text
        self.quit()

    def quit(self):
        """Do some cleanup before exiting."""
        pass

if __name__ == "__main__":
    HorseLife()
