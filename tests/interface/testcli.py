"""Test interface.cli.display."""
from nose.tools import assert_equals
import mock

from interface.cli.display import Display
from support.messages.action import Action


class TestDisplay(object):

    """Test interface.cli.display."""

    def __init__(self):
        """Set display."""
        self.display = Display()

    def test_get_int(self):
        """Test Display._get_int(max)."""
        # Testing a protected member.
        # pylint: disable=protected-access
        with mock.patch("__builtin__.raw_input", side_effect=["1"]):
            assert_equals(self.display._get_int(2), 1)

        with mock.patch("__builtin__.raw_input",
                        side_effect=["-10", "-2", "0", "1"]):
            assert_equals(self.display._get_int(2), 0)

        with mock.patch("__builtin__.raw_input",
                        side_effect=["20", "10", "9", "8"]):
            assert_equals(self.display._get_int(10), 9)

    def test_get_string(self):
        """Test Display.get_string(min_length, prompt)."""
        with mock.patch("__builtin__.raw_input",
                        side_effect=["test"]):
            assert_equals(self.display.get_string(2, "gimme a string: "),
                          "test")
        with mock.patch("__builtin__.raw_input",
                        side_effect=["no", "yes", "Even better!"]):
            assert_equals(self.display.get_string(3, "gimme a string: "),
                          "yes")

    def test_format_title(self):
        """Test Display._format_title()."""
        # pylint: disable=protected-access
        self.display._screen_width = 20
        self.display._title = "test"
        assert_equals(
            self.display._format_title(),
            "====================\n===     test     ===\n====================")

    def test_repeat(self):
        """Test Display._repeat(string, n)."""
        # pylint: disable=protected-access
        assert_equals(self.display._repeat("n", 5), "nnnnn")
        assert_equals(self.display._repeat(0, 5), "00000")
        assert_equals(
            self.display._repeat(["test", 0], 5),
            "['test', 0]['test', 0]['test', 0]['test', 0]['test', 0]")
        assert_equals(self.display._repeat("test", 0), "")
        assert_equals(self.display._repeat("a", -1), "")

    def test_wrap_text(self):
        """Test Display._wrap_text(text)."""
        # pylint: disable=protected-access
        self.display._screen_width = 10
        text1 = "wrap this text"
        assert_equals(self.display._wrap_text(text1), "wrap this\ntext")
        text2 = ("Paragraph one is really not much to look at\n\n"
                 "Can't say that the second is much better.")
        wrappedtext = ("Paragraph\n"
                       "one is\n"
                       "really not\n"
                       "much to\n"
                       "look at\n"
                       "\n"
                       "Can't say\n"
                       "that the\n"
                       "second is\n"
                       "much\n"
                       "better.")
        assert_equals(self.display._wrap_text(text2), wrappedtext)

    def test_display(self):
        """Test Display.display()."""
        # pylint: disable=protected-access
        option_zero = Action("option zero", "")
        option_one = Action("option one", "")
        self.display._actions = [option_zero, option_one]
        self.display._menu = ["quit", "save"]
        self.display._info = []
        # self.display.init(data, menu)
        self.display._title = "test"
        self.display._screen_width = 20

        with mock.patch('__builtin__.raw_input', side_effect=["0", "3"]):
            assert_equals(self.display.display(), option_zero)
            assert_equals(self.display.display(), "save")
