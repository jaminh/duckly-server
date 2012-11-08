"""


"""

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config
from .models import (
    DBSession,
    Base,
    User
)
from .predicates import (
    authorized,
    unauthorized
)
from pyramid.security import (
    Allow,
    Authenticated,
    NO_PERMISSION_REQUIRED
)

class Root(object):
    """


    """

    __acl__ = [
        (Allow, Authenticated, 'authenticated'),
        (Allow, 'g:verified', 'verified'),
        (Allow, NO_PERMISSION_REQUIRED, 'none')
    ]

    def __init__(self, request):
        """


        """

        self.request = request


def main(global_config, **settings):
    """


    """

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind = engine)
    Base.metadata.bind = engine

    session_factory = session_factory_from_settings(settings)
    authn_policy = AuthTktAuthenticationPolicy(settings['auth.secret'],
                                               callback = User.groupfinder)
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings = settings,
        session_factory = session_factory,
        authentication_policy = authn_policy,
        authorization_policy = authz_policy,
        root_factory = Root)

    config.add_static_view('images', 'duckly:static/images')
    config.add_static_view('js', 'duckly:static/js')
    config.add_static_view('css', 'duckly:static/css')
    config.add_google_oauth2_login_from_settings(prefix = 'google.')
    config.add_route('logout', '/logout')
    config.add_route('home.unauth', '/', custom_predicates = (unauthorized,))
    config.add_route('home', '/', custom_predicates = (authorized,))
    config.add_route('signup', '/signup')

    config.scan()

    return config.make_wsgi_app()
