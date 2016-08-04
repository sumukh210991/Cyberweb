import logging

import os
import commands
from hashlib import md5
import simplejson as json

import sqlalchemy as sa
from pylons import config, request, response, session, app_globals, tmpl_context as c
from pylons.controllers.util import abort, redirect
from webhelpers.paginate import Page

# add authentication to control who can access this class.
from authkit.authorize.pylons_adaptors import authorize, authorized

from cyberweb import model
from cyberweb.lib.base import BaseController, render
from cyberweb.lib import auth, Gccom, BaseJob, jobs as j
from cyberweb.model import meta, JobState, Account


log = logging.getLogger(__name__)

####CWPROJPATH = config.get('cw.cwuser_loc')
CWPROJPATH = config.get('cw.cwuser_rem')
SESS_KEY = 'filebrowser_data'


class DataController(BaseController):
    @authorize(auth.is_valid_user)
    def __before__(self, mako='/data/data.mako'):
        self.mako = mako
        session['available_resources'] = app_globals.user_resources(session.get('user_id'))
        session.save()

    def __init__(self):
        super(self.__class__, self).__init__()
        if SESS_KEY not in session:
            session[SESS_KEY] = {'left': {}, 'right': {}, 'viz': {}}
            session[SESS_KEY]['viz']['jobname'] = ''
            session[SESS_KEY]['viz']['jobid'] = ''
            session[SESS_KEY]['viz']['jobdir'] = ''
            session[SESS_KEY]['viz']['outputdir'] = ''
            session[SESS_KEY]['viz']['start_time'] = 0
            session[SESS_KEY]['viz']['stop_time'] = 10
            session[SESS_KEY]['viz']['vscale'] = 0.1
            session[SESS_KEY]['viz']['vnlines'] = 25
            session[SESS_KEY]['viz']['vscale'] = 0.1

            session[SESS_KEY]['viz']['grid_name'] = ''
            session[SESS_KEY]['viz']['grid_imax'] = ''
            session[SESS_KEY]['viz']['grid_jmax'] = ''
            session[SESS_KEY]['viz']['grid_kmax'] = ''
            session[SESS_KEY]['viz']['plot_jobid'] = ''
            session[SESS_KEY]['viz']['plot_jobname'] = ''

            session.save()

    def index(self):
        # Pull CGI params
        box = request.params.get('box')
        path = request.params.get('path')
        account_id = int(request.params.get('host') or 0)

        if account_id and box:
            if 'host' not in session[SESS_KEY][box] or session[SESS_KEY][box]['host'] != account_id:
                path = None

            session[SESS_KEY][box]['host'] = account_id
            session[SESS_KEY][box]['path'] = path
            session.save()
            return self._updatelisting(box)

        c.data = session[SESS_KEY]
        return render(self.mako)

    def upload(self):
        if 'datafile' in request.params:
            myfile = request.params.get('datafile')

            # Store file in user directory on Longboard
            source_dir = config.get('cw.cwdata_loc')
            source = os.path.join(source_dir, myfile.filename)
            ###target = os.path.sep.join([config.get('cw.cwproj_loc'), session.get('user', 'guest')])
            target = os.path.sep.join([config.get('cw.cwproj_rem'), session.get('user', 'guest')])
            file_contents = ''
            for i in myfile.file:
                file_contents += i
            if myfile.type.find('text') > -1:
                try:
                    fh = open(source, 'w')
                    fh.write(file_contents)
                    fh.close()
                except Exception as _:
                    log.error('Cannot write file to disk.')
            else:
                try:
                    fh = open(source, 'wb')
                    fh.write(file_contents)
                    fh.close()
                except Exception:
                    log.error('Cannot write file to disk.')
            host = config.get('cw.arch_host', 'longboard.acel')
            resource = app_globals.jodis.manager.getResource(host)
            resource.ssh.scp(None, None, source, resource.ssh.user, host, target)
        return render('/data/upload.mako')

    def delete(self):
        box = request.params.get('box')
        filedir = request.params.get('dir')
        files = request.params.get('file')
        log.debug("%s %s %s", box, filedir, files)
        return "%s %s %s" % (box, filedir, files)

    def _getlisting(self, account_id, path):
        # Get account_id and path
        if not account_id or not path:
            return []

        # Get file listing
        resource = app_globals.jodis.manager.getResource(account_id)
        if not resource:
            log.error('Connection to account %d is dead!!!' % account_id)
            return []

        # Obtain actual listing
        try:
            listing = resource.raw('ls -lh --time-style=long-iso %s' % path)
        except Exception as _:
            try:
                listing = resource.raw('ls -lh %s' % path)
            except Exception as _:
                log.critical('Cannot retrieve path %s on %s!', path, resource.host)
                return []

        # Parse file listing
        # What we pass to the mako template: type, filename, mod date, size
        newarr = []
        for a in listing[0].split('\n'):
            a = a.split()
            if len(a) >= 8:
                if a[0][0] == 'd':
                    newarr.append(['directory', a[-1].decode('latin1')])
                else:
                    if len(a) == 9:
                        date = ('%s %s %s' % (a[-4], a[-3], a[-2]))
                        newarr.append(['file', a[-1], date, a[-5]])
                    else:
                        date = ('%s %s' % (a[-3], a[-2]))
                        newarr.append(['file', a[-1], date, a[-4]])

        return newarr

    def _updatelisting(self, box, hostname='', path=''):
        account_id = int(session[SESS_KEY][box]['host'] or 0)
        account = meta.Session.query(Account).filter(Account.id == account_id).one()
        try: is_account_holder = account.user_id == session.get('user_id')
        except Exception as _: is_account_holder = False

        # Get user project path.
        ###cwuserpath = config.get('cw.cwuser_loc')
        cwuserpath = config.get('cw.cwuser_rem')
        userprojpath = os.path.sep.join([cwuserpath, session.get('user', 'guest')])

        # Set the path to one of the following (in order): specified path, existing path, user cw directory
        path = path if path else session[SESS_KEY][box].get('path', '')

        if not path:
            path = userprojpath
        # Prevent non-admins from accessing other folders
        elif not (authorized(auth.is_admin) or is_account_holder) and not path.startswith(userprojpath):
            path = userprojpath

        # Obtain actual listing
        try:
            listing = self._getlisting(account_id, path)
            log.debug('Updating %s %d:%s', box, account_id, path)
        except Exception:
            listing = []
            log.critical('Cannot update listing on %d!', account_id)

        if path.startswith(cwuserpath):
            mindir = None
            maxdir = None
            mypath = ''
            outputpath = ''
            jobname = ''
            jobid = ''
            path_arr = path.replace(cwuserpath, '').split('/')
            if len(path_arr) >= 2:
                jobname = path_arr[1]
                jobid = jobname.split('_')[-1]
                mypath = cwuserpath + '/'.join(path_arr[:2])

                outputpath = mypath + '/output'
                ls_output = self._getlisting(account_id, outputpath)
                if not ls_output:
                    outputpath = mypath + '/OUTPUT'
                    ls_output = self._getlisting(account_id, outputpath)
                for i in ls_output:
                    if i[0] == 'file' and i[1].endswith('.dat'):
                        try:
                            mynum = int(i[1][1:5])
                        except Exception as e:
                            log.error('Listing update failure! %s,%s. %s' % i[1], i[1][1:5], e)

                        if mindir == None or mynum < mindir:
                            mindir = mynum
                        if max == None or mynum > max:
                            maxdir = mynum

            session[SESS_KEY]['viz']['jobname'] = jobname
            session[SESS_KEY]['viz']['jobid'] = jobid
            session[SESS_KEY]['viz']['start_time'] = mindir
            session[SESS_KEY]['viz']['stop_time'] = maxdir
            session[SESS_KEY]['viz']['jobdir'] = mypath
            session[SESS_KEY]['viz']['outputdir'] = outputpath

            try:
                c.model_key = jobname.split('_')[2]
                c.grid_key = Gccom.model_info[c.model_key]['grid_key']
                session[SESS_KEY]['viz']['model_key'] = c.model_key
                session[SESS_KEY]['viz']['grid_name'] = Gccom.bath_grid[c.grid_key]['name']
                session[SESS_KEY]['viz']['grid_imax'] = Gccom.bath_grid[c.grid_key]['IMax']
                session[SESS_KEY]['viz']['grid_jmax'] = Gccom.bath_grid[c.grid_key]['JMax']
                session[SESS_KEY]['viz']['grid_kmax'] = Gccom.bath_grid[c.grid_key]['KMax']
            except (AttributeError, IndexError) as _:
                pass

        # Update session variables
        session[SESS_KEY][box]['path'] = path
        session[SESS_KEY][box]['listing'] = listing
        session.save()

        c.data = session[SESS_KEY]
        log.debug("c.data: %s", c.data)
        return render(self.mako)

    def changedir(self):
        # Grab params
        box = request.params.get('box').decode('latin1')
        dir = request.params.get('dir').decode('latin1')

        # Check a host exists
        if 'host' not in session[SESS_KEY][box]:
            return

        path = session[SESS_KEY][box]['path']
        account = int(session[SESS_KEY][box]['host'] or 0)

        # Clean input
        dir = dir[:-1] if dir[-1] == '/' else dir

        # Change full path
        if dir == '..Parent Directory':
            arr = session[SESS_KEY][box]['path'].split('/')
            path = '/'.join(arr[:-1])
            if not path:
                path = '/'
        elif dir == '..User Home Directory':
            path = '~'
        elif dir == '..Home Directory':
            path = None
        elif dir == '..Refresh Listing':
            pass
        else:
            path = path + '/' + dir

        # Update listing
        session[SESS_KEY][box]['path'] = path
        session.save()
        self._updatelisting(box, path)

    def copyfile(self, source, target, sourcehost, targethost):
        log.debug('copying file %s to %s', source, targethost)
        resource = app_globals.jodis.manager.getResource(sourcehost)
        tgtresource = app_globals.jodis.manager.getResource(targethost)
        if resource == None:
            log.error('Error: Resource (%s) is not available!' % sourcehost)
            return None

        filename = source.split('/')[-1]
        try:
            ###resource.ssh.scp(resource.ssh.user, sourcehost, source, None, None, config.get('cw.cwproj_loc'))
            resource.ssh.scp(resource.ssh.user, sourcehost, source, None, None, config.get('cw.cwproj_rem'))
            resource.ssh.scp(None, None, config.get('cw.cwproj_loc') + filename, tgtresource.ssh.user, targethost, target)
        except Exception as _:
            log.error('Trouble scping file %s from %s to %s', source, sourcehost, targethost)
            return None

        return resource

    def movefile(self, source, target, host):
        resource = app_globals.jodis.manager.getResource(host)
        if resource == None:
            log.error('Error: Resource (%s) is not available!' % host)
            return None

        try:
            resource.ssh.move(source, target)
        except Exception as e:
            log.error('Trouble moving file %s to %s: %s', source, host, e)
            return None

        return resource

    def transfer(self):
        source = request.params.get('src').decode('latin1')
        target = request.params.get('tgt').decode('latin1')
        sourcehost = request.params.get('srchost').decode('latin1')
        targethost = request.params.get('tgthost').decode('latin1')

        log.debug('Copying from %s:%s to %s:%s', sourcehost, source, targethost, target)
        if sourcehost == targethost:
            log.debug('Moving %s to %s on %s' % (source, target, sourcehost))
            self.movefile(source, target, sourcehost)
        else:
            log.debug('Copying %s:%s to %s:%s' % (sourcehost, source, targethost, target))
            self.copyfile(source, target, sourcehost, targethost)
        return

    def copy(self):
        source = request.params.get('src').decode('latin1')
        target = request.params.get('tgt').decode('latin1')
        sourcehost = request.params.get('srchost').decode('latin1')
        targethost = request.params.get('tgthost').decode('latin1')

        log.debug('Copying %s:%s to %s:%s' % (sourcehost, source, targethost, target))
        self.copyfile(source, target, sourcehost, targethost)
        return

    def move(self):
        source = request.params.get('src').decode('latin1')
        target = request.params.get('tgt').decode('latin1')
        sourcehost = request.params.get('srchost').decode('latin1')
        targethost = request.params.get('tgthost').decode('latin1')

        log.debug('Moving %s to %s on %s' % (source, target, sourcehost))
        resource = self.copyfile(source, target, sourcehost, targethost)
        if resource:
            try:
                resource.raw('rm -f source')
            except Exception as _:
                log.error('Connection killed')
        return resource

    def jobsummary(self):
        numJobs = 10
        c.user = session.get('user_id')
        c.title = config.get('project.shortname','CyberWeb') + ' Job Summary for:  ' + session['user']
        c.jobname = 'jobname'
        c.jobs = j.jobSummary(self, session.get('user_id'), numJobs)
        c.jobstates = j.getJobStateNames()
        c.jobstatekeys = j.getJobStateKeys()
        d = {}
        for i in range(len(c.jobstatekeys)):
            d[c.jobstatekeys[i]] = c.jobstates[i]
        c.jobstateheaders = d
        c.title = config.get('project.shortname','CyberWeb') + ' Job Monitor Listing for:  ' + session['user']
        return render('/data/jobsummary.mako')

    def jobmonitor(self):
        numjobs = 20
        c.user = session.get('user_id')
        c.jobname = request.params.get('jobname') or ''
        c.jobs = j.jobMonitor(self, session.get('user_id'), numjobs)
        c.jobstates = j.getJobStateNames()
        c.jobstatekeys = j.getJobStateKeys()
        d = dict()
        for i in range(len(c.jobstatekeys)):
            d[c.jobstatekeys[i]] = c.jobstates[i]
        c.jobstateheaders = d
        c.title = config.get('project.shortname', 'CyberWeb') + ' Job Monitor Listing for:  ' + session['user']
        #log.debug('GCOMJOBMONITOR: finished jobs:%s', str(c.jobs))
        return render('/data/jobmonitor.mako')

    ####
    # Function shows jobhistory depending on the type
    ####
    def jobhistory(self, tablename='running'):
        # Populate jobs
        c.list = tablename
        per_page = 20

        if tablename == 'queued':
            myjobstate = JobState.queued
            order = model.Job.submit_time
        elif tablename == 'running':
            myjobstate = JobState.running
            order = model.Job.start_time
        elif tablename == 'finished':
            myjobstate = JobState.finished
            order = model.Job.end_time
        elif tablename == 'error':
            myjobstate = JobState.error
            order = model.Job.end_time
        else:
            c.list = 'all'
            order = model.Job.submit_time

        if c.list == 'all':
            queue_query = meta.Session.query(model.Job).filter(model.Job.user_id == session['user_id']).order_by(sa.desc(order))
        else:
            queue_query = meta.Session.query(model.Job).filter(sa.and_(model.Job.state == myjobstate, model.Job.user_id == session['user_id'])).order_by(sa.desc(order))

        c.jobs = Page(queue_query, page=int(request.params.get('page', 1)), items_per_page=per_page)

        c.jobheaders = ['ID', 'Name', 'Service', 'Resource', 'Status', 'Submit Time', 'Start Time', 'End Time']
        return render('/data/jobhistory.mako')

    def getresults(self, tablename):
        ''' tablename is actually jobid '''
        output_arr = []
        ####jobdir = os.path.sep.join([config.get('cwuser_loc'), session['user'], tablename])
        jobdir = os.path.sep.join([config.get('cwuser_rem'), session['user'], tablename])
        output_arr.append('<b>Results for Job Directory: ' + session[SESS_KEY]['viz']['jobname'] + '<p></b>')
        output_arr.append('<br><b>Note: View results using the CW Job Monitor.</b><hr>')

        log.info('GetResults: jobdir = %s' % jobdir)
        r = app_globals.jodis.manager.getResource('longboard.acel.sdsu.edu')
        try:
            _ = r.raw('/bin/cat /u06/%s/job.info.local' % jobdir)[0].strip()
        except Exception as _:
            output_arr.append('<b>Results for Job Directory: ' + jobdir + '<p></b>')

        try:
            for i in file.splitlines():
                output_arr.append(i + '<br>')
        except Exception as _:
            output_arr.append("Job Completed")

        return  output_arr

    def getfile(self):
        user = session.get('user', '')
        path = request.params.get('path')
        try: host = int(request.params.get('host'))
        except Exception: host = None

        if not user or not path:
            return 'User or path not defined.'

        # @TODO: Test if host is in Jodis list
        if not host:
            return 'Unknown host %s.' % host

        filename = path.split('/')[-1]
        ext = path.split('.')[-1]

        # expected format of path: cwproj/users/<username>/<job id>/<filename>
        if host == 'longboard.acel.sdsu.edu':
            if not path.startswith('%s%s' % (CWPROJPATH, user)):
                return 'You are not allowed to access this file (%s)' % path

        resource = app_globals.jodis.manager.getResource(host)
        if not resource:
            log.debug('Can\'t retrieve resource %s', host)
            return

        if ext == 'jpg' or ext == 'jpeg' or ext == 'gif':
            if not os.path.isfile('cyberweb/public/viz/' + filename):
                try:
                    resource.ssh.scpFrom(None, None, path, 'cyberweb/public/viz')
                except Exception as e:
                    log.error('Error accessing file (%s). %s', path, e)
                    return 'Error accessing the file (%s)' % path

            return '<html><img src ="/viz/%s" alt ="vis image here" /></html>' % filename
        else:
            try:
                myfile = resource.raw('cat %s' % path)[0]
            except Exception as e:
                log.error('Error accessing file (%s). %s', path, e)
                return 'Error accessing the file (%s)' % path

            response.headers['content-type'] = 'text/plain; charset = utf-8'
            return myfile

    def jobviewer(self, tablename):
        user = session.get('user', '')
        if not user:
            return 'NO USER!'

        box = 'left'
        path = CWPROJPATH + user + '/' + tablename
        hostname = config.get('cw.arch_host', 'longboard.acel.sdsu.edu')

        if hostname and box:
            if 'host' not in session[SESS_KEY][box] or session[SESS_KEY][box]['host'] != hostname:
                path = None

            session[SESS_KEY][box]['host'] = hostname
            session[SESS_KEY][box]['path'] = path
            session.save()
            return self._updatelisting(box)

        c.data = session[SESS_KEY]
        return render(self.mako)

    def download(self):
        ''' tablename = filename '''
        user = session.get('user', '')
        box = request.params.get('box', '')
        filejson = request.params.get('file', '[]')
        log.debug('DOWNLOAD File: %s' % filejson)

        try:
            files = json.loads(filejson)
        except Exception as e:
            log.error('Can\'t parse json object (%s). %s', filejson, e)
            return 'Error: problem with tarfile'

        try:
            files = json.loads(filejson)
        except Exception as e:
            log.error('Can\'t parse json object (%s). %s', filejson, e)
            return 'Error: problem with tarfile'

        host = session[SESS_KEY][box]['host']
        path = session[SESS_KEY][box]['path']

        log.debug('DOWNLOAD: %s@%s:%s/%s', user, host, path, files)

        if not user or not path:
            return 'User or path not defined.'
        elif not files:
            return 'No file specified for download.'
        # @TODO: Test if host in in Jodis list
        elif not host:
            return 'Unknown host %s.' % host

        resource = app_globals.jodis.manager.getResource(host)
        md5Inst = md5('%s@%s:%s/%s' % (user, host, path, files)).hexdigest()
        target = '/tmp/%s.tar.gz' % md5Inst
        fileStr = ' '.join(files)
        log.debug('DOWNLOAD md5Inst File: %s' % md5Inst)
        print path+'|'+target+'|'+fileStr
        try:
            stderr = resource.raw('cd %s;tar -cvzf %s %s' % (path, target, fileStr))
            resource.ssh.scp(resource.ssh.user, host, target, None, None, '/tmp/')
        except Exception as e:
            log.error('Trouble tarring file. %s', e)
            return 'Error: problem with tarfile'

        if stderr:
            log.error('Problem with tarring. %s', stderr)
            return 'Error: problem with tarfile'

        retVal = ''
        try:
            fh = open(target, 'rb')
            for i in fh.readlines():
                retVal += i
            fh.close()
        except Exception as e:
            log.error('Trouble opening file. %s', e)
            return 'Error: problem with tarfile'

        response.headers['content-type'] = 'application/x-tar'
        return retVal
