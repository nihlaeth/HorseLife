from backend import Backend
from models.setting import Setting


class SettingBackend(Backend):
    @classmethod
    def all(cls, session):
        models = session.query(Setting).order_by(Setting.id)
        return [SettingBackend(model.id) for model in models]

    @classmethod
    def one(cls, session, name):
        return SettingBackend(
                session.query(Setting).filter_by(name=name)[0].id)

    @classmethod
    def _one_id(cls, session, id):
        return session.query(Setting).filter_by(id=id)[0]

    def __init__(self, id):
        self._id = id

    def get(self, session, name):
        setting = SettingBackend._one_id(session, self._id)
        return getattr(setting, name)

    def set(self, session, name, value):
        setting = SettingBackend._one_id(session, self._id)
        setattr(setting, name, value)
