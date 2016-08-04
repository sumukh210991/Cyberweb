"""The application's model objects"""
from cyberweb.model.meta import Session, Base
from cyberweb.model.message import Message, MessageType
from cyberweb.model.user import User, Group, GroupDefinition
from cyberweb.model.resource import Resource, Protocol, AuthKey, Account
from cyberweb.model.service import ServiceName, Service, ServiceType
from cyberweb.model.job import Task, Job, JobState
from cyberweb.model.queue import QueueService, QueueInfo, QueueSystem, QueueType


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)
