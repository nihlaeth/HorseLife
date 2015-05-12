"""Provide abstraction layer for HorseSkill model."""
from backend import Backend
from models.horseskill import HorseSkill


class HorseSkillBackend(Backend):

    """Abstraction layer for HorseSkill model."""

    @classmethod
    def _get_skillset(cls, session, horse_id):
        """Get bare skillset for this horse."""
        return session.query(HorseSkill).filter_by(horse_id=horse_id)

    def __init__(self, session, horse_id):
        """Some basic setup.

        Unlike other backends, this one doesn't represent just one
        model. It represents a skillset belonging to a single horse.
        """
        Backend.__init__(self, session, horse_id)
        self._cls = "HorseSkillBackend"
        self._str = str(HorseSkillBackend._get_skillset(session, horse_id))

    def all(self, session):
        """Return the entire (raw) skillset.

        This is used for display purposes.
        """
        return HorseSkillBackend._get_skillset(session, self.id_)
