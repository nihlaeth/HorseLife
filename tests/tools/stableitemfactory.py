import factory

from models.stableitem import StableItem


class StableItemFactory(factory.Factory):
    class Meta:
        model = StableItem

    name = "food"
    value = 0
