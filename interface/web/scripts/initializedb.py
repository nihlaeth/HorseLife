import os
import sys
import transaction
from sqlalchemy import engine_from_config

from interface.web.session import SESSION
from models.base import BASE
from models.horse import Horse
from models.stable import Stable
from models.pasture import Pasture
from models.stableitem import StableItem
from models.horseskill import HorseSkill
from models.person import Person
from models.transaction import Transaction
from models.setting import Setting


def usage(argv):
    """Print usage information."""
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: %s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    """Create models in database."""
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    SESSION.configure(bind=engine)
    BASE.metadata.create_all(engine)
    with transaction.manager:
        pass
