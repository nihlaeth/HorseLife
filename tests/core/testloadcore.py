"""Test LoadCore."""
from nose.tools import assert_equals
import mock

from core.loadcore import LoadCore
from interface.cli.loaddisplay import LoadDisplay
from support.messages.savedgame import SavedGame
from support.messages.newgame import NewGame
from support.messages.quit import Quit


class TestLoadCore(object):

    """Test LoadCore."""

    @mock.patch("core.loadcore.debug")
    @mock.patch("os.listdir")
    @mock.patch.object(LoadDisplay, "init")
    @mock.patch.object(LoadDisplay, "get_string")
    @mock.patch.object(LoadDisplay, "display")
    def test_run(self, m_display, m_getstr, m_init, m_listdir, m_debug):
        """Test LoadCore.run()."""
        core = LoadCore()

        # Disable pdb
        m_debug.return_value = False

        # Test SavedGame
        saved_game = SavedGame(":memory:")
        m_display.return_value = saved_game
        result = core.run()
        m_display.assert_called_once_with()
        assert_equals(result, saved_game)

        # Test NewGame
        new_game = NewGame()
        m_display.return_value = new_game
        m_getstr.return_value = "test"
        result = core.run()
        m_display.assert_called_with()
        m_getstr.assert_called_once_with(4, "Name your game: ")
        assert_equals(result, new_game)
        assert_equals(result.file_name, "test")

        # Test Quit
        quit_ = Quit()
        m_display.return_value = quit_
        result = core.run()
        m_display.assert_called_with()
        assert_equals(result, quit_)

        # Test directory listing
        m_listdir.return_value = ["file1", "file2"]
        m_display.return_value = Quit()
        core.run()
        args = m_init.call_args_list[-1:]
        arg1 = args[0][0][0]
        arg2 = args[0][0][1]
        assert_equals(arg1[0].file_name, "file1")
        assert_equals(arg1[1].file_name, "file2")
        assert_equals(isinstance(arg2[0], NewGame), True)
        assert_equals(isinstance(arg2[1], Quit), True)
