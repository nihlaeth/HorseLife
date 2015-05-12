"""HorseSkill model."""
from base import BASE
from sqlalchemy import ForeignKey, Column, Integer, String


# pylint: disable=no-init
class HorseSkill(BASE):

    """HorseSkill model."""

    __tablename__ = "horseskills"

    mid = Column(Integer, primary_key=True)

    name = Column(String)
    depends_on = Column(String)
    discipline = Column(String)
    difficulty = Column(Integer)
    life_stage = Column(String)
    progress = Column(Integer)

    horse_id = Column(Integer, ForeignKey("horses.mid"))
