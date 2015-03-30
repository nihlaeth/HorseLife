from textwrap import wrap, fill


class Display():
    def __init__(self):
        """ Initiate with only static data."""
        self._screen_width = 70
        self._separator = self._repeat('-', self._screen_width)
        self._title = "You should not be seeing this"
        self._description = "This class is not to be called directly."

    def init(self, data, menu):
        """ Initialize with (database) data.

        Arguments:
        data -- list of classes to be displayed
        menu -- menu options (quit, back to main, etc)
        """
        self._data = data
        self._menu = menu

    def display(self):
        """ Display screen and return user choice (class)."""
        print self._format_title()

        print ''.join([self._wrap_text(self._description), "\n\n"])

        self._i = 0

        for action in self._data:
            print ''.join([str(self._i), ") ", action])
            self._i += 1

        print ''.join(["\n\n", self._separator, "\n\n"])

        for item in self._menu:
            print ''.join([str(self._i), ") ", item])
            self._i += 1

        choice = self._get_int(self._i)

        if choice < len(self._data):
            return self._data[choice]
        else:
            return self._menu[choice-len(self._data)]

    def _repeat(self, string, n):
        """ Repeat string n times and return it."""
        return ''.join([str(string) for i in range(n)])

    def _format_title(self):
        """ Format the page title and return it."""
        frame = self._repeat("=", self._screen_width)
        whitespace = len(frame) - 6 - len(self._title)
        leading_whitespace = whitespace / 2
        trailing_whitespace = (whitespace / 2 if whitespace % 2 == 0
                               else whitespace / 2 + 1)
        header = ''.join([
            "===",
            self._repeat(" ", leading_whitespace),
            self._title,
            self._repeat(" ", trailing_whitespace),
            "==="])
        return ''.join([frame, "\n", header, "\n", frame])

    def _get_int(self, limit, prompt="Choice: "):
        """ Get an integer between 0 and limit from the user and return it.

        Arguments:
        limit -- the upper limit (exclusive)
        promt -- text to be displayed to the user
        """
        response = int(raw_input(prompt))
        while(response < 0 or response >= limit):
            print "Invalid choice, try again."
            response = int(raw_input(prompt))
        return response

    def _get_string(self, min_length, prompt):
        """ Get a str of min min_length characters from user and return it.

        Arguments:
        min_length -- the minimum string length
        promt -- text to be displayed to the user
        """
        response = raw_input(prompt)
        while(len(response) < min_length):
            print ''.join([
                "I need at least ",
                str(min_length),
                " characters."])
            response = raw_input(prompt)
        return response

    def _wrap_text(self, text):
        """ Wrap text to screen width while preserving paragraphs."""
        paragraphs = text.split("\n")
        return '\n'.join([fill(p, self._screen_width) for p in paragraphs])
