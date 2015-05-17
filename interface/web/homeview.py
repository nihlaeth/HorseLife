"""Home page."""
from pyramid.view import view_config

from session import SESSION
from backend.horsebackend import HorseBackend


@view_config(route_name='home', renderer='../../assets/web/templates/home.pt')
class HomeView(object):

    """Home page view."""

    def __init__(self, request):
        """Init."""
        self._request = request
        self._horses = HorseBackend.all(SESSION)

    def __call__(self):
        """Call."""
        return {'horses': self._horses, 'project': 'HorseLife'}
