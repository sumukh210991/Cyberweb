'''
This base class of Jodis holds basic data models used by jodis.
.. moduleauthor:: Carny Cheng <carny@me.com>
'''
import logging
import traceback
import os
from pylons import config, session, app_globals

from cyberweb.lib import BaseJob
from cyberweb.model import meta, JobState, Resource, QueueService, Task, Service, Job
from cyberweb.lib.jodis.resource_manager import Manager

log = logging.getLogger(__name__)


class JodisError(Exception):
    pass


class JodisJob:
    '''
    The Jodis Job represents a group of jobs. The underlying jobs (or tasks) can be associated
    with a queue or running job, but this layer simply aggregates the group and bundles
    the tasks that you might use to operate on the lower level.
    '''

    def __init__(self, service_id, owner_id, jobname=None, working_dir=None):
        '''
        Creates a new Jodis Job with a unique job name if it is not provided.

        Args:
            service_id (int): ID of the service in the database
            owner_id (int): ID of the owner requesting the job
            jobname (str): Job name (optional)
            working_dir (str): Path to the working directory (optional)
        '''
        self._jobstate = BaseJob()
        self._tasks = []
        self._owner_id = owner_id
        self._service = meta.Session.query(Service).get(service_id)
        self._id, self._name = self._jobstate.create(service_id, jobname)
        self.jobdir = working_dir if working_dir else self._name
        if not self._service:
            raise JodisError

    def addTask(self, account_id, submitfile='', taskname=None, queuename='', queueservice_id=None):
        '''
        Creates a new task for this particular JodisJob

        Args:
            submitfile (str): Submit file for the task
            taskname (str): Name of the task. One will be dynamically created if not supplied (optional)
            queuename (str): Name of the queue to sumibt this job
            queueservice_id (int): ID of the queue to submit this job
        '''
        submitfile = submitfile or os.path.join(self._service.path, self._service.command)
        try: resourcename = self._service.resource.name
        except AttributeError as _: print "failed getting resource name"
        try:
            t = JodisTask(int(self._jobstate.id), self.owner_id, submitfile, account_id, \
                      taskname, resourcename, queuename, queueservice_id)
            self._tasks.append(t)
        except TypeError as _: traceback.print_exc()

        return t

    def listTasks(self): return [int(i.id) for i in self._tasks]
    def countTasks(self): return len(self._tasks)
    def getTask(self, task_id):
        for i in self._tasks:
            if task_id == int(i.id):
                return i
        return None

    def start(self): return self._jobstate.start()
    def error(self): return self._jobstate.error()
    def queued(self): return self._jobstate.queued()
    def finished(self): return self._jobstate.finish()

    @property
    def state(self): return JobState.get_name(self._jobstate.state)

    @property
    def id(self): return self._jobstate.id

    @property
    def name(self): return self._name

    @property
    def owner_id(self):
        print 'OWNER_ID', self._owner_id
        return self._owner_id

    @property
    def service(self): return self._service


class JodisTask:
    '''
    This class represents a task for Jodis. A job is defined by
    multiple tasks
    '''

    def __init__(self,
                 jobid,
                 owner_id,
                 submitfile,
                 account_id,
                 taskname=None,
                 resourcename='',
                 queuename='',
                 queueservice_id=None
                ):

        self._submitfile = submitfile
        self.account_id = account_id
        self._task = None
        self.submitted = []

        # Look up queueservice_id
        if queueservice_id is None:
            print jobid, owner_id, submitfile, taskname, resourcename
            self._resource = meta.Session.query(Resource).filter(Resource.name == resourcename).first()

            if not self._resource:
                log.error('Resource %s could not be found. Couldn\'t create task for job %s', resourcename, jobid)
                return

            log.debug('Got resource (id %d): %s', self._resource.id, resourcename)
            self._queue = meta.Session.query(QueueService).filter(QueueService.resource_id == self._resource.id).first()

            if not self._queue:
                log.error('Queue could not be found. Couldn\'t create task for job %d', int(jobid))
                return

            queueservice_id = self._queue.id

        # Initialize task in database
        self._task = Task(jobid, owner_id, queueservice_id)
        try:
            meta.Session.add(self._task)
            meta.Session.commit()
        except Exception:
            log.error('Couldn\'t create task for job %d', int(jobid))
            meta.Session.rollback()
            meta.Session.flush()

    @property
    def id(self):
        return self._task.id if self._task else 0

    @property
    def status(self):
        try: return JobState.get_name(self._task.state)
        except Exception as _: return None

    @property
    def submitinfo(self):
        return {'account_id': self.account_id, 'resource' : self._resource.name, 'submitfile' : self._submitfile}

    def append_submitted(self, submittedjobs):
        if isinstance(submittedjobs, list) or isinstance(submittedjobs, tuple):
            self.submitted.extend(submittedjobs)
        else:
            self.submitted.append(submittedjobs)

    def setup(self): return self._change_state(JobState.setup)
    def error(self): return self._change_state(JobState.error)
    def queued(self): return self._change_state(JobState.queued)
    def running(self): return self._change_state(JobState.running)
    def finished(self): return self._change_state(JobState.finished)
    def complete(self): return self.finished()

    def _change_state(self, state):
        self._task.change_state(JobState.setup)
        try:
            meta.Session.add(self._task)
            meta.Session.commit()
        except:
            log.error('Couldn\'t update task status (id %d)', self.id)
            meta.Session.rollback()
            meta.Session.flush()


