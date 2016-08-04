import logging
import numpy as np
import os, sys, time, re, getopt, getpass, math, tempfile
import traceback,commands
import string, json
from time import strftime
import pexpect
import urlparse

from pylons import request, response, session, app_globals, tmpl_context as c, config, url
from pylons.decorators import jsonify
from authkit.authorize.pylons_adaptors import authorize,authorized
import sqlalchemy as sa
from sqlalchemy.orm.attributes import manager_of_class as manager
from config import Config
from pylons.controllers.util import redirect

from cyberweb.lib.base import BaseController, render
from cyberweb import model
from cyberweb.model import meta,JobState, Job, Message, Group, GroupDefinition, User, Service, ServiceName, Account, Resource

# add authentication to control who can access this class.
from authkit.permissions import ValidAuthKitUser
from cyberweb.lib.jodis import sshresource as myssh,resources
from cyberweb.lib.jodis.base import Jodis, JodisJob, JodisTask
from cyberweb import model
from cyberweb.lib import Viz, auth, Gccom, BaseJob as Job, helpers as h
from cyberweb.lib import jobs as j
 
log = logging.getLogger(__name__)
   

####CWPROJPATH = config.get('cw.cwuser_loc')
CWPROJPATH = config.get('cw.cwuser_rem')
SESS_KEY = 'filebrowser_data'
    
class PostjobController(BaseController):
    @authorize(auth.is_valid_user)
    def __before__(self, mako='/data/data.mako'):
        self.mako = mako

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
        c.plots = Viz.plots
        try: self.servicename_id = meta.Session.query(model.ServiceName).filter(model.ServiceName.name == 'SSH').first().id
        except Exception as _: self.servicename_id = 0

    def index(self):
        # Pull CGI params
        # test3 - through bitbucket repo
        box = request.params.get('box')
        path = request.params.get('path')
        
        print 'Box: %s, path: %s' % (box, path);
        
        account_id = int(request.params.get('host') or 0)

        if not session.get('available_resources'):
            session['available_resources'] = app_globals.user_resources(session.get('user_id'))
            session.save()

        if account_id and box:
            if 'host' not in session[SESS_KEY][box] or session[SESS_KEY][box]['host'] != account_id:
                path = None
            
            print 'Box: %s, path: %s' % (box, path);
            session[SESS_KEY][box]['host'] = account_id
            session[SESS_KEY][box]['path'] = path
            session.save()
            log.debug("In IF BLOCK")
            log.debug("Session: %s", session)
            log.debug("SESS_KEY: %s", SESS_KEY)
            return self._updatelisting(box)

        c.data = session[SESS_KEY]
        c.plots = Viz.plots
        #return render(self.mako)
        
        log.debug("Session: %s", session)
        log.debug("SESS_KEY: %s", SESS_KEY)
        return render('/postjob/index.mako')
        
    def _getlisting(self, account_id, path):
        # Get account_id and path
        if not account_id or not path:
            return []

        # Get file listing
        log.debug("In _getlisting function")
        log.debug("account_id:")
        log.debug(account_id)
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
        account = int(session[SESS_KEY][box]['host'] or 0)
        log.debug("Account : %s", account)
        
        # Get user project path.
        ###cwuserpath = config.get('cw.cwuser_loc')
        cwuserpath = config.get('cw.cwuser_rem')
        userprojpath = os.path.sep.join([cwuserpath, session.get('user', 'guest')])

        # Set the path to one of the following (in order): specified path, existing path, user cw directory
        path = path if path else session[SESS_KEY][box].get('path', '')

        if not path:
            path = userprojpath
        # Prevent non-admins from accessing other folders
        elif not authorized(auth.is_admin) and not path.startswith(userprojpath):
            path = userprojpath

        # Obtain actual listing
        try:
            listing = self._getlisting(account, path)
            log.debug('Updating %s %d:%s', box, account, path)
        except Exception:
            listing = []
            log.critical('Cannot update listing on %d!', account)

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
                ls_output = self._getlisting(account, outputpath)
                if not ls_output:
                    outputpath = mypath + '/OUTPUT'
                    ls_output = self._getlisting(account, outputpath)
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
        #return render(self.mako)
        return render('/postjob/index.mako')

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
    
     
    def selectHost(self):
        
        box = 'right'
        host = request.params.get('host_name')
        host_id = request.params.get('host_id')
        
        log.debug("host: %s", host)
        #log.debug("path: %s", path)
        log.debug("session[SESS_KEY][box]['host'] : %s", host_id)
        
        account = int(host_id or 0)
        session[SESS_KEY][box]['host'] = int(host_id)
        
        # Get user project path.
        ###cwuserpath = config.get('cw.cwuser_loc')
        cwuserpath = config.get('cw.cwuser_rem')
        userprojpath = os.path.sep.join([cwuserpath, session.get('user', 'guest')])

        # Set the path to one of the following (in order): specified path, existing path, user cw directory
        dir = request.params.get('host_path') if request.params.get('host_path') else session[SESS_KEY][box].get('path', '')
        #path = session[SESS_KEY][box]['path']

        log.debug("host: %s", host)
        log.debug("path: %s", dir)
        log.debug("account: %s", account)

        # Clean input
        if(dir != ''):
            dir = dir[:-1] if dir[-1] == '/' else dir

        # Change full path
        if dir == '..Parent Directory':
            arr = session[SESS_KEY][box]['path'].split('/')
            path = '/'.join(arr[:-1])
        elif dir == '..Home Directory':
            path = None
        elif dir == '..Refresh Listing':
            path = dir
        else:
            path = dir

        # Update listing
        session[SESS_KEY][box]['path'] = path

        if not path:
            path = userprojpath
        # Prevent non-admins from accessing other folders
        elif not authorized(auth.is_admin) and not path.startswith(userprojpath):
            path = userprojpath
        session[SESS_KEY][box]['path'] = path
        session.save()
        # Obtain actual listing
        try:
            listing = self._getlisting(account, path)
            log.debug('Updating %s %d:%s', box, account, path)
        except Exception:
            listing = []
            log.critical('Cannot update listing on %d!', account)

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
                ls_output = self._getlisting(account, outputpath)
                if not ls_output:
                    outputpath = mypath + '/OUTPUT'
                    ls_output = self._getlisting(account, outputpath)
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

        log.debug("session[SESS_KEY]['right']['host']: %s", session[SESS_KEY]['right']['host'])
        log.debug("session[SESS_KEY]['right']['path']: %s", session[SESS_KEY]['right']['path'])

        log.debug("Check Session: %s")
        log.debug(session)
        c.data = session[SESS_KEY]
