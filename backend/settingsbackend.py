from backend import Backend
from models.setting import Setting


class SettingsBackend(Backend):
    @classmethod
    def all(cls, session):
        return session.query(Setting).order_by(Setting.id)

    @classmethod
    def one(cls, session, name):
        return session.query(Setting).filter_by(name=name)[0]
