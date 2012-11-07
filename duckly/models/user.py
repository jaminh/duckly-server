"""


"""

from pyramid.security import (
    Allow,
    Authenticated,
    Everyone
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

class UserFactory(object):
    """


    """

    __acl__ = [
        (Allow, Everyone, 'view')
    ]

    def __init__(self, request):
        """


        """

        self.request = request

    def __getitem__(self, key):
        """


        """

        return User.get_by_id(key)


class User(Base):
    """


    """
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

    @property
    def __acl__(self):
        """


        """

        return [
            (Allow, Authenticated, 'authenticated'),
            (Allow, self.id, 'edit')
        ]


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

