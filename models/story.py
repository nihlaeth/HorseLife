"""Story model."""
from sqlalchemy import Column, Integer, String, Boolean

from base import BASE


# pylint: disable=no-init
class Story(BASE):

    """Story model.

    A single part in the story progression - or at least it's database
    part. Stories are kept in the config files. This model only keeps
    track of which parts have been read/viewed already, and allows for
    easy querying.
    """

    __tablename__ = "story"
    mid = Column(Integer, primary_key=True)
    text_id = Column(String)  # Also a section in story config file
    read = Column(Boolean)
    depends_on = Column(String)
    location = Column(String)
    level = Column(Integer)
