import logging
import os
import sys
import traceback
import commands

# add authentication to control who can access this class.
from authkit.permissions import ValidAuthKitUser
from authkit.authorize.pylons_adaptors import authorize

from pylons import config, request, response, session, app_globals, url, tmpl_context as c
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
import simplejson as json

from cyberweb.lib.base import BaseController, render
from cyberweb.lib.base import BaseController, render
from cyberweb.lib.jodis import sshresource as myssh,resources
from cyberweb.lib.jodis.base import Jodis, JodisJob, JodisTask
from cyberweb.lib import auth, Gcom, BaseJob, helpers as h
from cyberweb.model import meta, Service, JobState
from cyberweb.lib.menu import MenuReader 

log = logging.getLogger(__name__)

class BasicjobsController(BaseController):

    @authorize(auth.is_valid_user)
    def __before__(self, action, **params):
        pass

    def index(self):
        return 'Basic Job Controller'
        #return render('/demos/demos.mako')

    def cmd(self):
        # Return a rendered template
        c.cwuser = session.get('user', 'cwguest')
        return render('/demos/demo_cmd.mako')

    def getmenu(self):
        # Return a rendered template
        c.cwuser = session.get('user', 'cwguest')
        c.state = 'GetMenu:  OK'
        c.menu = "menu"
        c.jsonmenu = MenuReader.get_jsonmenu()
        return render('/demos/getmenu.mako')

    def basicjob(self):
        '''
        Demonstrates how to create a basic job and see list of jobs
        Uses the BaseJob class to create a Job that will execute simple Unix commands on a remote host
        Uses raw Jodis command to run the job via passwordless SSH
        Returns  STIO
        '''
        c.hostname = request.params.get('hostname')
        c.command = request.params.get('command')
        c.cwuser = session['user']
        jobname = "BaseJob Test"
        if not c.hostname and not c.command:
            c.state = False
        else:
            try:
                myjob = BaseJob()
                (c.jobid, c.jobname) = myjob.create(c.command,jobname)
                myjob.load(c.jobid)
                myjob.start()
                c.status, c.output = commands.getstatusoutput(c.command)
                c.results = c.output.splitlines()
            except Exception as e:
                c.results = e.message
            c.state = True
        #newline = re.compile('\n+')
        #c.results = newline.sub('||',output)
        #c.status = status
        #c.script = script
        #c.cwuser = session['user']
        #myjob.finish()
        # Return a rendered template

        # list the current machines that are up and have ssh available to jodis and the commands
        c.resources = app_globals.available_resources.keys()
        c.command_options = [('date','Date'),('ls -1','List dir'),('hostname','Hostname'),('uptime','Uptime'),('whoami','WhoAmI')]
        return render('/demos/demo_basicjob.mako')


    ################################################################################
    ###  Execution Services:  Run jobs using JODIS +  passwordless SSH  (local scripts)
    ################################################################################
    def cmd_ssh(self):
        c.hostname = request.params.get('hostname')
        c.command = request.params.get('command')
        c.cwuser = session['user']
        jobaction = request.params.get('job') or ''
        if not c.hostname and not c.command:
            c.state = False
        else:
            try:
                output,error = app_globals.jodis.manager.getResource(c.hostname).raw(c.command)
                c.results = output.splitlines()
            except Exception as e:
                c.results = e.message
            c.state = True

        # list the current machines that are up and have ssh available to jodis and the commands
        c.resources = app_globals.available_resources.keys()
        c.command_options = [('date','Date'),('ls -1','List dir'),('hostname','Hostname'),('uptime','Uptime'),('whoami','WhoAmI')]
        return render('/demos/demo_cmd_ssh.mako')

    def cmd_gsissh(self):
        c.hostname = request.params.get('hostname')
        c.command = request.params.get('command')
        c.cwuser = session['user']
        if not c.hostname and not c.command:
            c.state = False
        else:
            try:
                output,error = app_globals.jodis.manager.getResource(c.hostname).raw(c.command)
                c.results = output.splitlines()
            except Exception as e:
                c.results = e.message
            c.state = True

        # list the current machines that are up and have ssh available to jodis and the commands
        c.resources = app_globals.available_resources.keys()
        c.command_options = [('date','Date'),('ls -1','List dir'),('hostname','Hostname'),('uptime','Uptime'),('whoami','WhoAmI')]
        return render('/demos/demo_cmd_gsissh.mako')

    def batch(self):
        c.hostname = request.params.get('hostname')
        c.command = request.params.get('command')
        c.cwuser = session['user']
        if not c.hostname and not c.command:
            c.state = False
        else:
            try:
                output,error = app_globals.jodis.manager.getResource(c.hostname).raw(c.command)
                c.results = output.splitlines()
            except Exception as e:
                c.results = e.message
            c.state = True

        # list the current machines that are up and have ssh available to jodis and the commands
        c.resources = app_globals.available_resources.keys()
        c.command_options = [('date','Date'),('ls -1','List dir'),('hostname','Hostname'),('uptime','Uptime'),('whoami','WhoAmI')]
        return render('/demos/demo_batch.mako')

    def jodis(self):
        jobaction = request.params.get('job') or ''
        taskaction = request.params.get('task') or ''
        service_id = request.params.get('service') or ''
        jodis = app_globals.jodis

        # Deal with job action param
        if jobaction == 'add':
            c.job = jodis.createJob(service_id, session['user_id'])
            c.jobname = c.job.name
            c.result = 'Added job (%s): %s' % (c.job.id, c.job.name)
            log.debug(c.result)
        else:
            c.jobname = jobaction
            c.job = jodis.getJob(c.jobname)

        try: c.service_id = c.job.service.id
        except AttributeError: c.service_id = None

        # Deal with task action param
        if taskaction == 'add':
            task = c.job.addTask()
            if task:
                c.result = 'Added task (%s): %s' % (task.id, task.status)
                log.debug(c.result)
        elif taskaction == 'run':
            if c.job.listTasks():
                jodis.submitJob(c.job.name)
            else:
                c.result = 'Added task (%s): %s' % (task.id, task.status)
                log.debug(c.result)
        elif taskaction == 'monitor':
            pass
        
        try: c.monitor = jodis.statusJob(c.job.name)[1]
        except AttributeError:
            c.monitor = {}
            log.debug(traceback.format_exc())
        log.debug('c.monitor: %s', c.monitor)
        
        if c.job:
            c.current_tasks = c.job.listTasks()
        c.current_jobs = jodis.listJobs()
        c.services = meta.Session.query(Service)
        return render('/demos/jodis.mako')
