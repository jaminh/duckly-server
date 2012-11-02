from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyjade.compiler import Compiler
from pyramid.compat import escape
from pyramid_beaker import session_factory_from_settings

from .models import (
    DBSession,
    Base,
)

def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind = engine)
    Base.metadata.bind = engine

    config = Configurator(settings = settings,
        session_factory = session_factory_from_settings(settings))

    config.add_static_view('img', 'duckly:static/img')
    config.add_static_view('js', 'duckly:static/js')
    config.add_static_view('css', 'duckly:static/css')
    config.add_google_oauth2_login_from_settings()

    config.add_route('home', '/')

    config.scan()

    Compiler.filters['plain'] = lambda x,y: x
    Compiler.filters['css'] = (
        lambda x,y: '<style type="text/css">{0}</style>'.format(x))
    Compiler.filters['javascript'] = (
        lambda x,y: '<script type="text/javascript">{0}</script>'.format(x))
    Compiler.filters['escaped'] = lambda x,y: escape(x)

    return config.make_wsgi_app()

