import logging
import os
import traceback

from datetime import datetime
from time import strftime

from pylons import config, request, response, session, app_globals, url, tmpl_context as c
from pylons.controllers.util import abort, redirect

import sqlalchemy as sa
from authkit.authorize.pylons_adaptors import authorize

from cyberweb import model
from cyberweb.model import meta, JobState, AuthKey, Resource, Account, Service
from cyberweb.lib.base import BaseController, render
from cyberweb.lib.jodis import sshresource as myssh, resources
from cyberweb.lib import auth, helpers as h, jobs as j, Gccom

log = logging.getLogger(__name__)

class GcemController(BaseController):

    @authorize(auth.is_valid_user)
    def __before__(self, action, **params):
        pass

    def __init__(self):
        super(self.__class__, self).__init__()
        try:
            self.servicename_id = meta.Session.query(model.ServiceName).filter(model.ServiceName.name == 'GCOM').first().id
        except Exception as _:
            self.servicename_id = 0

    def index(self):
        return self.gcem()

    def gcem(self):
        user_id = session.get('user_id')
        c.title = 'GCEM Project:' + ' Recent Job Summary for:  ' + session['user']
        numJobs = 10
        c.jobheaders   = j.getJobHeaders()
        c.jobs         = j.jobMonitor(self,session.get('user_id'),numJobs)
        c.jobstates    = j.getJobStateNames()
        c.jobstatekeys = j.getJobStateKeys()
        d=dict()
        for i in range(len( c.jobstatekeys )):
             d[c.jobstatekeys[i]]= c.jobstates[i]
        c.jobstateheaders = d
        return render('/gcem/gcem.mako')

    def gcem_create(self):
        user_id = session.get('user_id')
        c.title = 'GCEM Project: Create New/Modify Existing Simulations'
        return render('/gcem/gcem_create.mako')

    def gcem_monitor(self):
        user_id = session.get('user_id')
        c.title = 'GCEM Project: Monitor Simulations'
        return render('/gcem/gcem_monitor.mako')

    def jobmonitor(self):
        user_id = session.get('user_id')
        c.title = 'GCEM Project: Monitor Simulations'
        return render('/gccom/jobmonitor.mako')

    def jobsummary(self):
        user_id = session.get('user_id')
        c.title = 'GCEM Project: Monitor Simulations'
        return render('/gccom/jobsummary.mako')

    def gcem_sim_details(self):
        user_id = session.get('user_id')
        c.title = 'GCEM Project: Simulation Job Details'
        return render('/gcem/gcem_sim_details.mako')

    def gcem_analyze(self):
        user_id = session.get('user_id')
        c.title = 'GCEM Project: Analyze Simulations'
        return render('/gcem/gcem_analyze.mako')

    def gcem_exec(self):
        user_id = session.get('user_id')
        c.title = 'GCEM Project: Submit and Execute Simulations'
        return render('/gcem/gcem_exec.mako')


