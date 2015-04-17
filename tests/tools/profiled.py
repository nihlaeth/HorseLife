import cProfile
import StringIO
import pstats
import contextlib


@contextlib.contextmanager
def profiled(echo=False):
    if echo:
        pr = cProfile.Profile()
        pr.enable()
        yield
        pr.disable()
        s = StringIO.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        # uncomment this to see who's calling what
        # ps.print_callers()
        print s.getvalue()
    else:
        yield
