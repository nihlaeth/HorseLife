"""Test BuildingCore."""
from nose.tools import assert_equals
import mock

from core.buildingcore import BuildingCore
from core.stablecore import StableCore
from backend.stablebackend import StableBackend
from support.messages.quit import Quit
from tests.tools.dummydb import DummyDB
from tests.tools.stablefactory import StableFactory


class TestBuildingCore(object):

    """Test BuildingCore."""

    @mock.patch.object(StableCore, "run")
    def test_run(self, m_stable):
        """Test BuildingCore.run()."""
        with DummyDB() as session:
            session.add(StableFactory())
            quit_ = Quit()
            m_stable.return_value = quit_

            result = BuildingCore(StableBackend(session, 1)).run()
            assert_equals(result, quit_)
