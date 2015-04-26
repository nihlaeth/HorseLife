"""Callback Factory to simplify testing."""
import factory

from models.callback import Callback


class CallbackFactory(factory.Factory):

    """Callback Factory to simplify testing."""

    class Meta(object):

        """Meta class."""

        model = Callback
    obj = "HorseBackend"
    obj_id = 1
