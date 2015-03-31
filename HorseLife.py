from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

import backend.session as s
from core.loadcore import LoadCore
from core.maincore import MainCore
from support.messages.newgame import NewGame
from support.messages.savedgame import SavedGame


class HorseLife():
    def __init__(self):
        # figure out which interface to use - for now there's only cli
        # later on, the default will be ncurses or opengl. This can
        # be overwritten with a command-line argument
        #self.gui = "cli"
        #if(self.gui == "cli"):
        #    from interface.cli.main import Main
        #elif(self.gui == "ncurses"):
        #    from interface.ncurses.main import Main
        #elif(self.gui == "opengl"):
        #    from interface.opengl.main import Main
        #else:
        #    self.error("Invalid interface, available modules are 'cli', 'ncurses' and 'opengl'")
        #    self.quit()

        # now get some user input about which db to load
        l = LoadCore()
        choice = l.run()

        if isinstance(choice.cls, NewGame):
            self.loadGame(choice.cls.file_name, True)
        elif isinstance(choice.cls, SavedGame):
            self.loadGame(choics.cls.file_name)
        elif isinstance(choice.cls, Quit):
            self.quit()

    def loadGame(self, database, new=False):
        # load database
        # when we're done testing, put in a permanent database,
        # and allow the user to pick
        # a db (savegame)
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        s.Session.configure(bind=self.engine)

        Base = declarative_base()
        Base.metadata.create_all(self.engine)

        m = MainCore()
        choice = m.run()

        if isinstance(choice.cls, Quit):
            self.quit()

    def error(self, text):
        """Error handling - print them, write them to a log, whatever!"""
        print "Error: " + text
        self.quit()

    def quit(self):
        pass


game = HorseLife()
