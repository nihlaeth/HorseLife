"""Some init."""
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from session import SESSION
from models.base import BASE
from models.stable import Stable
from models.stableitem import StableItem
from models.horse import Horse
from models.setting import Setting
from models.person import Person
from models.story import Story
from models.message import Message
from models.transaction import Transaction
from models.pasture import Pasture
from models.horseskill import HorseSkill


def main(_, **settings):
    """Return a Pyramid WSGI application.

    Normally a database engine and sessionmaker are provided here,
    but those are created by the lower layers.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    SESSION.configure(bind=engine)
    BASE.metadata.create_all(engine)
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