class Jodis:
    '''
    This class is the singleton that manages all of the connections and the jobs in
    Jodis. CyberWeb (Pylons) and various other web services will all plug into a singleton
    of this class. Jobs are managed by a class which are further broken down into tasks.
    Tasks are the smallest atomic piece inside a Jodis job.
    '''

    def __init__(self, manager=None, config={}):
        self.manager = manager or Manager()
        self.config = config
        self._jobstates = {}

    def createJob(self, service_id, owner_id, name=None):
        j = JodisJob(service_id, owner_id, name)
        self._jobstates[j.name] = j
        return j

    def getJob(self, name):
        return self._jobstates.get(name)

    def listJobs(self):
        return self._jobstates.keys()

    def countJobs(self):
        return len(self._jobstates.keys())

    #mpt#def submitJob(self, jobid):
    #mpt#    job = self._jobstates.get(jobid, None)
    def submitJob(self, jobname):
        job = self._jobstates.get(jobname, None)

        if not job:
            #mpt#log.error('Job %s does not exist for submit.', jobid)
            log.error('Job %s does not exist for submit.', jobname)
            return False
        if not job.countTasks():
            #mpt#log.error('Job %s does not have anything to do!', jobid)
            log.error('Job %s does not have anything to do!', jobname)
            return False

        for i in job.listTasks():
            task = job.getTask(i)
            h = task.submitinfo
            if not h:
                log.error('Cannot submit task %d from job %s', task.id, job.name)
                continue

            try:
                resource = self.manager.getResource(h['account_id'])
            except Exception as e:
                log.error('Something is wrong with self.manager. %s', e)
                task.error()
                return False
            else:
                task.queued()

            # Continue submitting job
            retVal, joblist, output = resource.submitJob(app=h['submitfile'])
            task.append_submitted(joblist)
        job.queued()
        return True

    def statusJob(self, jobname):
        job = self._jobstates.get(jobname, None)

        if not job:
            log.error('Job %s is not in memory.', jobname)
            db_job = meta.Session.query(Job).filter(Job.name == jobname).first()
            if not db_job:
                log.error('Job %s does not exist in db!', jobname)
                return False, {}
            return self._in_db_statusJob(db_job)
        if not job.countTasks():
            log.error('Job %s does not have anything to do!', jobname)
            return False, {}
        return self._in_memory_statusJob(job)

    def _in_db_statusJob(self, job):
        tasks = meta.Session.query(Task).filter(Task.job_id == job.id)
        if not tasks.count():
            log.error('Job %s does not have anything to do!', job.name)
            return False, {}

        job_states = {}
        hosts = {}
        for task in tasks:
            task_resource = task.job.service.resource
            for acc_id, resource in app_globals.user_resources(session.get('user_id')).items():
                if resource['name'] == task_resource.name:
                    account_id = acc_id
                    break
            else:
                account_id = None
                log.error('User has no access to', task_resource.name)
            try:
                resource = self.manager.getResource(account_id)
                if not resource: raise Exception
                hosts[account_id] = resource
            except Exception as _:
                log.error('Could not get retrieve connection to %s', account_id)
                log.error(traceback.format_exc())
        for hostname, resource in hosts.items():
            log.debug('Tracking jobs on %s %s', resource.name, resource.getStatus())
            try:
                states = resource.getStatus()[1].items()
            except AttributeError:
                log.debug(traceback.format_exc())
                states = []

        for submitted, status in states:
            for task in tasks:
                if submitted in task.account_id:
                    if status == 'C': task.finished()
                    elif status == 'R': task.running()
                    elif status == 'Q': task.queued()
                    else: print 'Unknown code:', status
                    job_states.setdefault(task.id, []).append((submitted, status))
        return bool(job_states), job_states

    def _in_memory_statusJob(self, job):
        hosts = {}
        job_states = {}
        for i in job.listTasks():
            task = job.getTask(i)
            hostname = task.submitinfo.get('resource')
            if hostname and not hosts.has_key(hostname):
                try: hosts[hostname] = self.manager.getResource(hostname)
                except Exception:
                    log.error('Could not get retrieve connection to %s', hostname)
                    log.error(traceback.format_exc())
        for hostname, resource in hosts.items():
            log.debug('Tracking jobs on %s %s', hostname, resource.getStatus())
            try:
                states = resource.getStatus()[1].items()
            except AttributeError:
                log.debug(traceback.format_exc())
                states = []
        for submitted, status in states:
            for taskname in job.listTasks():
                task = job.getTask(taskname)
                if submitted in task.submitted:
                    if status == 'C': task.finished()
                    elif status == 'R': task.running()
                    elif status == 'Q': task.queued()
                    else: print 'Unknown code:', status
                    job_states.setdefault(task.id, []).append((submitted, status))
        return True, job_states
