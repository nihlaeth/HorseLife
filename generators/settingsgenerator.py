from generator import Generator
from models.setting import Setting


class SettingsGenerator(Generator):
    @classmethod
    def _gen_one(cls, name, numeric, text):
        return Setting(name=name, numeric=numeric, text=text)

    @classmethod
    def gen_many(cls, session, settings):
        result = []
        for s in settings:
            result.append(cls._gen_one(s, settings[s][0], settings[s][1]))
        session.add_all(result)
        return result
