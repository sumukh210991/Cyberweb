import logging
import os
import traceback
import time
from datetime import datetime
from time import strftime

from pylons import config, request, response, session, app_globals, url, tmpl_context as c
from pylons.controllers.util import redirect
import sqlalchemy as sa

from authkit.authorize.pylons_adaptors import authorize

from cyberweb import model
from cyberweb.model import meta, JobState, AuthKey, Resource, Account, Service
from cyberweb.lib.base import BaseController, render
from cyberweb.lib.jodis import sshresource as myssh, resources
from cyberweb.lib import auth, helpers as h, jobs as j, Gccom

log = logging.getLogger(__name__)
all__ = ['batchScript_PBS']
class GccomController(BaseController):
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
        user_id = session.get('user_id')
        c.title = 'UCOAM Project:' + ' Recent Job Summary for:  ' + session['user']
        numJobs = 10
        c.jobheaders       =j.getJobHeaders()

        c.jobs         = j.jobMonitor(self, session.get('user_id'), numJobs)
        print c.jobs
        c.jobstates    = j.getJobStateNames()
        c.jobstatekeys = j.getJobStateKeys()
        d=dict()
        for i in range(len( c.jobstatekeys )):
             d[c.jobstatekeys[i]]= c.jobstates[i]
        c.jobstateheaders = d
        c.resources_user = session['available_resources']
        ###c.resources_user = h.get_user_resources(user_id)
        log.debug('GCOM: AVAIL USER RES= %s',c.resources_user)
        log.debug('GCOM: AVAIL RES= %s',session['available_resources'])
        return render('/gcem/gccom/gccom.mako')
    
    ####################################################################
    # GCOM demos
    ####################################################################
    def demo(self):
        c.title = 'GCOM Demo Jobs.'
        return render('/gcem/gccom/gccom_demo.mako')
    
    def demo_ldc2(self): return self._gccom_jobs('ldc2','demo')
    def demo_seamount1(self): return self._gccom_jobs('seamount1','demo')
    def demo_temperature1(self): return self._gccom_jobs('temperature1','demo')
    def demo_temperature2(self): return self._gccom_jobs('temperature2','demo')
    
    ####################################################################
    # GCOM test
    ####################################################################
    def test(self):
        c.title = 'GCOM Test Jobs.'
        return render('/gcem/gccom/gccom_test.mako')

    def test_ldc2(self): return self._gccom_jobs('ldc2','test')
    def test_seamount1(self): return self._gccom_jobs('seamount1','test')
    def test_temperature1(self): return self._gccom_jobs('temperature1','test')
    def test_temperature2(self): return self._gccom_jobs('temperature2','test')


    #####
    # Functions used to run the above tests and demos
    #####
    def _gccom_jobs(self, model_key, mode):
        c.jobstate          = 'build'
        c.jobmsg            = 'build: setting up the job. before submission.'
        c.model_key         = model_key
        c.mode              = mode
        c.error_flash       = None
        if session.has_key('error_flash'):
            c.error_flash = session['error_flash']
            try: del session['error_flash']
            except Exception as _: pass
        c.jobname           = '%s_%s' % (model_key, mode)
        c.cwuser            = session.get('user','user')
        c.acct              = Gccom.gccom_comm_acct
        c.model_param_hdrs  = Gccom.model_params['hdrs']
        c.model_params      = Gccom.model_params[c.model_key]
        c.model_desc        = str(Gccom.model_info[c.model_key]['desc'])
        c.title             = 'GCOM %s Simulation: Model:%s for JobName: %s' % (
                                   c.mode, str(c.model_desc), c.jobname)

        c.resources = h.get_user_resources(session.get('user_id'))
        c.hostname  = c.resources.keys()[0] if c.resources else ''     #used to init/set default host; reset later 

        c.grid_key          = Gccom.model_info[c.model_key]['grid_key']
        c.grid_imax         = Gccom.bath_grid[c.grid_key]['IMax']
        c.grid_jmax         = Gccom.bath_grid[c.grid_key]['JMax']
        c.grid_kmax         = Gccom.bath_grid[c.grid_key]['KMax']
        c.grid_name         = Gccom.bath_grid[c.grid_key]['name']
        c.grid_fname        = Gccom.bath_grid[c.grid_key]['fname']
        log.info( 'GCOM:: gccom_jobs:  building form data for model_key=%s, desc=%s, jobstate= %s, jobname= %s, gridname= %s, gridfnam=%s' % (c.model_key, c.model_desc,c.jobstate, c.jobname, c.grid_name, c.grid_fname))
        return render('/gcem/gccom/app_' + c.mode.lower() + '.mako')

    def app_jobs_action(self):
        mode = request.params.get('mode','').decode()
        model_key = request.params.get('model_key','').decode()
        model = {
                 'cwuser' : session.get('user','user'),
                 'model_key' : request.params.get('model_key','').decode(),
                 'acct' :  Gccom.gccom_comm_acct,
                 'model_desc' : Gccom.model_info[model_key]['desc'],
                 'title' : 'GCOM Demo: %s Test Case for user %s' % (Gccom.model_info[model_key]['desc'], session.get('user','user')),
                 'jobstate' : request.params.get('jobstate','').decode(),
                 'hostname' : request.params.get('hostname','').decode(),
                 'jobname' : request.params.get('jobname','').decode()
                 }
        if not model.get('jobstate'):
            log.error('Jobstate: not defined')
            return redirect(url(controller='gccom', action = '%s_%s' % (mode.lower(), model_key) ))

        log.info( 'GCOM Job Action: Exec JobName= %s , action= %s, host= %s' % (
                  model['jobname'],model['jobstate'],model['hostname']) )
        return self._rungccom(request.params, model, mode)

    def _rungccom(self, reqparams, model_dict, mode):
        # Static strings for template (stateless)
        dbgstr='';
        errstr='';
        c.cwuser = session['user_id']
        c.account_id = int(model_dict['hostname'])
        resource = app_globals.jodis.manager.getResource(c.account_id)
        log.info('GCOM HOSTNAME= %s' % resource.host)
        c.mode = mode
        c.menu = 'gccom_%s' % c.mode
        c.model_param_hdrs = Gccom.model_params['hdrs']
        c.model_key = model_dict['model_key']
        c.grid_key = Gccom.model_info[c.model_key]['grid_key']
        for i in ['name', 'IMax', 'JMax', 'KMax']:
            setattr(c, 'grid_%s' % i.lower(), Gccom.bath_grid[c.grid_key][i])
        session.setdefault(c.model_key, {})

        for k, v in model_dict.items():
            setattr(c, k, v)

        if c.jobstate == 'submit':
            log.debug('submit job')
            for i in ('jobstate','hostname', 'jobname','model_params','mode','jobdescription'):
                session[c.model_key][i] = reqparams.get(i,'')
                setattr(c, i, session[c.model_key][i])
                if i == 'model_params':
                    # This is not secure at all
                    session[c.model_key][i] = eval(session[c.model_key][i])

            # Retrieve model parameters & update c.model_params using the form data
            c.model_params = session[c.model_key]['model_params']
            for key, value in dict(reqparams).items():
                if key.strip().endswith('.paramval'):
                    key_str = key.split('.')[0]
                    value_str = str(value) or 'none'
                    count = 0
                    for i in c.model_params:
                        if key_str.find(str(i[0])) >= 0:
                            c.model_params[count][2] = value_str
                            count += 1

            # build parameter file and copy to host 
            paramfilestr = '&params\n'
            for p in c.model_params:
                paramfilestr += ('%s = %s      ! %s\n' % ( p[0], p[2], p[1]) )
            paramfilestr += '/\n'

            # Create job. This gives us jobid and creates a unique name
            try:
                account = meta.Session.query(Account).filter(Account.id == int(c.account_id)).first()
                if not account: raise
                log.debug('GCOMJOB: acct[uname: %s, res_id: %s, serv_id: %s], account_id: %d' , \
                           account.username, account.resource_id, account.service_id, account.id)
                service = meta.Session.query(Service).filter(Service.id == account.service_id).first()
                if not service: raise
            except Exception as e:
                errstr = 'Problem creating job on hostname: %s, err: %s' % (resource.host, str(e))
                log.error(errstr)
                session['error_flash'] = [errstr]
                session.save()
                return redirect(url(controller='gccom', action = '%s_%s' % (c.mode.lower(), c.model_key) ))
            infostr = ('GCOMJOB: [JobName: %s] [hostname: %s, accountID: %d] [Serv: ID=%s, %s @ %s] ' % ( \
                       c.jobname, resource.host, account.id, service.id, service.service_name, service.resource ) )
            log.info(infostr)
            sj = app_globals.jodis.createJob(service.id, session.get('user_id', 0), c.jobname)
            c.jobid = sj.id
            c.jobname = sj.name
            log.info('GCOMJOB: jobname:%s,  jobid: %s' % (c.jobname,c.jobid) )

            # Copy the session data from the setup model_key dictionary to the job id.
            # We then delete the model_key dictionary so that the user can start a new job
            # with no conflicts.
            session[c.jobid] = {1:{}}
            mytask = session.get(c.model_key, {}).copy()
            if not mytask.keys():
                log.error('Uh oh! We have session no data for model: %s', c.model_key)
            mytask['jobname'] = c.jobname
            mytask['model_key'] = c.model_key
            mytask['cwuser'] = c.cwuser
            mytask['jobid'] = c.jobid

            dt = strftime('%Y-%m-%d %H:%M:%S')
            del session[c.model_key]

            # get cyberweb home dir
            (home,err)  = resource.raw('pwd')
            # directories and file names for job to be run
            userdir           = ('%s/%s/%s' % (home,config.get('cw.cwuser_rem','.'), c.cwuser ))
            jobdir            = ('%s/%s' % ( userdir,c.jobname) )
            mytask['userdir'] = userdir

            # remote host: make the job directory for job using jobid  (cwrj_)
            cmd     = ('mkdir -p %s' % jobdir )
            out, err = resource.raw( cmd )
            log.info("GCOMJOB: mkdir userdir: output:[ %s], error:[%s]",out.splitlines(),err.splitlines())

            gcemdir       = ('%s/%s'  % (home, Gccom.gcem_dir) )
            gccomdir      = ('%s/%s'  % (gcemdir, Gccom.gccom_dir ) )
            modelname     = Gccom.model_info[c.model_key]['modelname']
            modeldir      = ('%s/%s'  % (gccomdir, c.model_key) ) 
            ###job_modelname = ('%s/%s'  % (jobdir,modelname))
            job_modelname = ('%s/%s'  % (jobdir, Gccom.model_info[c.model_key]['modelname'] ) )
            log.debug('GCOMJOB: TRY to copy model files: FROM: %s, TO: %s\n\n ' , modeldir, jobdir )
            # move GCOM model files over to job dir; rename for job runs
            out,err = resource.raw('cp -r %s/* %s' % (modeldir, jobdir) )
            log.debug('GCOMJOB: CP STATUS: OUT: %s \nERR: %s\n' , out.splitlines(), err.splitlines() )


            # rename application to include jobID
            fname_old   = job_modelname
            job_modelname  = '%s.%s' % (fname_old, str(c.jobid))
            resource.raw('mv %s %s' % (fname_old, job_modelname))
            resource.raw('chmod 755 %s/' % (modelname))
            out,err = resource.raw('ls -al %s' % jobdir )
            log.debug('GCOMJOB: DIR: %s \n LISTING: OUT:  %s \n ERR: %s\n' ,jobdir,out.splitlines(),err.splitlines() )

            ### -------------- GOOD TO HERE  ---------------###
 
            # Create the job submit file. This will be used in the qsub process
            # and for error checking later
            # name of batch script on the remote host
            batchscript_file = ('%s/batch.%s.%s' % (jobdir, modelname, c.jobid))    
            batchscript_contents = self.batchScript_PBS(modelname,c.jobid,jobdir,job_modelname)
            log.debug('After Script Build: batchscript_file: %s\n, CONTENTS: \n  %s', 
                       batchscript_file, batchscript_contents)
            #
            tmpfile = ('/tmp/%s.batch.%s.%s' % (c.cwuser, modelname, c.jobid))
            try:
                with open(tmpfile, 'w') as fh:
                    fh.write( batchscript_contents )
                log.debug('created file: %s',tmpfile)
            except:
                log.error("Can't write batch script %s" % tmpfile)

            # move application files over to job dir and rename
            out = resource.ssh.scp(None, None, tmpfile, resource.ssh.user, resource.host, batchscript_file)
            #out = resource.ssh.scpTo( resource.ssh.user, mytask.get('hostname'), tmpfile, batchscript_file )

            log.debug('GCOMJOB: SCP FROM: %s, TO: %s\n for USER: %s  @ HOST: %s, \n OUT: %s \n  ', \
                tmpfile, batchscript_file, resource.ssh.user, mytask.get('hostname'), out.splitlines() ) 
            sj.addTask(account.id, submitfile=batchscript_file)
            log.debug('GCOMJOB: Task added to JOB_ID: %s', sj.id)

            qsub_result = app_globals.jodis.submitJob(sj.name)
            if qsub_result:
                sj.start()
            else:
                log.error('Job submission didn\'t return anything. Changing state of %s to error', sj.id)
                sj.error()

            # build this array to associate batch queue job id with cw job number.
            if 'qsubid_list' not in mytask:
                mytask['qsubid_list'] = []
            mytask['qsubid_list'].append((sj.id, c.jobid))
            mytask['qsubids'] = sj.id
            c.grid_fname = Gccom.bath_grid[c.grid_key]['fname']
            c.grid_name  = Gccom.bath_grid[c.grid_key]['name']
            gridfname    = Gccom.bath_grid[c.grid_key]['fname']

            fstr = 'JOB HISTORY FOR JOB: ' + str(c.jobname) + '\n'
            fstr += '          Date: ' + dt + '\n'
            fstr += '    Model Type: ' + c.model_key + '\n'
            fstr += '  Submitted By: ' + c.cwuser + '\n'
            fstr += '          Host: ' + mytask['hostname'] + '\n'
            fstr += '       JobName: ' + mytask['jobname'] + '\n'
            fstr += '     Grid Name: ' + c.grid_name + '\n'
            fstr += 'Grid File Name: ' + gridfname + '\n'
            fstr += ('  Problem Size: [%s x %s x %s]\n' % (c.grid_imax, c.grid_jmax, c.grid_kmax))
            fstr += '  Batch Queue Job Info:  ' + mytask['qsubids'] + '\n'

            log.info('queue job history: %s' % fstr)
            resource.raw('echo \"%s\" >> %s/job.history.%s' % (fstr.replace('\n','\\n'), jobdir, c.jobid) )

            fstr =  ('JOBID = %s \\n' % (sj.id) )
            fstr += 'gridname = ' + c.grid_name + '\\n'
            fstr += 'gridfname = ' + gridfname + '\\n'
            fstr += ('Imax = %s \\n' % (c.grid_imax) )
            fstr += ('Jmax = %s \\n' % (c.grid_jmax) )
            fstr += ('Kmax = %s \\n' % (c.grid_kmax) )
            fstr += ('MaxFileNo = %s \\n' % ( Gccom.model_params[c.model_key][2][2]  ) ) 
            fstr += ('wrthz = %s \n' % ( Gccom.model_params[c.model_key][3][2]  ) ) 
            fstr += 'jobtype = ser' + '\\n' 
            fstr += 'PROCS = 1 \\n'
            fstr += 'Pi = 1 \\n'
            fstr += 'Pj = 1 \\n'
            fstr += 'Pk = 1 \\n'

            log.info('queue job info: %s' % fstr)
            resource.raw('echo \"%s\" >> %s/job.info.%s' % (fstr.replace('\n','\\n'), jobdir, c.jobid) )

            log.info('User %s submitted job %s' % (session['user'],mytask['qsubids']))
            c.jobstate = 'submitted'

            # Save the task to the database
            mytaskdb = model.Task(
                              int(c.jobid),
                              queuejob_id=mytask['qsubids'],
                              environment=mytask['hostname'],
                              state=sj.state,
                              type=c.model_key,
                              owner=session['user_id'],
                             )
            try:
                meta.Session.add(mytaskdb)
                meta.Session.commit()
            except:
                log.warn('Couldn\'t commit job')
                meta.Session.rollback()
            else:
                meta.Session.close()
        elif c.jobstate == 'monitor':
            log.info('Redirect to Job Monitor')
            return redirect(url(controller='gccom', action='jobmonitor'))
        else:
            c.jobstate = 'jobstate_error: submit'
            c.jobmsg = 'Invalid job state'
            log.debug(c.jobmsg)
            return render('/gcem/gccom/app_%s.mako' % mode.lower())
        session.save()
        return render('/gcem/gccom/app_%s.mako' % mode.lower())

    def search(inlist, matches):
        for li in inlist:
            for m in matches:
                if m in li:
                    return li
        return None

    def batchScript_PBS(self,jobname,jobid,jobdir, job_modelname):
        scpt = '#!/bin/bash\n'
        ###scpt += 'source /etc/profile\n'
        scpt += '#PBS -V \n'
        #scpt += '#PBS -l nodes=1:ppn=1:reserved \n'
        #scpt += '#PBS -q workq \n'
        jstr = jobdir + '/' + jobname + '.' + jobid 
        scpt += '#PBS -o ' + jstr + '.o${PBS_JOBID} \n'
        scpt += '#PBS -e ' + jstr + '.e${PBS_JOBID} \n'
        #scpt += '#PBS -joe \n'
        scpt += 'echo Working directory is $PBS_O_WORKDIR \n'
        scpt += 'cd ' + jobdir + '  \n'
        ### run 
        ### scpt += 'mpirun /nfs/dolphinfs/home2/mthomas/localscript.sh\n'

        scpt += 'mpiexec -n 1 ' + job_modelname + ' \n'

        scpt += 'echo "------------------------"  \n'
        scpt += 'echo "JOBNAME: " $PBS_JOBNAME  \e'
        scpt += 'echo "Host: " $PBS_O_HOST  \n'
        scpt += 'echo "Working dir: " $PBS_O_WORKDIR\n'
        scpt += 'echo "------------------------"  \n'
        scpt += 'qstat -f $PBS_JOBID > qstat.data\n'
        scpt += 'qstat -f $PBS_JOBID\n'

        return scpt

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
        #log.debug('GCOMJOBSUMMARY: finished jobs:%s', str(c.jobs))
        return render('/gcem/jobsummary.mako')

    def jobmonitor(self):
        numjobs = 20
        c.user = session.get('user_id')
        c.jobname = request.params.get('jobname') or ''
        c.jobs = j.jobMonitor(self, session.get('user_id'), numjobs)
        c.jobstates = j.getJobStateNames()
        c.jobstatekeys = j.getJobStateKeys()
        d = {}
        for i in range(len(c.jobstatekeys)):
            d[c.jobstatekeys[i]] = c.jobstates[i]
        c.jobstateheaders = d
        c.title = config.get('project.shortname', 'CyberWeb') + ' Job Monitor Listing for:  ' + session['user']
        #log.debug('GCOMJOBMONITOR: finished jobs:%s', str(c.jobs))
        return render('/gcem/jobmonitor.mako')

    def sim(self):
        c.title = 'GCOM Simulation Model.'
        return render('/gcem/gccom/gccom_sim.mako')

    def help(self):
        c.title = 'Help for running GCOM model'
        return render('/gcem/gccom/gccom_help.mako')
