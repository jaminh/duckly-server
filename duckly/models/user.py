"""


"""

from pyramid.security import (
    Allow,
    Authenticated
)

from datetime import datetime
from .meta import (
    Base,
    DBSession
)
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime
)
import uuid

class User(Base):
    """


    """

    class Root(object):
        """


        """
        __acl__ = [
            (Allow, Authenticated, 'authenticated'),
        ]

        def __init__(self, request):
            self.request = request


    __tablename__ = 'users'

    id = Column(Text, primary_key = True)
    username = Column(Text, unique = True, index = True)
    email = Column(Text, unique = True)
    display_name = Column(Text)
    name = Column(Text)
    creation_date = Column(DateTime, nullable = False,
                           default = datetime.utcnow())

    def __init__(self, profile):
        """


        """

        self.id = profile['accounts'][0]['userid']
        self.username = None
        self.display_name = None
        self.name = profile.get('displayName')
        self.email = profile.get('verifiedEmail')
        self.groups = []

    @property
    def verified(self):
        return bool(self.username)

    @classmethod
    def get_by_id(cls, userid):
        """


        """

        users = DBSession.query(User).filter_by(id = userid).all()
        return users[0] if users else None

    @classmethod
    def social(cls, profile, credentials):
        """


        """

        userid = profile['accounts'][0]['userid']
        user = User.get_by_id(userid)

        if user:
            return user

        return User(profile)

    @classmethod
    def groupfinder(cls, userid, request):
        """


        """

        user = User.get_by_id(userid)

        if user:
            return ['g:verified'] if user.verified else []
            #return ['g:{0}'.format(group) for group in user.groups]

