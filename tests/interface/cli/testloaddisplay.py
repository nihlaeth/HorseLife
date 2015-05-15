"""Test interface.cli.LoadDisplay."""
from nose.tools import assert_equals
import mock

from interface.cli.loaddisplay import LoadDisplay
from core.loadcore import LoadCore
from support.messages.savedgame import SavedGame
from support.messages.newgame import NewGame
from support.messages.back import Back
from support.messages.quit import Quit


class TestLoadDisplay(object):

    """Test interface.cli.LoadDisplay."""

    def test_init(self):
        """Test LoadDisplay.__init__(core)."""
        core = LoadDisplay("test")
        # pylint: disable=protected-access
        assert_equals(core._core, "test")

    @mock.patch("interface.cli.loaddisplay.debug")
    @mock.patch.object(LoadCore, "choice")
    @mock.patch.object(LoadDisplay, "get_string")
    @mock.patch.object(LoadDisplay, "init")
    def test_display(self, m_init, m_getstr, m_choice, m_debug):
        """Test LoadDisplay.display()."""
        m_debug.return_value = False
        m_init.return_value = None

        display = LoadDisplay(LoadCore())

        # pylint: disable=protected-access
        display._choice = None

        quit_ = Quit()
        m_choice.return_value = quit_
        result = display.display()
        assert_equals(result, quit_)

        back = Back()
        m_choice.side_effect = [
            SavedGame("test"),
            NewGame(),
            back]
        result = display.display()
        assert_equals(isinstance(result, SavedGame), True)

        m_getstr.return_value = "newgame"
        result = display.display()
        assert_equals(isinstance(result, NewGame), True)
        m_getstr.assert_called_once_with("Name your game: ", 4)
        assert_equals(result.file_name, "newgame")

        result = display.display()
        assert_equals(result, back)