#        temp = json.dumps(c.data)
#        log.debug("temp:")
#        log.debug(temp)
#        log.debug("Type of temp: %s", type(temp))
#        json_obj = json.loads(temp)
#        log.debug("Type of temp: %s", type(json_obj))
        
        return json.dumps(c.data)
       
    def selectjob(self):
        '''
        This represents the action after a form has been submitted.
        This function should be re-written in the original form function
        to easily handle mis-matched states
        '''
        scriptname = request.params['script']
        script = scriptname + '.py'
        scriptdir = "localscripts"
        c.cmd = '%s/%s ' % (scriptdir,script)
        myjob = BaseJob()
        myjob.create(2,scriptname)
        myjob.start()
        c.jobid = myjob.id
        status,output = commands.getstatusoutput(c.cmd)
        newline = re.compile('\n+')
        #c.results = newline.sub('||',output)
        #c.status = status
        #c.script = script
        #c.cwuser = session['user']
        myjob.finish()
        # Return a rendered template
        #return render('/demos/demo_cmd.mako')
        c.plots = Viz.plots
        return output
    	
    ################################################################################
    ###  Execution Services:  Run jobs using JODIS +  passwordless SSH  (local scripts)
    ################################################################################
    def getImageSSH(self):
        
        c.plots = Viz.plots
        
        c.hostname = session[SESS_KEY]['left']['host']
        c.job_path = request.params.get('job_path').decode('latin1')
        c.filename = request.params.get('file_name').decode('latin1')
        scriptname = session[SESS_KEY]['left']['path']
        script = scriptname + '.py'
        scriptdir = "localscripts"
        c.cmd = '%s/%s ' % (scriptdir,script)
        c.command = "ls -l";
        log.debug('Host:')
        log.debug('%s' % c.hostname)
        log.debug('job_path:')
        log.debug('%s' % c.job_path)
        
        taskaction = ''
        jobaction = ''
        jodis = app_globals.jodis

        
        log.debug('job name: ')  
        log.debug('%s' % c.job.name)
        log.debug('job id: ')  
        log.debug('%s' % c.job.id)
        log.debug('result: ')  
        log.debug('%s' % c.result)
        try:
            resource = app_globals.jodis.manager.getResource(c.hostname)
            if not resource:
                log.error('Connection to %s is dead!!!' % c.hostname)
                return []
        except Exception as e:
            output = e.message
        
        log.debug('Resource: ')          
        log.debug('%s' % resource.host)
        
        try:
            resource_id =  meta.Session.query(model.Resource).filter(model.Resource.name == resource.host).first().id
            service_id = resource.account.service_id

        except Exception as e:
            log.error('Problem creating job: %s', e)
            session['error_flash'] = 'Missing data input'
            session.save()
            return redirect(url(controller='gcom', action = '%s_%s' % (c.mode.lower(), c.model_key) ))
        log.debug('Resource id: ')  
        log.debug('%s' % resource_id)
        log.debug('User id: ')
        log.debug('%s' % session.get('user_id',0))  
        # log.debug('Job Name: ')
        c.job = jodis.createJob(service_id, session['user_id'])
        c.jobname = c.job.name
        c.result = 'Added job (%s): %s' % (c.job.id, c.job.name)
         
        complete_filepath = c.job_path + '/' + c.filename
        log.debug('Complete File path: ')
        log.debug('%s' % complete_filepath)
        
        command = ('xxd -ps %s ' % complete_filepath)
        log.debug('Command: ')
        log.debug('%s' % command)
        
        image = resource.raw(command)
        output = 'success'
        return image

