"""Helper functions

Consists of functions available to Controllers. This module is available to templates as 'j'.
"""
from datetime import datetime
import traceback
import simplejson as json
import sqlalchemy as sa
from sqlalchemy.sql.expression import desc

from pylons import url, session, request, response  as c
from pylons import config, request, response, session, app_globals, url, tmpl_context as c

from webhelpers import html

from cyberweb import model
from cyberweb.model import meta, Job, JobState
from cyberweb.lib.base import BaseController, render
from cyberweb.lib.jodis import sshresource as myssh, resources
from cyberweb.lib import auth, Gccom, BaseJob as basejob 


import logging
log = logging.getLogger(__name__)


__all__ = ['html', 'getJobs', 'getJobHeaders', 'jobmonitor', 'jobSummary', 'getJobSateNames','getJobStateKeys']

def getJobHeaders():
    return ['ID','Name','Service','Resource','Status','Submit Time','Start Time','End Time']

def getJobStateNames():
    return JobState._states   #array of job state names

def getJobStateKeys():
    return JobState._keys   #array of job state names

def getJobs(filter, user_id, limit=None):
    jobs_array = []
    
    query = meta.Session.query(Job).filter(sa.and_(Job.state == filter, Job.user_id == user_id)).order_by(
                                                                                      desc(Job.end_time), 
                                                                                      desc(Job.start_time), 
                                                                                      desc(Job.submit_time)
                                                                                                         )
    query = query.limit(limit) if limit else query
    for i in query:
        try: service_name = i.service.service_name.name 
        except AttributeError: service_name = 'Unknown Service'
        try: resource_name = i.service.resource.name 
        except AttributeError: resource_name = 'Unknown Resource'
        jobhash = {
		           'ID':i.id,
                   'Name':     i.name,
                   'Service':  service_name,
                   'Resource': resource_name,
                   'Status':   i.state
                  }
        if i.submit_time: jobhash['Submit Time'] = i.submit_time.strftime("%m/%d/%y %H:%M:%S")
        if i.start_time: jobhash['Start Time'] = i.start_time.strftime("%m/%d/%y %H:%M:%S")
        if i.end_time: jobhash['End Time'] = i.end_time.strftime("%m/%d/%y %H:%M:%S")
        jobs_array.append(jobhash)
    return jobs_array

def jobMonitor(self,user_id,numjobs):
    '''
    Queries database for running jobs and looks for those jobs in the qstat of the respective machines. 
    This method returns a page displaying the status of recent jobs and gives the
    user the ability to refresh the page.
    '''
    jobs_array = []

    # first, update [queue] jobs, if any
    active_jobs = getJobs(JobState.running, user_id, numjobs) + getJobs(JobState.queued, user_id, numjobs)
    for i in active_jobs:
        try:
            status, _ = app_globals.jodis.statusJob(i['Name'])
            if not status:
                thisjob = meta.Session.query(model.Job).filter(model.Job.id == i['ID']).first()
                thisjob.state = JobState.finished
                thisjob.end_time = datetime.now()
                meta.Session.add(thisjob)
                meta.Session.commit()
                log.error('Job not in status menu. Probably done.')
        except Exception as _:
            log.error(traceback.format_exc())

    #log.debug('LIB_JOB_MONITOR_STAT: User[%s] Jobs array: %s ',user_id,active_jobs)

    jobkeys = getJobStateKeys()
    query = meta.Session.query(Job).filter(sa.and_(Job.state.in_( [JobState.queued, 
                                                                  JobState.running, 
                                                                  JobState.finished,
                                                                  JobState.cancelled]), 
                                                   Job.user_id == user_id)).order_by(
                                                                  desc(Job.end_time), 
                                                                  desc(Job.start_time), 
                                                                  desc(Job.submit_time)  )
    query = query.limit(numjobs)
    for i in query:
        try: service_name = i.service.service_name.name 
        except AttributeError: service_name = 'None'
        try: resource_name = i.service.resource.name 
        except AttributeError: resource_name = 'None'
	jobstatekey = jobkeys[ int(i.state) ]
        jobhash = {
                   'ID':         i.id,
                   'Name':       i.name,
                   'Service':    service_name,
                   'Resource':   resource_name,
                   'Status':     i.state,
                   'StatusKey':  jobstatekey
                  }
        if i.submit_time:
            jobhash['Submit Time'] = i.submit_time.strftime("%m/%d/%y %H:%M:%S")
        else:
            jobhash['Submit Time'] = 'None'
            
        if i.start_time: 
            jobhash['Start Time'] = i.start_time.strftime("%m/%d/%y %H:%M:%S")
        else:
            jobhash['Start Time'] = 'None'
            
        if i.end_time: 
            jobhash['End Time'] = i.end_time.strftime("%m/%d/%y %H:%M:%S")
        else:
            jobhash['End Time'] = 'None'
        jobs_array.append(jobhash)
        
        sort_on = "Name"
        jsort = [(dict_[sort_on], dict_) for dict_ in jobs_array]
        jsort.sort()
        sorted_jobs = [dict_ for (key, dict_) in jsort]
 
    return reversed(sorted_jobs)
    #return jobs_array
 
def jobSummary(self,user_id, limit):
    jobs_array = []
    jobkeys = getJobStateKeys()
    
    query = meta.Session.query(Job).filter(sa.and_(Job.state.in_( [JobState.setup, 
                                                                  JobState.queued, 
                                                                  JobState.running, 
                                                                  JobState.idle, 
                                                                  JobState.paused,
                                                                  JobState.finished,
                                                                  JobState.cancelled]), 
                                                    Job.user_id == user_id)).order_by(
                                                                  desc(Job.end_time), 
                                                                  desc(Job.start_time), 
                                                                  desc(Job.submit_time)  )
    query = query.limit(limit)
    for i in query:
        try: service_name = i.service.service_name.name 
        except AttributeError: service_name = 'None'
        try: resource_name = i.service.resource.name 
        except AttributeError: resource_name = 'None'
	jobstatekey = jobkeys[ int(i.state) ]
        jobhash = {
                   'ID':         i.id,
                   'Name':       i.name,
                   'Service':    service_name,
                   'Resource':   resource_name,
                   'Status':     i.state,
                   'StatusKey':  jobstatekey
                  }
        if i.submit_time:
            jobhash['Submit Time'] = i.submit_time.strftime("%m/%d/%y %H:%M:%S")
        else:
            jobhash['Submit Time'] = 'None'
            
        if i.start_time: 
            jobhash['Start Time'] = i.start_time.strftime("%m/%d/%y %H:%M:%S")
        else:
            jobhash['Start Time'] = 'None'
            
        if i.end_time: 
            jobhash['End Time'] = i.end_time.strftime("%m/%d/%y %H:%M:%S")
        else:
            jobhash['End Time'] = 'None'
        jobs_array.append(jobhash)

    log.debug('LIB_JOB_SUMMARY: User[%s] Jobs array: %s ',user_id,jobs_array)
    return jobs_array
