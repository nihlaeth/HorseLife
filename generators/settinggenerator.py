"""Generator for Setting models."""
from generator import Generator
from models.setting import Setting


class SettingGenerator(Generator):

    """Generator for Setting models."""

    # Arguments are supposed to be different from parent class method.
    # pylint: disable=arguments-differ
    @classmethod
    def _gen_one(cls, name, numeric, text):
        """Generate single Setting model.

        name -- setting name
        numeric -- numerical value (if this setting has one)
        text -- string value (if this setting has one)
        """
        return Setting(name=name, numeric=numeric, text=text)

    @classmethod
    def gen_many(cls, session, settings):
        """Generate one or more Setting objects.

        session -- sqlalchemy session
        settings -- dict with setting info
        example:
        {"Date": [0, ""],
         "Time": [20, ""]}
        """
        result = []
        for setting in settings:
            result.append(cls._gen_one(
                setting["name"],
                setting["numeric"],
                setting["text"]))
        session.add_all(result)
        session.flush()
        return result
