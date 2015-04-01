from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from models.base import Base
from models.building import Building
from models.buildingproperties import BuildingProperties
from models.horse import Horse
from models.person import Person
from models.setting import Setting

class DummyDB():
    def __init__(self):
        self._Session = sessionmaker()
        self._engine = create_engine('sqlite:///memory:', echo=True)
        self._Session.configure(bind=self._engine)
        Base.metadata.create_all(self._engine)

    def __enter__(self):
        self._session = self._Session()
        return self._session

    def __exit__(self, type, value, tb):
        if type is not None:
            # Exception occured
            self._session.rollback()
        else:
            self._session.commit()
        self._session.close()
        

