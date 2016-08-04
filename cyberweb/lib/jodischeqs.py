'''
Created on Mar 26, 2011

@author: carny
'''
import logging

import os
import math
from resource_manager import Manager

#from sqlalchemy.orm.attributes import manager_of_class as manager

from cyberweb.lib import Jodis


log = logging.getLogger(__name__)

class JodisCHEQS(Jodis):
    '''
    This class is the core backend of the gateway. The web service and
    WSDL will plug into this class.
    '''

    def __init__(self, manager, config={}, jobdir=None, jobstem=None):
        Jodis.__init__(manager, config, jobdir, jobstem)
        self.tasklist = {'file':[], 'string':[]}

    def addTasks(self, file=None, string=None):
        '''
        Add tasks to our list. Tasks can be added in the form of a JSON string
        or a file containing these JSON strings (one per line).
        They will be stored as one aggregate list to be parsed when
        all the jobs are added
        '''
        if file:
            if os.path.isfile(file):
                for _ in open(file, 'r'):
                    self.tasks += 1
                self.tasklist['file'].append(file)
                return True
            return False
        if string:
            self.tasks += len(string.strip().split('\n'))
            self.tasklist['string'].append(string)
            return True

        return False

    def clearTasks(self):
        '''
        Clear the queue of tasks.
        '''

        self.tasks = 0
        self.tasklist = {'file':[], 'string':[]}
        self.jobtracker = {}

        import time
        self.jobdir = time.strftime('dist_%Y%m%d_%H%M%S')
        self.jobstem = time.strftime('dist_%Y%m%d_%H%M%S')

        return True

    def splitTasks(self, maxJobs=0, minTasks=10):
        '''
        Split the tasks in the queue into sizeable chunks which will later be
        dispersed across the various resources.
        '''

        # Create a directory to write our job files (if not already done)
        if not os.path.isdir(self.jobdir):
            os.mkdir(self.jobdir)

        # Find the maximum number of jobs
        if not maxJobs:
            maxJobs = self.manager.getMaxJobs()
        elif maxJobs > self.manager.getMaxJobs():
            log.warn('Specified jobs exceeds maximum allowed on resources. Resizing.')
            maxJobs = self.manager.getMaxJobs()

        # Check if we're allowed any jobs.
        if not maxJobs:
            log.warn('Error: 0 jobs allowed on resources!')
            return
        else:
            log.debug('Maximum # of jobs: %d' % maxJobs)

        # Caculate the number of jobs we need and how many tasks we need per job
        # Tasks are naively dispersed across jobs. Currently jobs are dispersed
        # naively to the resources. Only the maximum number of jobs for the
        # resources is known.
        tasksPerJob = self.tasks/maxJobs
        if tasksPerJob < minTasks:
            tasksPerJob = minTasks
        jobs = int(math.ceil(self.tasks/tasksPerJob))

        # Open up job files
        self.jobfiles = []
        jobhandles = []
        for i in range(0, jobs):
            try:
                file = '%s/%s_%04d.in' % (self.jobdir, self.jobstem, i)
                f = open(file, 'w')
            except IOError:
                log.error("Can't write to file %s" % file)
            else:
                self.jobfiles.append(file)
                log.debug('Adding job file: %s' % file)
                jobhandles.append(f)

        # Iterate original job files
        thisjob = 0
        jobcursor = jobhandles.pop()
        for file in self.tasklist['file']:
            try:
                f = open(file, 'r')
            except:
                log.warn("Can't read input file %s." % file)
                return False
            chunk = f.read(5000)
            while chunk:
                next = f.read(5000)
                if not next:
                    chunk = chunk.strip()
                numtasks = len(chunk.split('\n'))

                # Write out tasks
                try:
                    jobcursor.write(chunk)
                except Exception:
                    pass
                else:
                    thisjob += numtasks

                if thisjob >= tasksPerJob and len(jobhandles):
                    jobcursor.close()
                    jobcursor = jobhandles.pop()
                    thisjob = 0

                chunk = next

        for string in self.tasklist['string']:
            for task in string.strip().split('\n'):
                try:
                    jobcursor.write(task + '\n')
                except Exception:
                    pass
                else:
                    thisjob += 1

                if thisjob >= tasksPerJob and len(jobhandles):
                    jobcursor.close()
                    jobcursor = jobhandles.pop()
                    thisjob = 0

        try:
            jobcursor.close()
        except Exception:
            pass

    def jobFinished(self):
        for k, jobarray in self.jobtracker.iteritems():
            for jobfile in jobarray:
                stdout, stderr = self.manager.getResource(k).raw('ls %s.fini' % jobfile)
                if len(stdout) == 0 or (len(stdout) > 0 and stdout.find('No such file') > -1):
                    return False
        return True

    def getResults(self, dsthost=None, dstpath=None):
        output = ''
        for k, jobarray in self.jobtracker.iteritems():
            for jobfile in jobarray:
                basedir = os.path.split(jobfile)[0]
                basename = os.path.splitext(jobfile)[0] if (jobfile[0] == '/' or jobfile[0] == '~') else '~/' + os.path.splitext(jobfile)[0]
                outputfile = basename + '.out'
                scriptoutputfile = basename + '.scriptout'
                logfile = basename + '.in.log'
                log.debug('jobfile: %s' % jobfile)
                log.debug('basename: %s' % basename)

            if dsthost is not None:
                dstresource = self.manager.getResource(dsthost)
                kresource = self.manager.getResource(k)
                output = dstresource.raw('mkdir %s; cd %s' % (basedir, basedir))
                log.debug('%s: mkdir %s'  % (k, basedir))
                log.debug('%s: output directory: %s' % dstresource.raw('pwd'))

                output = kresource.ssh.scpFrom(None, dsthost, outputfile, basedir)
                scriptoutput = kresource.ssh.scpFrom(None, dsthost, scriptoutputfile, basedir)
                logoutput = kresource.ssh.scpFrom(None, dsthost, logfile, basedir)
                log.debug('Results (%s): %s' % (k, jobfile))
        return output

    def parseResults(self, dsthost=None, dstpath=None):
        output = ''
        for k, jobarray in self.jobtracker.iteritems():
            for jobfile in jobarray:
                basedir = os.path.split(jobfile)[0]
                basename = os.path.splitext(jobfile)[0]
                outputfile = basename + '.out'
                scriptoutputfile = basename + '.scriptout'
                logfile = basename + '.in.log'

                cmd = 'cat %s' % outputfile
                output += '\n' + self.manager.getResource(k).raw(cmd)[0]
                log.debug('Running (%s): %s' % (k, cmd))
        return output.split()

    def calcStats(self):
        return True


    def submitJobs(self):
        if not len(self.jobfiles):
            log.warn("No jobs to run")
            return

        retVal = True
        jobindex = 0
        # Iterate through the resources
        for host, resource in self.manager.iterResources():
            # Grab host config settings
            hostconfig = resource.config
            java = hostconfig.java1_6 if hostconfig.get('java1_6') else 'java'
            workingdir = hostconfig.workingdir if hostconfig.get('workingdir') else '~'

            # Make the data dir
            jobdir = self.jobdir
            resource.raw('mkdir %s' % os.path.join(workingdir, jobdir))

            appdir = 'cheqs'
            app = '%s -cp %s/CHEQSApplet.jar:cheqs CHEQSWrapperApp' % (java, appdir)

            if not self.jobtracker.has_key(host) and self.manager.getHostMax(host):
                self.jobtracker[host] = []

            for i in range(0, self.manager.getHostMax(host)):
                log.debug('%s:%s', host, self.manager.getHostMax(host))

                # job input file already created in the self.jobdir directory
                inputfile = '%s' % self.jobfiles[jobindex]
                submitfile = '%s/%s_%04d.submit' % (jobdir, self.jobstem, i)
                t_inputfile = os.path.join(workingdir, inputfile)
                t_submitfile = os.path.join(workingdir, submitfile)
                resultfile = '%s/%s/%s_%04d.out' % (workingdir, jobdir, self.jobstem, i)
                outputfile = '%s/%s/%s_%04d.scriptout' % (workingdir, jobdir, self.jobstem, i)
                errorfile = '%s/%s/%s_%04d.err' % (workingdir, jobdir, self.jobstem, i)

                # Write the command to file and submit.
                appargs = [t_inputfile, resultfile]
                command = 'echo %s;%s %s' % (resultfile, app, ' '.join(appargs))
                log.debug('submit: %s', command)
                #resource.writefile(submitfile, command)

                # Create the job submit file. This will be used in the qsub process
                # and for error checking later
                submitscript = resource.jobScript(command, self.jobstem, outputfile, errorfile)
                try:
                    with open(submitfile, 'w') as fh:
                        fh.write(submitscript)
                except:
                    log.error("Can't write submit script %s" % submitfile)

                # Upload files
                resource.upload(submitfile, None, '%s/%s' % (workingdir, jobdir))
                resource.upload(inputfile, None, '%s/%s' % (workingdir, jobdir))

                # Submit job
                resource.submitJob(app=t_submitfile)
                self.jobtracker[host].append(t_inputfile)

                # Increment job index. Return if there are no more jobs to submit.
                jobindex += 1
                if jobindex >= len(self.jobfiles):
                    return retVal

        # Upload job files
        # Run jobs
        return retVal
