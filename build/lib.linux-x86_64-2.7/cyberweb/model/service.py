from sqlalchemy import Column,ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy.types import Integer, String, DateTime, Boolean
from datetime import datetime

from cyberweb.model.meta import Base
from cyberweb.model.resource import Resource


class ServiceType(Base):
    __tablename__ = 'servicetype'
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(25),unique=True)
    description = Column(String(255))
    active = Column(Boolean,default=True)
    
    def __init__(self,name=None,description='',active=True):
        self.name = name
        self.description = description
        self.active = active
        
    def __repr__(self):
        return self.name

class ServiceName(Base):
    __tablename__ = 'servicename'
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(25))
    service_type_id = Column(Integer,ForeignKey("servicetype.id"),nullable=False)
    active = Column(Boolean,default=True)
    
    service_type = relation('ServiceType')
    
    def __init__(self,name=None,service_type_id=None,active=True):
        self.name = name
        self.service_type_id = service_type_id
        self.active = active
        
    def __repr__(self):
        return self.name or 'Service Name'


class Service(Base):
    __tablename__ = 'service'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    servicename_id = Column(Integer,ForeignKey("servicename.id"),nullable=False)
    protocol_id = Column(Integer,ForeignKey("protocol.id"),nullable=False)
    resource_id = Column(Integer,ForeignKey("resource.id"),nullable=False)
    path = Column(String(255))
    command = Column(String(255))
    port = Column(Integer)
    active = Column(Boolean,default=True)
    timestamp = Column(DateTime,default=datetime.now())
    
    service_name = relation('ServiceName')
    protocol = relation('Protocol')
    resource = relation('Resource')
    
    def __init__(self,
                 service_name_id=None,
                 protocol_id=None,
                 resource_id=None,
                 path=None,
                 command=None,
                 port=None,
                 active=True
                ):
        self.servicename_id = service_name_id
        self.protocol_id = protocol_id
        self.resource_id = resource_id
        self.path = path
        self.command = command
        self.port = port
        self.active = active
        
    def __repr__(self):
        if self.port:
            return '%s/%s:%d' % (self.path,self.command,self.port)
        else:
            return '%s/%s' % (self.path,self.command)