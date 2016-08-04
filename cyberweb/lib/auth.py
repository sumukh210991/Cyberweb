import logging

from authkit.authorize import NotAuthenticatedError, NotAuthorizedError
from authkit.authorize.pylons_adaptors import authorized
from pylons import session

from cyberweb.model import meta, User, Group


log = logging.getLogger(__name__)


class ValidUser():
    """
    Decorator for validating a user
    """

    def __init__(self):
        pass

    def check(self, app, environ, start_response):
        if 'user' not in session:
            raise NotAuthenticatedError('Not Authenticated')
        return app(environ, start_response)


class ValidGroupMember():
    """
    Decorator for validating a user is part of a group
    """

    def __init__(self, groups):
        self.group_array = groups

    def check(self, app, environ, start_response):
        if 'user' not in session:
            raise NotAuthenticatedError('Not Authenticated')

        try:
            user_id = meta.Session.query(User).filter(User.username == session.get('user')).one().id
        except Exception:
            raise NotAuthenticatedError('Not Authenticated. Contact your Administrator')

        rows = meta.Session.query(Group).filter(Group.user_id == user_id)
        for i in rows.all():
            if i.group_definition.name in self.group_array:
                return app(environ, start_response)

        raise NotAuthorizedError('This user is not a valid member of this group.')


class NotInGroup():
    """
    Decorator for validating a user is not part of a group
    """

    def __init__(self, groups):
        self.group_array = groups

    def check(self, app, environ, start_response):
        if 'user' not in session:
            raise NotAuthenticatedError('Not Authenticated')
        try:
            user_id = meta.Session.query(User).filter(User.username == session.get('user')).one().id
        except Exception:
            raise NotAuthenticatedError('Not Authenticated. Contact your Administrator')

        rows = meta.Session.query(Group).filter(Group.user_id == user_id)
        if rows.count() == 0:
            raise NotAuthorizedError('This user does not belong to any groups.')
        for i in rows.all():
            if i.group.groupname in self.group_array:
                raise NotAuthorizedError('This user is of the group %s' % i.group.groupname)

        return app(environ, start_response)


is_valid_user = ValidUser()
is_verified = NotInGroup(['GCEM_guest'])
is_admin = ValidGroupMember(['Supercw_users', 'Administrators'])
is_developer = ValidGroupMember(['Supercw_users'])
