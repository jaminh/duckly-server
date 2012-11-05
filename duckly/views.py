"""


"""

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import remember
from pyramid.security import forget
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from pyramid.view import notfound_view_config
from pyramid.view import forbidden_view_config
from pyramid.url import route_url

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    User,
)

from velruse import login_url
import json

@view_config(route_name = 'home.unauth', renderer = 'home_unauth.jade')
def home_unauth(request):
    return {'login_url': login_url(request, 'google')}

@view_config(route_name = 'home', renderer = 'home.jade')
def home(request):
    userid = authenticated_userid(request)
    user = User.get_by_id(userid)
    return {'user': user}

@view_config(context = 'velruse.AuthenticationComplete')
def login_complete_view(request):
    user = User.social(request.context.profile, request.context.credentials)
    DBSession.add(user)
    DBSession.flush()
    headers = remember(request, user.id)
    next = request.params.get('next') or request.route_url('home')
    return HTTPFound(location = next, headers = headers)

@view_config(context = 'velruse.AuthenticationDenied',
             renderer = 'home_unauth.jade')
def login_denied_view(request):
    return logout(request)

@view_config(route_name = 'logout')
def logout(request):
    return HTTPFound(location = route_url('home', request),
                     headers = forget(request))

@notfound_view_config(renderer = 'notfound.jade')
def notfound_view(request):
    return {}

@forbidden_view_config(renderer = 'forbidden.jade')
def forbidden_view(request):
    if authenticated_userid(request):
        return HTTPForbidden()

    next = login_url(request, 'google')
    return HTTPFound(location = next)
