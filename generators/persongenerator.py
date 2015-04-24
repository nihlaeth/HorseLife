"""Generator for Person models."""
import random
import names

from generator import Generator
from models.person import Person


class PersonGenerator(Generator):

    """Generator for Person models."""

    # Arguments are supposed to be different from parent class method.
    # pylint: disable=arguments-differ
    @classmethod
    def _gen_one(cls, agerange, money, name=None):
        """Generate a person.

        agerange -- age range the person should be in. If this is an
        inteter, the person will be this exact age. If it's a string
        in [child, adult, twenties, older], it will be a random number
        from those ranges.
        money -- how much money a person should have to start with.
        Eiter a string in [low, mid, high] or an integer.
        name -- Set to None to activate the name generator. Names should
        be uninque if there's any reasonable way to do that, so don't
        specify a name when creating multiple people at once!
        """
        if agerange == "child":
            age = random.randint(12, 18)
        elif agerange == "adult":
            age = random.randint(18, 70)
        elif agerange == "twenties":
            age = random.randint(18, 30)
        elif agerange == "older":
            age = random.randint(30, 70)
        elif isinstance(agerange, int):
            age = agerange
        else:
            # unknown agerange
            raise

        if name is None:
            # We don't care about gender here
            name = names.get_full_name()

        if money == "low":
            money = 100
        elif money == "mid":
            money = 2000
        elif money == "high":
            money = 10000
        elif isinstance(money, int):
            # It's in integer already, do nothing.
            pass

        return Person(name=name, age=age, money=money)

    # I respectfully disagree. 6 arguments is just fine.
    # pylint: disable=too-many-arguments
    @classmethod
    def gen_many(cls, session, num, agerange, money, name=None):
        """Generate people.

        session -- sqlalchemy session
        num -- number of people to create (int)
        agerange -- age range the person should be in. If this is an
        inteter, the person will be this exact age. If it's a string
        in [child, adult, twenties, older], it will be a random number
        from those ranges.
        money -- how much money a person should have to start with.
        Eiter a string in [low, mid, high] or an integer.
        name -- Set to None to activate the name generator. Names should
        be uninque if there's any reasonable way to do that, so don't
        specify a name when creating multiple people at once!
        """
        result = []
        for _ in range(num):
            result.append(cls._gen_one(agerange, money, name))
        session.add_all(result)
        session.flush()
        return result
