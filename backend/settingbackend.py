"""Provide abstraction layer for Setting model."""
from backend import Backend
from models.setting import Setting


class SettingBackend(Backend):

    """Abstraction layer for Setting model."""

    @classmethod
    def all(cls, session):
        """Return a list of all settings (encapsulated).

        session -- sqlalchemy session
        """
        models = session.query(Setting).order_by(Setting.mid)
        return [SettingBackend(session, model.mid) for model in models]

    @classmethod
    def one(cls, session, name):
        """Return encapsulated setting, selected by (unique) name.

        session -- sqlalchemy session
        name -- setting name (str)
        """
        return SettingBackend(
            session,
            session.query(Setting).filter_by(name=name)[0].mid)

    @classmethod
    def _one_id(cls, session, id_):
        """Return (unencapsulated) setting model - internal use only.

        session -- sqlalchemy session
        id -- setting model id (int)
        """
        return session.query(Setting).filter_by(mid=id_)[0]

    def __init__(self, session, id_):
        """Set model id.

        id -- model id (int)
        """
        Backend.__init__(self, session, id_)
        self._cls = "SettingBackend"

    def set(self, session, key, value):
        """Set attribute on encapsulated model.

        session -- sqlalchemy session
        key -- attribute name (str)
        value -- new value
        """
        setting = SettingBackend._one_id(session, self.id_)
        setting.set(key, value)
