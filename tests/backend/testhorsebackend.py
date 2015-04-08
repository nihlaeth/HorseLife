from nose.tools import assert_equals, assert_less, assert_greater

from backend.horsebackend import HorseBackend
from tests.tools.dummydb import DummyDB
from tests.tools.horsefactory import HorseFactory


class TestHorseBackend():
    def test_init(self):
        assert_equals(HorseBackend(1)._id, 1)

    def test_one_id(self):
        with DummyDB() as session:
            session.add(HorseFactory.build())
            assert_equals(HorseBackend._one_id(session, 1).id, 1)

    def test_all(self):
        with DummyDB() as session:
            horses = HorseFactory.build_batch(10)
            session.add_all(horses)
            backends = HorseBackend.all(session)
            assert_equals(len(backends), 10)

    def test_get(self):
        with DummyDB() as session:
            session.add(HorseFactory.build(name="Spirit"))
            backend = HorseBackend(1)
            assert_equals(backend.get(session, "name"), "Spirit")

    def test_set(self):
        with DummyDB() as session:
            session.add(HorseFactory.build(name="Storm"))
            backend = HorseBackend(1)
            backend.set(session, "name", "Mary")
            assert_equals(backend.get(session, "name"), "Mary")

    def test_pass_time(self):
        with DummyDB() as session:
            session.add(HorseFactory.build(name="Fury"))
            backend = HorseBackend(1)
            backend.pass_time(session, 200, False)
            assert_less(backend.get(session, "hygiene"), 100)

    def test_groom(self):
        with DummyDB() as session:
            session.add(HorseFactory.build(hygiene=0, stimulation=0))
            backend = HorseBackend(1)
            backend.groom(session)
            assert_equals(backend.get(session, "hygiene"), 100)
            assert_greater(backend.get(session, "stimulation"), 0)

    def test_pet(self):
        with DummyDB() as session:
            session.add(HorseFactory.build(stimulation=0))
            backend = HorseBackend(1)
            backend.pet(session)
            assert_greater(backend.get(session, "stimulation"), 0)
