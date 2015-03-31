from nose.tools import assert_equals
import mock

from interface.cli.display import Display


class TestDisplay():
    def __init__(self):
        self.display = Display()

    def test_get_int(self):
        print "Test Display._get_int(limit)"
        print "-- basic functionality"
        with mock.patch("__builtin__.raw_input", side_effect=["1"]):
            assert_equals(self.display._get_int(2), 1)

        print "-- test lower limit (0)"
        with mock.patch("__builtin__.raw_input",
                        side_effect=["-10", "-2", "0", "1"]):
            assert_equals(self.display._get_int(2), 0)

        print "-- test upper limit"
        with mock.patch("__builtin__.raw_input",
                        side_effect=["20", "10", "9", "8"]):
            assert_equals(self.display._get_int(10), 9)

    def test_get_string(self):
        print "Test Display._get_string(max_length)"
        print "-- basic functionality"
        with mock.patch("__builtin__.raw_input",
                        side_effect=["test"]):
            assert_equals(self.display.get_string(2, "gimme a string: "),
                          "test")
        print "-- minimum string length"
        with mock.patch("__builtin__.raw_input",
                        side_effect=["no", "yes", "Even better!"]):
            assert_equals(self.display.get_string(3, "gimme a string: "),
                          "yes")

    def test_format_title(self):
        print "Test Display._format_title()"
        print "-- basic functionality"
        self.display._screen_width = 20
        self.display._title = "test"
        assert_equals(
            self.display._format_title(),
            "====================\n===     test     ===\n====================")

    def test_repeat(self):
        print "Test Display._repeat(string, n)"
        print "-- basic string repetition"
        assert_equals(self.display._repeat("n", 5), "nnnnn")
        print "-- handling of non-string data"
        assert_equals(self.display._repeat(0, 5), "00000")
        assert_equals(
                self.display._repeat(["test", 0], 5),
                "['test', 0]['test', 0]['test', 0]['test', 0]['test', 0]")
        print "-- handling of n=0"
        assert_equals(self.display._repeat("test", 0), "")
        print "-- handling of n<0"
        assert_equals(self.display._repeat("a", -1), "")

    def test_wrap_text(self):
        self.display._screen_width = 10
        print "Testing Display._wrap_text(text)"
        print "-- single paragraph"
        text1 = "wrap this text"
        assert_equals(self.display._wrap_text(text1), "wrap this\ntext")
        print "-- multiple paragraphs"
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
        print "Test Display.display()"
        data = ["option zero", "option one"]
        menu = ["quit", "save"]
        self.display.init(data, menu)
        self.display._title = "test"
        self.display._screen_width = 20

        with mock.patch('__builtin__.raw_input', side_effect=["0", "3"]):
            print "-- basic testing"
            assert_equals(self.display.display(), "option zero")
            print "-- menu"
            assert_equals(self.display.display(), "save")
