"""Interface for *Generator classes to inherit from."""


class Generator(object):

    """Some common methods for *Generator classes to inherit."""

    @classmethod
    def _gen_one(cls):
        """Generate a single model."""
        pass

    @classmethod
    def gen_many(cls, session, num):
        """Generate one or more models and add them to the session."""
        pass
