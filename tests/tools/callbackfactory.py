import factory

from models.callback import Callback


class CallbackFactory(factory.Factory):
    class Meta:
        model = Callback
    obj = "HorseBackend"
    obj_id = 1
