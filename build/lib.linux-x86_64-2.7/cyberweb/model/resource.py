from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy.types import Integer, String, DateTime, Boolean
from datetime import datetime

from cyberweb.model import meta
from cyberweb.model.meta import Base


class Resource(Base):
    __tablename__ = 'resource'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    hostname = Column(String(100))
    institution = Column(String(50))
    total_memory_gb = Column(Integer)
    num_cpus = Column(Integer)
    memory_per_cpu_gb = Column(Integer)
    num_nodes = Column(Integer)
    path = Column(String(255))
    queue = Column(String(24))
    active = Column(Boolean, default=True)
    insert_date = Column(DateTime, default=datetime.now())

    def __init__(self,
                name=None,
                hostname=None,
                institution='',
                total_memory_gb=None,
                num_cpus=None,
                memory_per_cpu_gb=None,
                num_nodes=None,
                path=None,
                queue=None,
                active=True
                 ):

        self.name = name
        self.hostname = hostname
        self.institution = institution
        self.total_memory_gb = total_memory_gb
        self.num_cpus = num_cpus
        self.memory_per_cpu_gb = memory_per_cpu_gb
        self.num_nodes = num_nodes
        self.path = path
        self.queue = queue
        self.active = active

    def __repr__(self):
        return self.name or 'Resource'


class Protocol(Base):
    __tablename__ = 'protocol'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), unique=True)
    description = Column(String(255))
    active = Column(Boolean, default=True)

    def __init__(self, name=None, description='', active=True):
        self.name = name
        self.description = description
        self.active = active

    def __repr__(self):
        return self.name or 'Protocol'


class AuthKey(Base):
    ''' 
    Stores the path of the private and public keys for authentication. Users may store either
    relative or absoluate paths.
    '''
    __tablename__ = 'authkey'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    private_key = Column(String(1024))
    public_key = Column(String(1024))
    active = Column(Boolean, default=True)

    user =  relation('User', backref=backref('keys', order_by=id))

    def __init__(self, private_key=None, public_key=None, user_id=None, active=True):
        self.private_key = private_key
        self.public_key = public_key
        self.user_id = user_id
        self.active = active

    def __repr__(self):
        return '%d' % self.id


class Account(Base):
    '''
    The account table stores the user information for remote resources. Users may access these
    resources via public/private key or gsissh. The accounts can be either for an individual or a group, but not both
    The table has both for foreign key mapping.
    '''
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(255))
    username = Column(String(25))
    password = Column(String(25), nullable=True)
    authkey_id = Column(Integer, ForeignKey("authkey.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    group_id = Column(Integer, ForeignKey('user_group.id'), nullable=True)
    resource_id = Column(Integer, ForeignKey("resource.id"), nullable=False)
    default_servicename_id = Column(Integer, ForeignKey("servicename.id"), nullable=True)
    service_id = Column(Integer, ForeignKey("service.id"), nullable=True)
    base_directory = Column(String(255))
    active = Column(Boolean, default=True)
    insert_date = Column(DateTime, default=datetime.now())

    user = relation('User')
    group = relation('Group')
    resource = relation('Resource')
    service_name = relation('ServiceName')
    authkey = relation('AuthKey')
    service = relation('Service')

    def __init__(self,
                 name=None,
                 username=None,
                 resource_id=None,
                 password=None,
                 authkey_id=None,
                 user_id=None,
                 group_id=None,
                 default_servicename_id=None,
                 service_id=None,
                 description='',
                 active=True
                 ):
        self.name = name
        self.username = username
        self.resource_id = resource_id
        self.password = password
        self.authkey_id = authkey_id
        self.user_id = user_id
        self.group_id = group_id
        self.description = description
        #self.default_servicename_id = default_servicename_id
        self.service_id = service_id
        self.active = active
        self.insert_date = datetime.now()

    def __repr__(self):
        return '%d %s' % (self.id, self.name)
