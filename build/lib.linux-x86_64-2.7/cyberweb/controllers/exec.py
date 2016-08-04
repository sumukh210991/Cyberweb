import logging
import os, sys, time, re, getopt, getpass
import traceback,commands
import string
from time import strftime
import pexpect

from pylons import config, request, response, session, app_globals, url, tmpl_context as c

# add authentication to control who can access this class.
from authkit.permissions import ValidAuthKitUser
from authkit.authorize.pylons_adaptors import authorize

from cyberweb.lib.base import BaseController, render
from cyberweb.lib import auth, Gccom, helpers as h, jobs as j
from cyberweb.model import meta, JobState


log = logging.getLogger(__name__)
class ExecController(BaseController):

    @authorize(auth.is_valid_user)
    def __before__(self, action, **params):
        pass

    def index(self):
        # build a job summary table:
        c.title = 'CyberWeb Demo Portal:  ' + ' Job Summary for:  ' + session['user']

        user_id = session['user_id']
        num_jobs = 4
        # Populate jobs
        c.jobs2 = dict()
        c.jobs2['Queued']   = j.getJobs(JobState.queued,user_id,num_jobs)
        c.jobs2['Running']  = j.getJobs(JobState.running,user_id,num_jobs)
        c.jobs2['Finished'] = j.getJobs(JobState.finished,user_id,num_jobs)
        c.jobs2['Crashed']  = j.getJobs(JobState.error,user_id,num_jobs)
        c.jobheaders        = j.getJobHeaders()
        numJobs = 10
        c.jobs         = j.jobMonitor(self,session.get('user_id'),numJobs)
        c.jobstates    = j.getJobStateNames()
        c.jobstatekeys = j.getJobStateKeys()
        d=dict()
        for i in range(len( c.jobstatekeys )):
             d[c.jobstatekeys[i]]= c.jobstates[i]
        c.jobstateheaders = d

        return render('/exec/exec.mako')


    def jobsummary(self):
        numJobs = 10
        c.user         = session.get('user_id')
        c.title        = config.get('project.shortname','CyberWeb') + ' Job Summary for:  ' + session['user']
        c.jobname      = 'jobname'
        c.jobs         = j.jobSummary(self,session.get('user_id'),numJobs)
        c.jobstates    = j.getJobStateNames()
        c.jobstatekeys = j.getJobStateKeys()
        d=dict()
        for i in range(len( c.jobstatekeys )):
             d[c.jobstatekeys[i]]= c.jobstates[i]
        c.jobstateheaders = d
        c.title = config.get('project.shortname','CyberWeb') + ' Job Monitor Listing for:  ' + session['user']
        #log.debug('GCOMJOBSUMMARY: finished jobs:%s', str(c.jobs))
        return render('/exec/jobsummary.mako')

    def jobmonitor(self):
        numjobs = 20
        c.user  = session.get('user_id')
        c.jobname = request.params.get('jobname') or ''
        c.jobs  = j.jobMonitor(self,session.get('user_id'),numjobs)
        c.jobstates    = j.getJobStateNames()
        c.jobstatekeys = j.getJobStateKeys()
        d=dict()
        for i in range(len( c.jobstatekeys )):
             d[c.jobstatekeys[i]]= c.jobstates[i]
        c.jobstateheaders = d
        c.title = config.get('project.shortname','CyberWeb') + ' Job Monitor Listing for:  ' + session['user']
        #log.debug('GCOMJOBMONITOR: finished jobs:%s', str(c.jobs))
        return render('/exec/jobmonitor.mako')

