from nose.tools import assert_equals, assert_less, assert_is_not

from tests.tools.dummydb import DummyDB
from generators.persongenerator import PersonGenerator
from models.person import Person


class TestPersonGenerator():
    def test_gen_one(self):
        """ Test PersonGenerator._gen_one(agerange, money, name)"""
        person = PersonGenerator._gen_one("child", "low", "Mary Sue")
        assert_less(person.age, 19)
        assert_equals(person.name, "Mary Sue")
        assert_equals(person.money, 100)

        # Now test random name generator & preset age/money
        person = PersonGenerator._gen_one(23, 1200, None)
        assert_equals(person.age, 23)
        assert_equals(person.money, 1200)
        assert_is_not(person.name, None)

    def test_gen_many(self):
        """ Test PersonGenerator.gen_many(session, n, agerange, money, name)"""
        with DummyDB() as session:
            people = PersonGenerator.gen_many(session, 20, "adult", "mid")
            assert_equals(len(people), 20)
