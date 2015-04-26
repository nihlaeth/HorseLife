"""StableItem factory to simplify testing."""
import factory

from models.stableitem import StableItem


class StableItemFactory(factory.Factory):

    """StableItem factory to simplify testing."""

    class Meta(object):

        """Meta class."""

        model = StableItem

    name = "food"
    value = 0
