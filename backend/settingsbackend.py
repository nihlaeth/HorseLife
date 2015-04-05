from backend import Backend
from models.setting import Setting


class SettingsBackend(Backend):
    @classmethod
    def all(cls, session):
        models = session.query(Setting).order_by(Setting.id)
        return [SettingsBackend(model.id) for model in models]

    @classmethod
    def one(cls, session, name):
        return SettingsBackend(
                session.query(Setting).filter_by(name=name)[0].id)

    @classmethod
    def _one_id(cls, session, id):
        return session.query(Setting).filter_by(id=id)[0]

    def __init__(self, id):
        self._id = id

    def get(self, session, name):
        setting = SettingsBackend._one_id(session, self._id)
        return getattr(setting, name)

    def set(self, session, name, value):
        setting = SettingsBackend._one_id(session, self._id)
        setattr(setting, name, value)