#    def getPlot(self, host, path, imagename):
#        
#        c.plots = Viz.plots
#        c.hostname = host
#        c.job_path = path
#        c.filename = imagename
#
#        jodis = app_globals.jodis
#
#        try:
#            resource = app_globals.jodis.manager.getResource(c.hostname)
#            if not resource:
#                log.error('Connection to %s is dead!!!' % c.hostname)
#                return []
#        except Exception as e:
#            output = e.message
#        
#        try:
#            resource_id =  meta.Session.query(model.Resource).filter(model.Resource.name == resource.host).first().id
#            service_id = resource.account.service_id
#            
#        except Exception as e:
#            log.error('Problem creating job: %s', e)
#            session['error_flash'] = 'Missing data input'
#            session.save()
#            return redirect(url(controller='postjob', action = 'index'))
#        
#        complete_filepath = c.job_path + c.filename
#        command = ('xxd -ps %s ' % complete_filepath)
#        image = resource.raw(command)
#        return image

    def getPlot(self, host, path, imagename):
        
        c.plots = Viz.plots
        c.hostname = host
        c.job_path = path
        c.filename = imagename

        jodis = app_globals.jodis

        try:
            resource = app_globals.jodis.manager.getResource(c.hostname)
            if not resource:
                log.error('Connection to %s is dead!!!' % c.hostname)
                return []
        except Exception as e:
            output = e.message
        
        try:
            resource_id =  meta.Session.query(model.Resource).filter(model.Resource.name == resource.host).first().id
            service_id = resource.account.service_id
            
        except Exception as e:
            log.error('Problem creating job: %s', e)
            session['error_flash'] = 'Missing data input'
            session.save()
            return redirect(url(controller='postjob', action = 'index'))
        
        complete_filepath = c.job_path + c.filename
        command = ('xxd -ps %s ' % complete_filepath)
        image = resource.raw(command)
        return image
    
    def getMovie(self, host, path, movie_name):
    	c.hostname = host
    	c.job_path = path
    	c.filename = movie_name
    	jodis = app_globals.jodis
        try:
            resource = app_globals.jodis.manager.getResource(c.hostname)
            if not resource:
                log.error('Connection to %s is dead!!!' % c.hostname)
                return []
        except Exception as e:
            output = e.message
        
        try:
            resource_id =  meta.Session.query(model.Resource).filter(model.Resource.name == resource.host).first().id
            service_id = resource.account.service_id
            
        except Exception as e:
            log.error('Problem creating job: %s', e)
            session['error_flash'] = 'Missing data input'
            session.save()
            return redirect(url(controller='postjob', action = 'index'))
        
        complete_filepath = c.job_path + c.filename
        #command = ('scp %s ' % complete_filepath)
        full_path = '%s%s' % (path, movie_name)
        #target = '%s/cyberweb/public/contour_movies/%s' % (os.getcwd(), movie_name)
        target = '%s/cyberweb/public' % (os.getcwd())
        print "full_path type: "
        print type(full_path)
        print "resource.ssh.host type: "
        print type(resource.ssh.host)
        print "resource.ssh.user type: "
        print type(resource.ssh.user)
        
        sourceStr = resource.ssh.host + ':' + full_path
        print sourceStr
        
        command = 'resource.ssh.scp(%s, %s, %s, %s, %s, %s)' % (resource.ssh.user,resource.ssh.host,full_path,None,None,target)
        print command
        result = resource.ssh.scp(resource.ssh.user,resource.ssh.host,full_path,None,None,target)
        #image = resource.raw(command)
        return 	
    
    def checkIfImagePresent(self, filename, filePath):
        jodis = app_globals.jodis 
        complete_filepath = ('%s%s' % (filePath, filename))
        
        try:
            resource = app_globals.jodis.manager.getResource(c.hostname)
            if not resource:
                log.error('Connection to %s is dead!!!' % c.hostname)
                return []
        except Exception as e:
            output = e.message
                
        # scp the localscript file to remote host in the target plot file location
        filename = 'check_plot_present.py';
        source_dir = 'localscripts'
        source = os.path.join(source_dir, filename)
        full_path =  os.path.abspath(source)
        host_name = session['available_resources'][c.hostname]['hostname']
        
        feedback = resource.ssh.scp(None,None,full_path,resource.ssh.user,host_name,filePath)
        log.debug("SCP RESULT: %s", feedback)
        
        #run the script which was just copied to remote host
        #command = 'cd ' + filePath + '; /home4/smita/lib/python/Python-2.7.2/bin/python2.7 ' + filename + ' ' + complete_filepath 
        command = 'cd ' + filePath + '; python2.7 ' + filename + ' ' + complete_filepath 
        log.info("Command: %s" % command)
        result = resource.raw(command)
        log.debug(result)
        feedback = result[0]
        new_eval = eval(feedback)
        return new_eval
        
    
    def createPlotImage(self):
        
        all_parameters = request.params
        for key, value in request.params.items(): 
            if(key == "analysisTypes"):
                log.debug("value: %s", value)
                if(value == "performance"):
                    FinalPlot = request.params.get(value)
                    log.debug("Final Option: %s", FinalPlot)
                    if(FinalPlot == "elapsedTime"):
                        plot = self.createElapsedTimePlot()
                    elif(FinalPlot == "cumulativeTime"):
                        plot = self.createCumulativeTimePlot()
                    elif(FinalPlot == "runtime"):
                        plot = self.createRunTimePlot()
                elif(value == "bathymetry"):
                    log.debug("plot_file: %s", request.params.get('plot_file'))
                    plot = self.createBathymetryPlot(request.params.get('plot_file'))
                elif(value == "contour" or value == "vector"):
                    plot = self.createContourMovie(all_parameters)
        return plot

    def rebuildPlotImage(self):
        
        all_parameters = request.params
        
        #all_parameters[plot_type] if plot_type in all_parameters, else error
        plot_type = all_parameters.get("plot_type", "error")  
        check_rebuild = all_parameters.get("check_rebuild", "error")
        print all_parameters
        print "plot_type"
        print plot_type
        print "check_rebuild"
        print check_rebuild
        print "type(check_rebuild)"
        print type(check_rebuild)
        if(plot_type == 'bathymetry' and check_rebuild == '1'):
            plot = self.createBathymetryPlot(all_parameters.get("plot_file", 'none'), 'true', {})
        elif(plot_type == 'bathymetry' and check_rebuild == '0'):
            plot = self.createBathymetryPlot(all_parameters.get("plot_file", 'none'), 'true', all_parameters)
        return plot
        
    def getBathymetryLocation(self):
        bathymetry_location = config.get('cw.bathymetry_location')
        print "Bathymetry_location"
        print bathymetry_location
        feedback = {'path':bathymetry_location}
        return json.dumps(feedback)

    def createContourMovie(self, all_parameters):
        print "In createContourMovie function"
        print "Session: "
        print session
        
        print "all_parameters"
        print type(all_parameters)
        print all_parameters
        
        print "check_selected_job"
        print all_parameters['check_selected_job']
        
        
        print "all_parameters"
        print type(all_parameters)
        print all_parameters
        
        if 'contour_image' in all_parameters:
        	view_plane = all_parameters['contour_image']
        elif 'contour_movie' in all_parameters:
            view_plane = all_parameters['contour_movie']
        elif 'contour_sequence' in all_parameters:
            view_plane = all_parameters['contour_sequence']
        else:
            #default plane is XZ
        	view_plane = 'XZ'
        print "Plane"
        print view_plane
        bathymetry_location = config.get('cw.bathymetry_location')
        print "bathymetry_location"
        print bathymetry_location
        print "session['gridfname']"
        print session['gridfname']
        if(all_parameters['analysisTypes'] == 'vector'):
            contour_output_format = all_parameters['vector']
        elif(all_parameters['analysisTypes'] == 'contour'):
            contour_output_format = all_parameters[all_parameters['contour']]
        print "contour_output_format"
        print contour_output_format
        
        # make start_time and skip_time as view_plane
        start_time = 0
        end_time = session['MaxFileNo']
        skip_time = 10
        
        grid_file = '%s/%s' % (bathymetry_location, session['gridfname'])#all_parameters['plot_file']
        iMax = session['Imax']
        jMax = session['Jmax']
        kMax = session['Kmax']
        plot_type = all_parameters['analysisTypes']
        #version is 2 for now
        version = 2
        if(all_parameters['analysisTypes'] == 'vector'):
            input_parameter = 'velocity'
        elif(all_parameters['analysisTypes'] == 'contour'):
            input_parameter = all_parameters['contour']
        jodis = app_globals.jodis       
        c.hostname = session[SESS_KEY]['right']['host']
        c.job_path = urlparse.unquote(all_parameters['check_selected_job'])
        #session[SESS_KEY]['right']['path']
        
        #calculate job name
        path_values = urlparse.unquote(all_parameters['check_selected_job']).split('/')
        print "path_values"
        print path_values
        total_path_values = len(path_values)
        job_name = path_values[-1]
        print "job_name"
        print job_name
        path_values[-1] = ''
        job_path = '/'.join(path_values)
        print "job_path"
        print job_path
        
        check_plot = 'true'
        if(contour_output_format == 'contour_movie'):
            plotFileName = job_name + '_' + input_parameter+ '_' + view_plane + '_' + plot_type + "_movie.mp4"
        elif(contour_output_format == 'contour_image' or contour_output_format == 'contour_sequence'):
            check_plot = 'false'
            
        #"contourMovie.mp4"
        target = c.job_path + '/' + 'OUTPUT/'
        log.debug("c.hostname: %s", c.hostname)
        
        
        # check if the plot is already created for only movies. 
        #Coz images can be named according to the skip time and can conflict naming convention
        #So make sure you always create new images.
        if(check_plot == 'true'):
            feedback = self.checkIfImagePresent(plotFileName, target)
        else:
            feedback = {}
            feedback['error'] = 'false'
            feedback['plotNew'] = 'true'
            feedback['result'] = 'false'
        print "DEBUG contourvectorPlot"
        print feedback
        
        if(feedback['error'] != 'true' and (feedback['result'] == "false" or feedback['plotNew'] == "true")):
            # create new plot only id plot was not created previously and was not create one week back
            try:
                resource = app_globals.jodis.manager.getResource(c.hostname)
                if not resource:
                    log.error('Connection to %s is dead!!!' % c.hostname)
                    return []
            except Exception as e:
                output = e.message
            
            try:
                resource_id =  meta.Session.query(model.Resource).filter(model.Resource.name == resource.host).first().id
                service_id = resource.account.service_id
            except Exception as e:
                log.error('Problem creating job: %s', e)
                session['error_flash'] = 'Missing data input'
                session.save()
                return e
                            
            #c.job_path = session[SESS_KEY]['job_path']
            #log.debug("Job Path: %s", c.job_path)
            #jobPathElements = c.job_path.split('/')
            #jobName = jobPathElements[-1]
            
            # scp the localscript file to remote host in PARA folder of the job selected
            filename = 'contour_movie_script.py';
            source_dir = 'localscripts'
            source = os.path.join(source_dir, filename)
            full_path = os.path.join(source_dir, filename)
            host_name = session['available_resources'][c.hostname]['hostname']
            result = resource.ssh.scp(None,None,full_path,resource.ssh.user,host_name,target)
            log.debug("SCP result: %s" , result)
            
            #run the script which was just copied to remote host
            submitfn = target
            #writeTimesFilename = 'writetimes.dat'
            #command = 'cd ' + submitfn + '; /home4/smita/lib/python/Python-2.7.2/bin/python2.7 ' + filename + ' ' + writeTimesFilename + ' ' + plotFileName + ' ' + session["wrthz"]
            command = 'cd ' + submitfn + '; python2.7 contour_movie_script.py ' + '../..' + ' ' + job_name + ' ' \
                        + str(start_time) + ' ' + str(end_time) + ' ' + str(skip_time) + ' ' + str(version) + ' ' \
                        + grid_file + ' ' + str(iMax) + ' ' + str(jMax) + ' ' + str(kMax) + ' ' + str(input_parameter) + \
                        ' ' + str(view_plane) + ' ' + str(contour_output_format) + ' ' + plot_type
            print command
            #command = 'cd ' + submitfn + '; python contour_movie_script.py /home4/smita/cyberweb_data/jobs/par job.140487.100.200 1 100 5 2 /home4/smita/bathymetry/Grid.97x33x33.dat 97 33 33 velocity ' + view_plane
            #print command
            log.info("Command: %s" % command)
            #plot_file = resource.raw(command)
            plotscript_feedback = resource.raw(command)
            log.debug("feedback from script: %s", plotscript_feedback)
            log.debug("Type of plotscript_feedback[0]:  %s", type(plotscript_feedback[0]))
            log.debug("feedback[0]: %s", plotscript_feedback[0])
            feedback_dict = {}
            try:
                return_feedback = plotscript_feedback[0].split('{')
                check_feedback = '{' + return_feedback[1]
                feedback_dict = eval(check_feedback)
            except Exception as e:
                #error occured
                feedback_dict['error'] = 'true'
                feedback_dict['message'] = e
                log.error('Error occured: %s', e)
                return json.dumps(feedback_dict)
            if(feedback_dict['error'] == 'true'):  #if not error
                log.debug("feedback error: %s", feedback_dict['error'])
                log.debug("feedback message: %s", feedback_dict['message'])           
        elif feedback['error'] == 'true':
            #log.debug("Error checking file: %s" % feedback['error'])
            #return ''
            log.debug("Error checking file: %s" % feedback['error'])
            msg = "Error checking file: %s" % feedback['message']
            returnFeedback = { 'error' : 'true', 'message' : msg}
            return json.dumps(returnFeedback)
        elif(contour_output_format == 'contour_movie'):
            feedback_dict = {}
            feedback_dict['output_name'] = plotFileName
            feedback_dict['error'] = 'false'
            feedback_dict['message'] = ''
            feedback_dict['output_movie'] = 'movie'
        movie_name = feedback_dict['output_name']
        feedback_dict['output_type'] = str(contour_output_format)
        if(feedback_dict['output_type'] == ''):
            feedback['image'], er = self.getPlot( c.hostname, target, plotFileName)
            log.debug("Type of c variable: %s", type(c))
            log.debug("Type of feedback_dict variable: %s", type(feedback))
        if(contour_output_format == 'contour_movie'):
            movie = self.getMovie(c.hostname, target, movie_name)
            feedback_dict['output_name'] = plotFileName
            feedback_dict['output_movie'] = 'movie'
        elif(contour_output_format == 'contour_sequence'):
            image_bytes = []
            for image_name in feedback_dict['output_name']:
                New_image, er = self.getPlot( c.hostname, target, image_name)
                image_bytes.append(New_image)
            feedback_dict['image_data'] = image_bytes
            #movie = self.getMovie(c.hostname, target, movie_name)
            #feedback_dict['output_name'] = plotFileName
            #feedback_dict['output_movie'] = 'movie'
        elif(contour_output_format == 'contour_image'):
            feedback_dict['image'], er = self.getPlot( c.hostname, target, feedback_dict['output_name'])
            log.debug("Type of c variable: %s", type(c))
            log.debug("Type of feedback_dict variable: %s", type(feedback_dict))
        log.debug("Type of feedback_dict variable: %s", type(feedback_dict))
        feedback_dict['parameters'] = []
        print json.dumps(feedback_dict)
        return json.dumps(feedback_dict)
      
    def createBathymetryPlot(self, filename, replot='false', params={}):
        
        log.debug("Replot: %s", replot)
        log.debug("Params: ")
        print params
        
        jodis = app_globals.jodis 
        
        c.hostname = session[SESS_KEY]['right']['host']
        c.job_path = session[SESS_KEY]['right']['path']
        
        #log.debug("Hostname: %s", session[SESS_KEY]['right']['host'])
        #log.debug("Job_PATH: %s", session[SESS_KEY]['right']['path'])
        log.debug("FileName: %s", filename)
        
        file = filename.split('.dat', 1)
        
        plotFileName = "%s%s" % (file[0], ".png")
        log.debug("plotFileName: %s",  plotFileName)
        target = c.job_path
        
        # check if the plot is already created
        if(replot == 'false'):
            feedback = self.checkIfImagePresent(plotFileName, target)
        else:
            feedback = {'error' : 'false',
                        'result': 'false',
                        'plotNew': 'true'}
        log.debug("Is Plot present: %s", feedback)
        
        if(feedback['error'] != 'true' and (feedback['result'] == "false" or feedback['plotNew'] == "true")):
        	# create new plot only id plot was not created previously and was not create one week back
            try:
                resource = app_globals.jodis.manager.getResource(c.hostname)
                if not resource:
                    log.error('Connection to %s is dead!!!' % c.hostname)
                    return []
            except Exception as e:
                output = e.message
            
            try:
                resource_id =  meta.Session.query(model.Resource).filter(model.Resource.name == resource.host).first().id
                service_id = resource.account.service_id
            except Exception as e:
                log.error('Problem creating job: %s', e)
                session['error_flash'] = 'Missing data input'
                session.save()
                return elog.debug("Resource_id : %d", resource_id)
            
            log.debug("Service_Id : %d", service_id)
            log.debug("Job Path: %s", c.job_path)
            
			#jobPathElements = c.job_path.split('/')
			#jobName = jobPathElements[-1]
            
            # scp the localscript file to remote host in PARA folder of the job selected
            script_file = 'bathymetry_script.py';
            source_dir = 'localscripts'
            source = os.path.join(source_dir, script_file)
            full_path = os.path.join(source_dir, script_file)
            host_name = session['available_resources'][c.hostname]['hostname']
            
            result = resource.ssh.scp(None,None,full_path,resource.ssh.user,host_name,target)
            log.debug("SCP result: %s" , result)
            #run the script which was just copied to remote host
            submitfn = target
            bathymetry_file = filename
            bathymetry_file_prbsz =  "%s%s" % (file[0], ".probsize.dat")
            writeTimesFilename = 'writetimes.dat'
            #command = 'cd ' + submitfn + '; /home4/smita/lib/python/Python-2.7.2/bin/python2.7 ' + script_file + ' ' + bathymetry_file + ' ' + bathymetry_file_prbsz + ' ' + plotFileName
            command = 'cd ' + submitfn + '; python2.7 ' + script_file + ' ' + bathymetry_file + ' ' + bathymetry_file_prbsz + ' ' + plotFileName
            
            for key, value in params.items(): 
                if(key != 'plot_type'):
                    command = command + ' ' + key + '=' + value
            log.info("Command: %s" % command)
            plot_file = resource.raw(command)
            plotscript_feedback = resource.raw(command)
            log.debug("feedback from script: %s", plotscript_feedback)
            log.debug("Type of plotscript_feedback[0]:  %s", type(plotscript_feedback[0]))
            log.debug("feedback[0]: %s", plotscript_feedback[0])
            #feedback = {}
            try:
                feedback = eval(plotscript_feedback[0])
            except Exception as e:
                #error occured
                log.error('Error occured: %s', e)
                feedback['error'] = 'true'
                feedback['message'] = e
                return json.dumps(feedback)
            if(feedback['error'] == 'false'):  #if not error
                #save parameters using viz parameter bathymetry_params
                parameters = feedback['parameters']
                feedback['parameters'] = Viz.bathymetry_params
                for i in range(0, len(feedback['parameters'])):
                    if(parameters.has_key(feedback['parameters'][i]["name"])):
                        feedback['parameters'][i]["value"] = parameters[feedback['parameters'][i]["name"]]
                log.debug("Feedback parameters with value:")
                print feedback['parameters']
                
                log.debug("feedback error: %s", feedback['error'])
                log.debug("feedback message: %s", feedback['message'])
                log.debug("feedback parameters: %s", feedback['parameters'])           
            else:
                log.error('Error occured: %s', feedback['message'])
                return json.dumps(feedback)
            #log.debug("Result of Script: %s", plot_file)
            #if(plot_file != 'Success'):
            #	return plot_file           
        elif feedback['error'] != '':
            log.debug("Error checking file: %s" % feedback['error'])
            feedback['error'] = 'false'
            feedback['message'] = "Error checking file: %s" % feedback['error']
            return json.dumps(feedback)
        #if not error get the image data streams
        target = target + '/'
        #image = self.getPlot( c.hostname, target, plotFileName)
        feedback['image'], er = self.getPlot( c.hostname, target, plotFileName)
        log.debug("Type of c variable: %s", type(c))
        log.debug("Type of feedback_dict variable: %s", type(feedback))
        #returnOption = {'name':optionName, 'label': Label,'values':optionValues}
        # log.debug('Return Variable: %s' , returnOption)
        #log.debug("Image: %s", image)
        #feedback.plot = image
        #feedback.error = 'true'
        #feedback['widget'] = self.getWidget('bathymetry')

        #return json.dumps(feedback)
        print json.dumps(feedback)
        return json.dumps(feedback)

    def createElapsedTimePlot(self):
        
        jodis = app_globals.jodis       
        c.hostname = session[SESS_KEY]['right']['host']
        c.job_path = session[SESS_KEY]['right']['path']
        
        plotFileName = "plotFile.png"
        target = c.job_path + '/' 
        #+ 'INFO/'
        log.debug("c.hostname: %s", c.hostname)
        
        
        # check if the plot is already created
        feedback = self.checkIfImagePresent(plotFileName, target)
        print "DEBUG createElapsedTimePlot"
        print feedback
        
        if(feedback['error'] != 'true' and (feedback['result'] == "false" or feedback['plotNew'] == "true")):
            # create new plot only id plot was not created previously and was not create one week back
            try:
                resource = app_globals.jodis.manager.getResource(c.hostname)
                if not resource:
                    log.error('Connection to %s is dead!!!' % c.hostname)
                    return []
            except Exception as e:
                output = e.message
            
            try:
                resource_id =  meta.Session.query(model.Resource).filter(model.Resource.name == resource.host).first().id
                service_id = resource.account.service_id
            except Exception as e:
                log.error('Problem creating job: %s', e)
                session['error_flash'] = 'Missing data input'
                session.save()
                return e
                            
            #c.job_path = session[SESS_KEY]['job_path']
            #log.debug("Job Path: %s", c.job_path)
            #jobPathElements = c.job_path.split('/')
            #jobName = jobPathElements[-1]
            
            # scp the localscript file to remote host in PARA folder of the job selected
            filename = 'performance_parsing.py';
            source_dir = 'localscripts'
            source = os.path.join(source_dir, filename)
            full_path = os.path.join(source_dir, filename)
            host_name = session['available_resources'][c.hostname]['hostname']
            result = resource.ssh.scp(None,None,full_path,resource.ssh.user,host_name,target)
            log.debug("SCP result: %s" , result)
            #run the script which was just copied to remote host
            submitfn = target
            writeTimesFilename = 'writetimes.dat'
            job_id = session['JOBID']
            #command = 'cd ' + submitfn + '; /home4/smita/lib/python/Python-2.7.2/bin/python2.7 ' + filename + ' ' + writeTimesFilename + ' ' + plotFileName + ' ' + session["wrthz"]
            command = 'cd ' + submitfn + '; python2.7 ' + filename + ' ' + writeTimesFilename + ' ' + plotFileName + ' ' + session["wrthz"] + ' ' + job_id
            log.info("Command: %s" % command)
            #plot_file = resource.raw(command)
            plotscript_feedback = resource.raw(command)
            log.debug("feedback from script: %s", plotscript_feedback)
            log.debug("Type of plotscript_feedback[0]:  %s", type(plotscript_feedback[0]))
            log.debug("feedback[0]: %s", plotscript_feedback[0])
            #feedback_dict = {}
            try:
                feedback_dict = eval(plotscript_feedback[0])
            except Exception as e:
                #error occured
                feedback['error'] = 'true'
                feedback['message'] = e
                log.error('Error occured: %s', e)
                return json.dumps(feedback)
            if(feedback_dict['error'] == 'false'):  #if not error
                log.debug("feedback error: %s", feedback_dict['error'])
                log.debug("feedback message: %s", feedback_dict['message'])           
            else:
                log.error('Error occured: %s', feedback_dict['message'])
                return json.dumps(feedback_dict)
        elif feedback['error'] == 'false':
            #log.debug("Error checking file: %s" % feedback['error'])
            #return ''
            log.debug("Error checking file: %s" % feedback['error'])
            msg = "Error checking file: %s" % feedback['message']
            returnFeedback = { 'error' : 'true', 'message' : msg}
            return json.dumps(returnFeedback)
        else:
            feedback_dict = {}
        #if not error get the image data streams
        #image = self.getPlot( c.hostname, target, plotFileName)
        #return image
        feedback_dict['image'], er = self.getPlot( c.hostname, target, plotFileName)
        log.debug("Type of c variable: %s", type(c))
        log.debug("Type of feedback_dict variable: %s", type(feedback_dict))
        feedback_dict['parameters'] = []
        #returnOption = {'name':optionName, 'label': Label,'values':optionValues}
        # log.debug('Return Variable: %s' , returnOption)
        print json.dumps(feedback_dict)
        return json.dumps(feedback_dict)

    def createCumulativeTimePlot(self):
        jodis = app_globals.jodis
        c.hostname = session[SESS_KEY]['right']['host']
        c.job_path = session[SESS_KEY]['right']['path']
        plotFileName = "cumulativeTimePlot.png"
        target = c.job_path + '/' 
        #+ 'INFO/'
        log.debug("c.hostname: %s", c.hostname)
        #c.hostname = 'dolphin.sdsu.edu'
        
        # check if the plot is already created
        feedback = self.checkIfImagePresent(plotFileName, target)
        
        if(feedback['error'] != 'true' and (feedback['result'] == "false" or feedback['plotNew'] == "true")):
            # create new plot only id plot was not created previously and was not create one week back
            try:
                resource = app_globals.jodis.manager.getResource(c.hostname)
                if not resource:
                    log.error('Connection to %s is dead!!!' % c.hostname)
                    return []
            except Exception as e:
                output = e.message
            
            try:
                resource_id =  meta.Session.query(model.Resource).filter(model.Resource.name == resource.host).first().id
                service_id = resource.account.service_id
            except Exception as e:
                log.error('Problem creating job: %s', e)
                session['error_flash'] = 'Missing data input'
                session.save()
                return e
                   
            #c.job_path = session[SESS_KEY]['job_path']
            #jobPathElements = c.job_path.split('/')
            #jobName = jobPathElements[-1]
            
            # scp the localscript file to remote host in PARA folder of the job selected
            filename = 'cumulative.time.plot.py';
            source_dir = 'localscripts'
            source = os.path.join(source_dir, filename)
            full_path =  os.path.abspath(source)
            target = c.job_path + '/'
            # + 'INFO/' # + jobName + '.info/PARAM/'
            host_name = session['available_resources'][c.hostname]['hostname']
            feedback = resource.ssh.scp(None,None,full_path,resource.ssh.user,host_name,target)
            log.debug("SCP RESULT: %s", feedback)
            
            #run the script which was just copied to remote host
            submitfn = target
            writeTimesFilename = 'writetimes.dat'
            plotFileName = "cumulativeTimePlot.png"
            job_id = session['JOBID']
            #command = 'cd ' + submitfn + '; /home4/smita/lib/python/Python-2.7.2/bin/python2.7 ' + filename + ' ' + writeTimesFilename + ' ' + plotFileName + ' ' + session["wrthz"]
            command = 'cd ' + submitfn + '; python2.7 ' + filename + ' ' + writeTimesFilename + ' ' + plotFileName + ' ' + session["wrthz"] + ' ' + job_id
            #command = 'cd ' + submitfn + '; pwd'
            log.info("Command: %s" % command)
            #plot_file = resource.raw(command)
            plotscript_feedback = resource.raw(command)
            log.debug("feedback from script: %s", plotscript_feedback)
            log.debug("Type of plotscript_feedback[0]:  %s", type(plotscript_feedback[0]))
            log.debug("feedback[0]: %s", plotscript_feedback[0])
            #feedback_dict = {}
            try:
                feedback_dict = eval(plotscript_feedback[0])
            except Exception as e:
                #error occured
                feedback['error'] = 'true'
                feedback['message'] = e
                log.error('Error occured: %s', e)
                return json.dumps(feedback)
            if(feedback_dict['error'] == 'false'):  #if not error
                log.debug("feedback error: %s", feedback_dict['error'])
                log.debug("feedback message: %s", feedback_dict['message'])           
            else:
                log.error('Error occured: %s', feedback_dict['message'])
                return json.dumps(feedback_dict)
        elif feedback['error'] == 'true':
            log.debug("Error checking file: %s" % feedback['error'])
            msg = "Error checking file: %s" % feedback['message']
            returnFeedback = { 'error' : 'true', 'message' : msg}
            return json.dumps(returnFeedback)
        else:
            feedback_dict = {}
        #if not error get the image data streams
        #image = self.getPlot( c.hostname, target, plotFileName)
        #return image
        feedback_dict['image'], er = self.getPlot( c.hostname, target, plotFileName)
        log.debug("Type of c variable: %s", type(c))
        log.debug("Type of feedback_dict variable: %s", type(feedback_dict))
        feedback_dict['parameters'] = []
        #returnOption = {'name':optionName, 'label': Label,'values':optionValues}
        # log.debug('Return Variable: %s' , returnOption)
        print json.dumps(feedback_dict)
        return json.dumps(feedback_dict)
    

    def createRunTimePlot(self):
        jodis = app_globals.jodis
        c.hostname = session[SESS_KEY]['right']['host']
        c.job_path = session[SESS_KEY]['right']['path']
        
        log.debug("Hostname (session[SESS_KEY]['right']['host']): %s", session[SESS_KEY]['right']['host'])
        log.debug("Job_PATH (session[SESS_KEY]['right']['path']): %s", session[SESS_KEY]['right']['path'])
        
        plotFileName = "RunTimePlot.png"
        target = c.job_path + '/'
        # + 'INFO/'
        log.debug("c.hostname: %s", c.hostname)
        #c.hostname = 'dolphin.sdsu.edu'
        
        # check if the plot is already created
        feedback = self.checkIfImagePresent(plotFileName, target)
        
        if(feedback['error'] != 'true' and (feedback['result'] == "false" or feedback['plotNew'] == "true")):
            # create new plot only id plot was not created previously and was not create one week back
            try:
                resource = app_globals.jodis.manager.getResource(c.hostname)
                if not resource:
                    log.error('Connection to %s is dead!!!' % c.hostname)
                    return []
            except Exception as e:
                output = e.message
            
            try:
                resource_id =  meta.Session.query(model.Resource).filter(model.Resource.name == resource.host).first().id
                service_id = resource.account.service_id
            except Exception as e:
                log.error('Problem creating job: %s', e)
                session['error_flash'] = 'Missing data input'
                session.save()
                return e
                   
            #c.job_path = session[SESS_KEY]['job_path']
            #obPathElements = c.job_path.split('/')
            #jobName = jobPathElements[-1]
            
            # scp the localscript file to remote host in PARA folder of the job selected
            filename = 'run_time_script.py';
            source_dir = 'localscripts'
            source = os.path.join(source_dir, filename)
            full_path =  os.path.abspath(source)
            target = c.job_path + '/' 
            #+ 'INFO/' # + jobName + '.info/PARAM/'
            host_name = session['available_resources'][c.hostname]['hostname']
            feedback = resource.ssh.scp(None,None,full_path,resource.ssh.user,host_name,target)
            log.debug("SCP RESULT: %s", feedback)
            
            #run the script which was just copied to remote host
            submitfn = target
            writeTimesFilename = 'writetimes.dat'
            plotFileName = "RunTimePlot.png"
            job_id = session['JOBID']
            wrthz = session['wrthz']
            #command = 'cd ' + submitfn + '; /home4/smita/lib/python/Python-2.7.2/bin/python2.7 ' + filename + ' ' + writeTimesFilename + ' ' + plotFileName + ' 10' #remove hard coded WrtFreq = 10 
            command = 'cd ' + submitfn + '; python2.7 ' + filename + ' ' + writeTimesFilename + ' ' + plotFileName + ' ' + wrthz + ' ' + job_id#' 10' #remove hard coded WrtFreq = 10 
            #command = 'cd ' + submitfn + '; pwd'
            log.info("Command: %s" % command)
            plotscript_feedback = resource.raw(command)
            log.debug("feedback from script: %s", plotscript_feedback)
            log.debug("Type of plotscript_feedback[0]:  %s", type(plotscript_feedback[0]))
            log.debug("feedback[0]: %s", plotscript_feedback[0])
            #feedback_dict = {}
            try:
                feedback_dict = eval(plotscript_feedback[0])
            except Exception as e:
                #error occured
                log.error('Error occured: %s', e)
                feedback_dict['error'] = 'true'
                feedback_dict['message'] = e
                return json.dumps(feedback_dict)
            if(feedback_dict['error'] == 'false'):  #if not error
                log.debug("feedback error: %s", feedback_dict['error'])
                log.debug("feedback message: %s", feedback_dict['message'])           
            else:
                log.error('Error occured: %s', feedback_dict['message'])
                return json.dumps(feedback_dict)
        elif feedback['error'] == 'true':
            msg = "Error checking file: %s" % feedback['message']
            returnFeedback = { 'error' : 'true', 'message' : msg}
            return json.dumps(returnFeedback)
        else:
            feedback_dict = {}
        #if not error get the image data streams
        feedback_dict['image'], er = self.getPlot( c.hostname, target, plotFileName)
        log.debug("Type of c variable: %s", type(c))
        log.debug("Type of feedback_dict variable: %s", type(feedback_dict))
        feedback_dict['parameters'] = []
        #returnOption = {'name':optionName, 'label': Label,'values':optionValues}
        # log.debug('Return Variable: %s' , returnOption)
        print json.dumps(feedback_dict)
        return json.dumps(feedback_dict)
    
    
    def selectJobSSH(self):
        c.plots = Viz.plots
        
        # get paramters from frontend
        c.hostname = session[SESS_KEY]['right']['host']
        c.job_path = request.params.get('job_path').decode('latin1')
        
        #Store job path in session
        session[SESS_KEY]['right']['path'] = c.job_path
        
        log.debug("Job Selected and the job path gets stored in session variable......")
        log.debug("session[SESS_KEY]['right']['path'] : %s", session[SESS_KEY]['right']['path'])
        
        c.filename = request.params.get('file_name').decode('latin1')
        scriptname = session[SESS_KEY]['right']['path']
        script = scriptname + '.py'
        scriptdir = "/cyberweb/localscripts"
        c.cmd = '%s/%s ' % (scriptdir,script)
        c.command = "ls -l";
        
        jodis = app_globals.jodis

        
        try:
            resource = app_globals.jodis.manager.getResource(c.hostname)
            if not resource:
                log.error('Connection to %s is dead!!!' % c.hostname)
                return []
        except Exception as e:
            output = e.message
        
        log.debug("USER IS: %s", resource.ssh.user)
        
        try:
            resource_id =  meta.Session.query(model.Resource).filter(model.Resource.name == resource.host).first().id
            service_id = resource.account.service_id
            if not service_id: raise
        except Exception as e:
            log.error('Problem creating job: %s', e)
            session['error_flash'] = 'Missing data input'
            session.save()
            return e
                
        jobPathElements = c.job_path.split('/')
        jobName = jobPathElements[-1]
        
        # scp the localscript file to remote host in PARA folder of the job selected        
        filename = 'read.job.summary.ssh.py';
        source_dir = 'localscripts'
        source = os.path.join(source_dir, filename)
        full_path =  os.path.abspath(source)
        target = c.job_path 
        #job_id = session['JOBID']
        #+ '/' + 'INFO'
        host_name = session['available_resources'][c.hostname]['hostname']
        feedback = resource.ssh.scp(None,None,full_path,resource.ssh.user,host_name,target)
        log.debug("SCP RESULT: %s", feedback)
        
        #run the script which was just copied to remote host
        submitfn = target
        #command = 'cd ' + submitfn + '; /home4/smita/lib/python/Python-2.7.2/bin/python2.7 ' + filename + ' ' + host_name
        command = 'cd ' + submitfn + '; python2.7 ' + filename + ' ' + host_name + ' ' + target
        print command
        plotscript_feedback = resource.raw(command)
        log.debug("feedback[0]: %s", plotscript_feedback[0])
        # Storing analytics data in session for future plotting of images
        try:
            feedback_dict = eval(plotscript_feedback[0])
        except Exception as e:
            #error occured
            log.error('Error occured: %s', e)
            feedback_dict = {}
            feedback_dict['error'] = 'true'
            feedback_dict['message'] = e
            return json.dumps(feedback_dict)
        if feedback_dict['error'] == 'true':
            return json.dumps(feedback_dict)
        else:
            print "File Contents:"
            print feedback_dict['message']
            output = feedback_dict['message']
            lines = output.split('\\n')
            lineValues = [x for x in lines if x != '\n']
            html_output = "<br />".join(lineValues)
            feedback_dict['message'] = html_output
            print "html_output"
            print html_output
            for i in range(0, len(lineValues)):                
                values = lineValues[i].split('=')
                name = values[0].strip()
                data = values[1].strip()
                session[name] = data
        """
        if not output:
            return ''
        else:
            lineValues = output[0].split('\n')
            for i in range(1, len(lineValues)):
                values = lineValues[i].split('=')
                name = values[0].strip()
                data = values[1].strip()
                session[name] = data
        """
                
        session.save()
        print "Session"
        print session
        print "\n\n\n"
        return json.dumps(feedback_dict)

    def getNextOptions(self):
        
        optionName = request.params.get('optionName')
        optionLabel = request.params.get('optionLabel')
        # log.debug('Option Name: %s' , optionName)
        # log.debug('Option Label: %s' , optionLabel)
        returnOption = ''
        if(optionName == '' or optionLabel == ''):
            return json.dumps(returnOption)
        Label = ''
        if not c.plots[optionLabel]:
            return json.dumps(returnOption)
        else:
            for item in c.plots[optionLabel]:
                if(item['name'] == optionName):
                    Label = item['label']
                    SubtypeName = item['subtype']
            # log.debug('Label: %s' , Label)
            optionValues = c.plots[optionName]
            returnOption = {'name':optionName, 'label': Label, 'subtype' : SubtypeName, 'values':optionValues}
            # log.debug('Return Variable: %s' , returnOption)
        return json.dumps(returnOption)
        

    def createRemoteScript(self):
        output = 'false'
        
        # get host name and dir path
        c.hostname = session[SESS_KEY]['right']['host']
        c.job_path = request.params.get('job_path').decode('latin1')
        
        try:
            resource = app_globals.jodis.manager.getResource(c.hostname)
            if not resource:
                log.error('Connection to %s is dead!!!' % c.hostname)
                return []
        except Exception as e:
            output = e.message
        
        try:
            resource_id =  meta.Session.query(model.Resource).filter(model.Resource.name == resource.host).first().id
        except Exception as e:
            log.error('Problem creating job: %s', e)
            session['error_flash'] = 'Missing data input'
            session.save()
            return redirect(url(controller='postjob', action = 'index'))

        script =  "#\!/bin/bash\n"
        script += "PATH=$PATH:/usr/bin\n"
        script += "ls -al"
        filename = "scriptfile"
        commands = ('echo \'%s\' > %s' % (script, filename) )
        
        resource.raw(commands)
        
        c.jobname = ''
        sj = app_globals.jodis.createJob(service.id, session.get('user_id',0), c.jobname)
        c.jobid = sj.id
        c.jobname = sj.name
                
        sj.addTask(submitfile=filename)
        qsub_result = app_globals.jodis.submitJob(sj.name)
        if qsub_result:
            sj.start()
        else:
            log.error('Job submission didn\'t return anything. Changing state of %s to error',sj.id)
            sj.error()
        
        output = 'success'
        return output
    
    
    def getWidget(self, plot_type):
        log.debug("Type of plot: %s", plot_type)
        parameters = {}
        if (plot_type == 'bathymetry'):
            parameters =    {
                                'X-min' :  {
                                                'value' : '',
                                                'type' : 'input'
                                           },
                                'X-max' :  {
                                                'value' : '',
                                                'type' : 'input'
                                           },
                                'Y-min' :  {
                                                'value' : '',
                                                'type' : 'input'
                                           },
                                'Y-max' :  {
                                                'value' : '',
                                                'type' : 'input'
                                           },
                                'Z-min' :  {
                                                'value' : '',
                                                'type' : 'input'
                                           },
                                'Z-max' :  {
                                                'value' : '',
                                                'type' : 'input'
                                           },
                                'Title' :  {
                                                'value' : '',
                                                'type' : 'textarea'
                                           }
                            }
        return parameters
    
    
    
    
    
        
