class Display():
    def __init__(self):
        """ Initiate with only static data."""
        self._screen_width = 80
        self._separator = self._repeat('-', self._screen_width)
        self._title = "Main"

    def init(self, data):
        """ Initialize with (database) data.

        Arguments:
        data -- list of classes to be displayed
        """
        self._data = data
        self._i = 0

    def display(self):
        """ Display screen and return user choice (class)."""
        print self._format_title()

        for action in self.actions:
            print str(self.i)+") "+action
            self.i+=1
        
        choice = e.getInt(self.i)
        return actions[choice]

    def _repeat(self, string, n):
        """ Repeat string n times and return it."""
        return ''.join([string for i in range(n)])
    
    def _format_title(self):
        """ Format the page title and return it."""
        frame = repeat("=", self._screen_width)
        whitespace = len(frame) - 6 - len(self._title)
        leading_whitespace = whitespace / 2
        trailing_whitespace = whitespace / 2 if whitespace%2 == 0 else whitespace/2 + 1
        header = ''.join(["===", self._repeat(" ", leading_whitespace), self._title, self._repeat(" ", trailing_whitespace), "==="])
        return ''.join([frame, "\n", header, "\n", frame])
    
    def _getInt(self, limit, prompt="Choice: "):
        """ Get an integer between 0 and limit from the user and return it.

        Arguments:
        limit -- the upper limit (inlusive)
        promt -- text to be displayed to the user
        """
        response = int(raw_input(prompt))
        while(response < 0 or response >= limit):
            print "Invalid choice, try again."
            response = int(raw_input(prompt))
            return response
    
    def _getString(self, minlength, prompt):
        """ Get a string of minimum minlength characters from the user and return it.

        Arguments:
        minlength -- the minimum string length
        promt -- text to be displayed to the user
        """
        response = raw_input(prompt)
        while(len(response)<minlength):
            print "I need at least " + str(minlength) + " characters."
            response = raw_input(prompt)
            return response

