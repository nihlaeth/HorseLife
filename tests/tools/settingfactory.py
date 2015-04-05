import factory

from models.setting import Setting


class SettingFactory(factory.Factory):
    class Meta:
        model = Setting

    name = factory.Sequence(lambda n: "Test%d" % n)
    numeric = 0
    text = ""
