from sqlalchemy import Column,ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy.types import Integer, String, DateTime, Boolean
from datetime import datetime

from cyberweb.model.meta import Base
from cyberweb.model.resource import Resource


################################
# Queue Info table
################################
class QueueInfo(Base):
    __tablename__ = 'queueinfo'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(255))
    no = Column(Integer)
    policy = Column(String(255))
    max_walltime = Column(Integer)
    max_jobs = Column(Integer)
    max_CPUsPerJob = Column(Integer)
    avg_waittime = Column(Integer)
    num_nodes = Column(Integer)
    cpus_per_node = Column(Integer)
    parameters = Column(String(255))
    active = Column(Boolean,default=True)
    timestamp = Column(DateTime,default=datetime.now())

    def __init__(self):
        pass
    
    def __repr__(self):
        return self.name or 'Queue Info'

################################
# Queue Type table
################################
class QueueType(Base):
    __tablename__ = 'queuetype'

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(25),unique=True)
    description = Column(String(255))
    active = Column(Boolean,default=True)
    
    def __init__(self):
        pass
    
    def __repr__(self):
        return self.name

################################
# Queue System table
################################
class QueueSystem(Base):
    __tablename__ = 'queuesystem'

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(25))
    queuetype_id = Column(Integer,ForeignKey("queuetype.id"),nullable=False)
    path = Column(String(100))
    submit = Column(String(25))
    delete = Column(String(25))
    status = Column(String(25))
    other1 = Column(String(25))
    other2 = Column(String(25))
    active = Column(Boolean,default=True)
    
    queuetype = relation(QueueType)

    def __init__(self):
        pass
    
    def __repr__(self):
        return self.name or 'Queue System'

################################
# Queueing Service table
################################
class QueueService(Base):
    __tablename__ = 'queueservice'

    id             = Column(Integer,primary_key=True,autoincrement=True)
    queuesystem_id = Column(Integer,ForeignKey("queuesystem.id"),nullable=False)
    queueinfo_id   = Column(Integer,ForeignKey("queueinfo.id"),nullable=False)
    resource_id    = Column(Integer,ForeignKey("resource.id"),nullable=False)
    bin_dir        = Column(String(1024))
    arg_string     = Column(String(1024))
    active = Column(Boolean,default=True)
    
    queuesystem = relation(QueueSystem)
    queueinfo = relation(QueueInfo)
    resource = relation(Resource)
    
    def __init__(self):
        pass

    def __repr__(self):
        return self.queueinfo.name