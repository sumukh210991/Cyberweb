from sqlalchemy import Column,ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy.types import Integer, String, DateTime, Boolean
from datetime import datetime

from cyberweb.model.meta import Base
from cyberweb.model.user import User, Group

class MessageType(Base):
    __tablename__ = 'message_type'
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(25),unique=True)
    description = Column(String(255))
    active = Column(Boolean,default=True)
    
    def __init__(self,name=None,description='',active=True):
        self.name = name
        self.description = description
        self.active = active

class Message(Base):
    __tablename__ = 'message'
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    message = Column(String(255))
    message_type_id = Column(Integer,ForeignKey('message_type.id'),nullable=False)
    author_id = Column(Integer,ForeignKey('user.id'))
    recipient_user_id = Column(Integer, ForeignKey('user.id'),nullable=True)
    recipient_group_id = Column(Integer,ForeignKey('user_group.id'),nullable=True)
    active = Column(Boolean,default=True)
    date = Column(DateTime,default=datetime.now())
    
    author = relation('User', primaryjoin=author_id == User.id, backref=backref('messages_sent'))
    recipient_user = relation('User', primaryjoin=recipient_user_id == User.id, backref=backref('messages_by_user'))
    recipient_group = relation('Group', backref=backref('messages_by_group'))
    message_type = relation('MessageType')

    def __init__(self,
                 author_id=None,
                 recipient_id=None,
                 message=None,
                 group = False,
                 message_type_id = 1,
                 active=True
                 ):
        self.author_id = author_id
        self.message = message
        self.message_type_id = message_type_id
        self.active = active
        self.date = datetime.now()

        # Broadcast message. @todo: Worry about permission in the cyberweb middleware later.
        if not recipient_id: pass
        elif group: self.recipient_group_id = recipient_id
        else: self.receipient_user_id = recipient_id

    def __repr__(self):
        return '%s' % self.message