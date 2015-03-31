from sqlalchemy import create_engine

import backend.session as s


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

    def loadGame(self, database, new=False):
        # load database
        # when we're done testing, put in a permanent database,
        # and allow the user to pick
        # a db (savegame)
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        s.Session.configure(bind=engine)

        Base.metadata.create_all(self.engine)

    def error(self, text):
        """Error handling - print them, write them to a log, whatever!"""
        print "Error: " + text
        self.quit()

    def quit(self):
        pass


game = HorseLife()
