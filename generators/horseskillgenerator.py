"""Generator for HorseSkill models."""
import ConfigParser

from generator import Generator
from models.horseskill import HorseSkill


# pylint: disable=arguments-differ
class HorseSkillGenerator(Generator):

    """Generator for HorseSkill models."""

    def __init__(self):
        """Setup config parser."""
        self._config = ConfigParser.SafeConfigParser()
        self._config.read("config/horseskills.cfg")

    def _gen_one(self, text_id, horse_id):
        """Generate a single HorseSkill model."""
        return HorseSkill(
            name=text_id,
            depends_on=self._config.get(text_id, "depends_on"),
            discipline=self._config.get(text_id, "discipline"),
            difficulty=self._config.getint(text_id, "difficulty"),
            life_stage=self._config.get(text_id, "life_stage"),
            progress=0,
            horse_id=horse_id)

    def gen_many(self, session, horses):
        """Generate complete skillsets for all horses in the list.

        session -- sqlalchemy session
        horses -- integer list of horse id's
        """
        result = []
        for horse_id in horses:
            for text_id in self._config.sections():
                result.append(self._gen_one(text_id, horse_id))
        session.add_all(result)
        session.flush()
        return result
