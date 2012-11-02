from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

from velruse import login_url
import json

@view_config(route_name='home', renderer='home_unauth.jade')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name=='one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'login_url': login_url(request, 'google')}

@view_config(
    context='velruse.AuthenticationComplete',
    renderer='home.jade',
)
def login_complete_view(request):
    context = request.context
    result = {
        'provider_type': context.provider_type,
        'provider_name': context.provider_name,
        'profile': context.profile,
        'credentials': context.credentials,
    }
    return {
        'result': result,
    }

@view_config(
    context='velruse.AuthenticationDenied',
    renderer='home_unauth.jade',
)
def login_denied_view(request):
    return {
        'result': 'denied',
        'login_url': login_url(request, 'google')
    }

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_duckly_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

