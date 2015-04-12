from backend import Backend
from models.setting import Setting


class SettingBackend(Backend):
    @classmethod
    def all(cls, session):
        """ Return a list of all settings (encapsulated).

        session -- sqlalchemy session
        """
        models = session.query(Setting).order_by(Setting.id)
        return [SettingBackend(model.id) for model in models]

    @classmethod
    def one(cls, session, name):
        """ Return encapsulated setting, selected by (unique) name.

        session -- sqlalchemy session
        name -- setting name (str)
        """
        return SettingBackend(
                session.query(Setting).filter_by(name=name)[0].id)

    @classmethod
    def _one_id(cls, session, id):
        """ Return (unencapsulated) setting model - internal use only!

        session -- sqlalchemy session
        id -- setting model id (int)
        """
        return session.query(Setting).filter_by(id=id)[0]

    def __init__(self, id):
        """ Set model id.

        id -- model id (int)
        """
        self._id = id

    def get(self, session, key):
        """ Get attribute from encapsulated model.

        session -- sqlalchemy session
        key -- attribute name (str)
        """
        setting = SettingBackend._one_id(session, self._id)
        return getattr(setting, key)

    def set(self, session, name, key):
        """ Set attribute on encapsulated model.

        session -- sqlalchemy session
        key -- attribute name (str)
        value -- new value
        """
        setting = SettingBackend._one_id(session, self._id)
        setattr(setting, name, key)
