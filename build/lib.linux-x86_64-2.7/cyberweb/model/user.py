from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy.types import Integer, String, DateTime, Boolean
from datetime import datetime

from cyberweb.model.meta import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100))
    password = Column(String(100))
    firstname = Column(String(100))
    lastname = Column(String(100))
    email = Column(String(100))
    institution = Column(String(100))
    last_login_date = Column(DateTime())
    last_login_ip = Column(String(100))
    active = Column(Boolean, default=True)
    created = Column(DateTime())
    verified = Column(Boolean())

    def __init__(self,
                username=None,
                password=None,
                email=None,
                firstname=None,
                lastname=None,
                institution=None,
                active=True,
                created=datetime.now()
                ):
        self.username = username
        self.password = password
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.institution = institution
        self.active = active
        self.created = created

    def __repr__(self):
        return self.username


class GroupDefinition(Base):
    __tablename__ = 'group_definition'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    description = Column(String(255))
    active = Column(Boolean, default=True)

    def __init__(self, name=None, description='', active=True):
        self.name = name
        self.description = description
        self.active = active

    def __repr__(self):
        return self.name


class Group(Base):
    __tablename__ = 'user_group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    group_definition_id = Column(Integer, ForeignKey('group_definition.id'))
    active = Column(Boolean, default=True)

    user = relation('User', backref=backref('groups', order_by=id))
    group_definition = relation('GroupDefinition', backref=backref('members', order_by=id))

    def __init__(self, user_id=None, group_id=None, active=True):
        self.user_id = user_id
        self.group_definition_id = group_id
        self.active = active

    def __repr__(self):
        # Return Group Name for Admin Grid display
        return self.group_definition.name
