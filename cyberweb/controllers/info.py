import logging
from pylons import config, request, response, session, app_globals, url, tmpl_context as c
from pylons.controllers.util import redirect
from authkit.authorize.pylons_adaptors import authorize

from cyberweb.lib.base import BaseController, render
from cyberweb.lib import auth, helpers as h
from cyberweb.model import JobState

log = logging.getLogger(__name__)


class InfoController(BaseController):

    @authorize(auth.is_valid_user)
    def __before__(self, action, **params):
        pass

    def index(self):
        return self._jobsummary()

    def services(self):
        redirect('/user/resources')

    def gpir(self):
        return render('/info/teragrid_status.mako')

    def jobs(self):
        return render('/info/info.mako')

    def jobsummary(self):
        redirect('/info/')

    def _jobsummary(self):
        # build a job summary table:
        user_id = session.get('user_id')
        c.title = config.get('project.shortname','CyberWeb') + ' Job Summary for:  ' + session['user']

        # Recent jobs
        num_jobs = 6
        c.jobs = dict()
        c.jobs['Queued'] = h.getJobs(JobState.queued,user_id,num_jobs)
        c.jobs['Running'] = h.getJobs(JobState.running,user_id,num_jobs)
        c.jobs['Finished'] = h.getJobs(JobState.finished,user_id,num_jobs)
        c.jobs['Crashed'] = h.getJobs(JobState.error,user_id,num_jobs)
        c.jobheaders = h.getJobHeaders()
        
        return render('/info/jobsummary.mako')

