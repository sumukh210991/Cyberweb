'''
The base Controller API
Provides the BaseController class for subclassing.

    @author: carny
'''

import logging

from datetime import datetime
import time

from pylons import session

from cyberweb import model
from cyberweb.model import JobState
from cyberweb.model.meta import Session


log = logging.getLogger(__name__)


class BaseJob:
    '''
    The base jobs wraps the Job model and JobState. It is kept separate from the models because...
    @todo: fill in more of the docs
    '''

    def __init__(self):
        self._username = session.get('user')
        if not self._username:
            log.critical('Non-user wants to run a job. This should not be allowed.')
            raise

        try: self._user = Session.query(model.User).filter(model.User.username == self._username).one()
        except Exception as _:
            log.critical('User does not exist.')
            raise

    def _createname(self, name=None):
        idpart = '_%s' % self.id if self.id else ''
        name = '_%s' % name if name else ''
        return ''.join([time.strftime('%Y%m%d_%H%M%S'), name, idpart])

    def create(self, service_id, name=None, parent=None):
        '''
        method creates a job in the database and returns its id and name
        '''
        self._job = model.Job(self._user.id, service_id, name, parent)
        self._job.name = ''
        self._job.state = JobState.setup
        # Save job to get ID
        try:
            Session.add(self._job)
            Session.commit()
        except Exception as _:
            log.warn('Couldn\'t commit job')
            Session.rollback()
            return None, None

        # Save job name
        self._job.name = self._createname(name)
        try:
            Session.add(self._job)
            Session.commit()
        except Exception as _:
            log.warn('Couldn\'t commit job')
        return self.id, self._job.name

    def load(self, idStr):
        try:
            id = int(idStr)
        except Exception:
            log.error('Invalid id %s', idStr)
            return None

        try: jobs = Session.query(model.Job).filter(model.Job.id == id)
        except Exception as _: pass

        if not jobs.count() == 1:
            log.error('No jobs found with id: %d', id)
            return None

        self._job = jobs.one()
        self._state = self._job.state

    def __repr__(self):
        if self._job.id:
            return '%06d' % self._job.id
        else:
            return ''

    ###
    # Getter functions (readonly)
    ###
    @property
    def state(self):
        try: return self._job._state
        except AttributeError as _: pass

        return JobState.unknown

    @property
    def statename(self):
        return JobState.get_name(self.state)

    @property
    def id(self):
        try: return '%06d' % self._job.id
        except Exception as _: pass

        return None

    @property
    def userid(self):
        return self._user.id

    @property
    def name(self):
        return self._job.name

    ###
    # Functions to change state
    ###
    def queued(self):
        self._change_state(JobState.queued)

    def start(self):
        if JobState.is_finished(self._state):
            log.warn('Job %s wants to go from finished state to running. Start a new job.' % self)
        self._change_state(JobState.running)

    def finish(self):
        self._change_state(JobState.finished)
        log.debug('TODO: Move job to job history table.')

    def error(self):
        self._change_state(JobState.error)

    def _change_state(self, state):
        if self._job.state == state:
            log.debug('Job %s already in this state. Do nothing' % self)
            return

        if state == JobState.running:
            self._job.start_time = datetime.now()
        elif state == JobState.finished or state == JobState.error:
            self._job.end_time = datetime.now()

        try:
            self._job.state = state
            Session.add(self._job)
            Session.commit()
        except:
            log.warn('Couldn\'t commit job')
        else:
            self._state = state
            log.debug('Job %s changed state.' % self)
