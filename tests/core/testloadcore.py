"""Test LoadCore."""
from nose.tools import assert_equals
import mock

from core.loadcore import LoadCore
from support.messages.savedgame import SavedGame
from support.messages.newgame import NewGame
from errors.invalidchoice import InvalidChoice


class TestLoadCore(object):

    """Test LoadCore."""

    def test_init(self):
        """Test LoadCore.__init__()."""
        # if it dies, there's a problem
        LoadCore()

    @mock.patch("os.listdir")
    def test_get_actions(self, m_listdir):
        """Test LoadCore.get_actions(None)."""
        m_listdir.return_value = ["file1", "file2"]
        actions = LoadCore().get_actions(None)
        assert_equals(len(actions), 2)
        assert_equals(actions[0].file_name, "file1")
        assert_equals(actions[1].file_name, "file2")

    def test_get_menu(self):
        """Test LoadCore.get_menu()."""
        menu = LoadCore().get_menu()
        assert_equals(len(menu), 3)
        assert_equals(isinstance(menu[0], NewGame), True)

    def test_choice(self):
        """Test LoadCore.choice(None, choice)."""
        core = LoadCore()
        saved_game = SavedGame("file")
        result = core.choice(None, saved_game)
        assert_equals(result, saved_game)
        new_game = NewGame()
        result = core.choice(None, new_game)
        assert_equals(result, new_game)
        try:
            core.choice(None, "invalid-choice")
        except InvalidChoice:
            assert True
        else:
            assert False
