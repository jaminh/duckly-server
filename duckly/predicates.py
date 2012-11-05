"""


"""

from pyramid.security import authenticated_userid

def authorized(info, request):
    """


    """

    return bool(authenticated_userid(request))

def unauthorized(info, request):
    """


    """

    return not bool(authenticated_userid(request))
