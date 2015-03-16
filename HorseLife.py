from models.base import Base
from models.horse import Horse
from models.person import Person
from models.building import Building
from models.setting import Setting

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class HorseLife():
    def __init__(self):
        # figure out which interface to use - for now there's only cli
        # later on, the default will be ncurses or opengl. This can
        # be overwritten with a command-line argument
        self.gui = "cli"
        if(gui == "cli"):
            from interface.cli.main import Main
        elif(gui == "ncurses"):
            from interface.ncurses.main import Main
        elif(gui == "opengl"):
            from interface.opengl.main import Main
        else:
            self.error("Invalid interface, available modules are 'cli', 'ncurses' and 'opengl'")
            self.quit()
        
        # now display the game selection screen
        self.loadScreen(action)

    def loadGame(self, database, new=False):
        # load database
        # when we're done testing, put in a permanent database, and allow the user to pick
        # a db (savegame)
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        self.Session = sessionmaker(bind=self.engine)
        
        # later on, there might be multiple sessions if the game becomes multi-threaded
        self.session = self.Session()
        
        Base.metadata.create_all(self.engine)
        
        # if this is not a saved game, but a new one, create it
        if new: 
            newgame(self.session)
        # now create an action to load the main screen and pass it to loadScreen
        self.loadScreen(action)

    def loadScreen(self, action):
        pass

    def error(self, text):
        """Error handling - print them, write them to a log, whatever!"""
        print "Error: " + text
        self.quit()

    def quit(self):
        pass


game = HorseLife()
