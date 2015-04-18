from nose.tools import assert_equals
import mock

from core.loadcore import LoadCore
from interface.cli.loaddisplay import LoadDisplay
from support.messages.savedgame import SavedGame
from support.messages.newgame import NewGame
from support.messages.quit import Quit
from support.messages.command import Command


class TestLoadCore():
    @mock.patch("os.listdir")
    @mock.patch.object(LoadDisplay, "init")
    @mock.patch.object(LoadDisplay, "get_string")
    @mock.patch.object(LoadDisplay, "display")
    def test_run(self, m1, m2, m3, m4):
        """ Test LoadCore.run()"""
        core = LoadCore()
        # Test SavedGame
        saved_game = SavedGame(":memory:")
        m1.return_value = saved_game
        result = core.run()
        m1.assert_called_once_with()
        assert_equals(result, saved_game)

        # Test NewGame
        new_game = NewGame()
        m1.return_value = new_game
        m2.return_value = "test"
        result = core.run()
        m1.assert_called_with()
        m2.assert_called_once_with(4, "Name your game: ")
        assert_equals(result, new_game)
        assert_equals(result.file_name, "test")

        # Test Quit
        quit = Quit()
        m1.return_value = quit
        result = core.run()
        m1.assert_called_with()
        assert_equals(result, quit)

        # Test Command
        command = Command("assert False")
        m1.return_value = command
        try:
            core.run()
        except AssertionError:
            # test passed!
            m1.assert_called_with()
        else:
            assert False

        # Test directory listing
        m4.return_value = ["file1", "file2"]
        m1.return_value = Quit()
        core.run()
        args = m3.call_args_list[-1:]
        arg1 = args[0][0][0]
        arg2 = args[0][0][1]
        print "arg1=" + str(arg1)
        print "arg2=" + str(arg2)
        assert_equals(arg1[0].file_name, "file1")
        assert_equals(arg1[1].file_name, "file2")
        assert_equals(isinstance(arg2[0], NewGame), True)
        assert_equals(isinstance(arg2[1], Quit), True)
