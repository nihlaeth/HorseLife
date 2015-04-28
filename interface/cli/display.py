"""Interface to inherit from for *Display classes."""
from textwrap import fill

from support.messages.meter import Meter
from support.messages.command import Command


# pylint: disable=too-many-instance-attributes
class Display(object):

    """Common methods to inherit from by *Display classes."""

    def __init__(self):
        """Initiate with only static data."""
        self._screen_width = 70
        self._separator = self._repeat('-', self._screen_width)
        self._title = "You should not be seeing this"
        self._description = "This class is not to be called directly."
        self._data = None
        self._menu = None
        self._info = None
        self._story = None

    def init(self, data, menu, info=None, story=None):
        """Initialize with backend data.

        Arguments:
        data -- list of classes to be displayed
        menu -- menu options (quit, back to main, etc)
        info -- list of strings to display
        """
        self._data = data
        self._menu = menu
        if info is None:
            info = []
        self._info = info
        self._story = story

    def display(self):
        """Display screen and return user choice (class)."""
        print self._format_title()

        print ''.join([self._wrap_text(self._description), "\n\n"])

        for string in self._info:
            if isinstance(string, Meter):
                print self._meter(string)
            else:
                print self._wrap_text(str(string))

        print "\n\n"

        count = 0

        if self._story is not None:
            print self._separator
            print self._wrap_text(self._story.text)
            print "".join([str(count), ") ", str(self._story.action)])
            count += 1
            print self._separator

        for action in self._data:
            print self._wrap_text(''.join([
                str(count),
                ") ",
                str(action)]))
            count += 1

        print ''.join(["\n\n", self._separator, "\n\n"])

        for item in self._menu:
            print self._wrap_text(''.join([str(count), ") ", str(item)]))
            count += 1

        choice = self._get_int(count)

        offset = 0 if self._story is None else 1
        if choice == 555:
            # debug console
            return Command(self.get_string(0, "Command: "))
        elif self._story is not None and choice == 0:
            return self._story.action
        elif choice - offset < len(self._data):
            return self._data[choice - offset]
        else:
            return self._menu[choice - len(self._data) - offset]

    def hide(self):
        """Just a placeholder."""
        pass

    def _repeat(self, string, num):
        """Repeat string num times and return it."""
        return ''.join([str(string) for _ in range(num)])

    def _format_title(self):
        """Format the page title and return it."""
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
        """Get an integer between 0 and limit from the user and return it.

        Arguments:
        limit -- the upper limit (exclusive)
        promt -- text to be displayed to the user
        """
        try:
            response = int(raw_input(prompt))
        except ValueError:
            response = -1
        while (response < 0 or response >= limit) and response != 555:
            print "Invalid choice, try again."
            try:
                response = int(raw_input(prompt))
            except ValueError:
                pass
        return response

    def get_string(self, min_length, prompt):
        """Get a str of min min_length characters from user and return it.

        Arguments:
        min_length -- the minimum string length
        promt -- text to be displayed to the user
        """
        response = raw_input(prompt)
        while len(response) < min_length:
            print ''.join([
                "I need at least ",
                str(min_length),
                " characters."])
            response = raw_input(prompt)
        return response

    def _wrap_text(self, text):
        """Wrap text to screen width while preserving paragraphs."""
        paragraphs = text.split("\n")
        return '\n'.join([fill(p, self._screen_width) for p in paragraphs])

    def _meter(self, meter):
        """Return a graphical meter."""
        percent_filled = float(meter.percent) / 100.
        columnsfilled = int((self._screen_width - 2) * percent_filled)
        return ''.join([
            "[",
            self._repeat("=", columnsfilled),
            self._repeat(" ", self._screen_width - columnsfilled - 2),
            "]"])
