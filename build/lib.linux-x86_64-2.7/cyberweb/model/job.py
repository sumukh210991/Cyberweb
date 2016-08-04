from sqlalchemy import Column,ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy.types import Integer, String, DateTime, Boolean
from datetime import datetime

from cyberweb.model.meta import Base
from cyberweb.model.queue import QueueService
from cyberweb.model import Service,User

class JobState:
    setup = 0
    queued = 1
    running = 2
    idle = 3
    paused = 4
    finished = 5
    error = 6
    # Unused below this point
    cancelled = 7
    timeout = 8
    unknown = 9
    _states = ['setup','queued', 'running', 'idle', 'paused', 'finished', 'error', 'cancelled', 'timeout', 'unknown']
    _keys   = ['S', 'Q', 'R', 'I', 'P', 'F', 'E', 'C', 'T', 'U']
    @staticmethod
    def is_running(state): return state in [JobState.queued, JobState.running, JobState.idle]

    @staticmethod
    def is_finished(state): return state in [JobState.finished, JobState.error, JobState.cancelled, JobState.timeout]

    @staticmethod
    def get_name(state): return JobState._states[state] if state < len(JobState._states) else ''

class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer,primary_key=True,autoincrement=True)
    job_id = Column(Integer,ForeignKey("job.id"),nullable=False)
    queue_service_id = Column(Integer,ForeignKey("queueservice.id"))
    queue_job_id = Column(String(255))
    label = Column(String(255))
    type = Column(String(255))
    name = Column(String(255))
    version = Column(String(255))
    keyword = Column(String(255))
    executable = Column(String(255))
    arguments = Column(String(255))
    stdin = Column(String(255))
    stdout = Column(String(255))
    stderr = Column(String(255))
    stdstatus = Column(String(255))
    environment = Column(String(255))
    state = Column(Integer)
    owner = Column(Integer,ForeignKey("user.id"),nullable=False)
    requested_cpu = Column(Integer)
    actual_cpu = Column(Integer)
    requested_memory = Column(Integer)
    actual_memory = Column(Integer)
    estimated_walltime = Column(DateTime)
    requested_walltime = Column(DateTime)
    actual_walltime = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    pending_time = Column(DateTime)
    running_time = Column(DateTime)

    queue = relation('QueueService')
    job = relation('Job')

    def __init__(self,
                 job_id=None,
                 owner=None,
                 queueservice_id=None,
                 queuejob_id=None,
                 label=None,
                 type=None,
                 name=None,
                 version=None,
                 environment=None,
                 state=JobState.setup,
                ):
        self.job_id = job_id
        self.queueservice_id = queueservice_id
        self.queue_job_id = queuejob_id
        self.label = label
        self.type = type
        self.name = name
        self.version = version
        self.state = state
        self.owner = owner
        self.environment = environment

    def __repr__(self):
        return '%(task_id)d,%(job_id)d,%(state)d' % self.__dict__
    
    def change_state(self, state):
        self.state = state

class Job(Base):
    __tablename__ = 'job'

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(128))
    user_id = Column(Integer,ForeignKey("user.id"),nullable=False)
    service_id = Column(Integer,ForeignKey("service.id"),nullable=False)
    parent_job_id = Column(Integer)
    state = Column(Integer)
    submit_time = Column(DateTime,default=datetime.now())
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    user = relation(User)
    service = relation(Service)

    def __init__(self,
                 user_id=None,
                 service_id=None,
                 name=None,
                 parent_job_id=None,
                 submit_time=datetime.now()
                 ):
        self.user_id = user_id
        self.name = name
        self.service_id = service_id
        self.parent_job_id = parent_job_id
        self.submit_time = submit_time
        self.state = JobState.queued

    def __repr__(self):
        return self.name

################################
# File table
################################
class File(Base):
    __tablename__ = 'file'

    id = Column(Integer,primary_key=True,autoincrement=True)
    task_id = Column(Integer,ForeignKey("task.id"),nullable=False)
    service_id = Column(Integer,ForeignKey("service.id"),nullable=False)
    endpoint_ref = Column(String(255))
    size = Column(String(255))
    format = Column(String(255))
    type = Column(String(255))

    task = relation(Task)
    service = relation(Service)

    def __init__(self):
        pass
