"""Setting factory to simplify testing."""
import factory

from models.setting import Setting


class SettingFactory(factory.Factory):

    """Setting factory to simplify testing."""

    class Meta(object):

        """Meta class."""

        model = Setting

    name = factory.Sequence(lambda n: "Test%d" % n)
    numeric = 0
    text = ""
