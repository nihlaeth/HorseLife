"""Profiling context manager to help track bugs."""
import cProfile
import StringIO
import pstats
import contextlib


@contextlib.contextmanager
def profiled(echo=False):
    """Profiling context manager to help track bugs.

    Warning: This will slow down your code tenfold, don't trust the
    timings this thing gives you!
    """
    if echo:
        profile = cProfile.Profile()
        profile.enable()

        yield
        profile.disable()
        string = StringIO.StringIO()
        p_stats = pstats.Stats(profile, stream=string).sort_stats('cumulative')
        p_stats.dump_stats("profile-output.log")
    else:
        yield
