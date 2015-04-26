"""Test BuildingCore."""
from nose.tools import assert_equals
import mock

from core.buildingcore import BuildingCore
from core.stablecore import StableCore
from backend.stablebackend import StableBackend
from support.messages.quit import Quit


class TestBuildingCore(object):

    """Test BuildingCore."""

    @mock.patch.object(StableCore, "run")
    def test_run(self, m_stable):
        """Test BuildingCore.run()."""
        quit_ = Quit()
        m_stable.return_value = quit_

        result = BuildingCore(StableBackend(1)).run()
        assert_equals(result, quit_)
