"""
.. module:: resources

.. moduleauthor:: Carny Cheng <carny@me.com>

The resource class represents a connection to a computational resource.
"""
import logging
import os
import re
import pexpect
import xml.parsers.expat as xmlparser
import sshresource


log = logging.getLogger(__name__)


class resource():
    """
    Abstract class for a resource. All classes should inherit from this.
    A developer can use this abstract class for use w/ non-queue type resources.
    """
    def __init__(self, host, user, type=None, config=None, app=None, gsissh=False, keyfile=None, account=None, queueservice=None, name=''):
        """ Init method

        Args:
            host: hostname string which to connect to
            user: username
            type: queue system type
            config: dictionary of configuration options
            app: the service this applies to
            gsissh: boolean value of which authentication mechanism to use

        """
        self.name = name
        self.host = host
        self.user = user
        self.outputfile = 'output'
        self.config = config or {}
        self.account = account
        self.app = app
        self.jobs = {}
        try:
            self.bindir = getattr(queueservice, 'bin_dir')
        except AttributeError as _:
            self.bindir = ''
        try:
            self.argstring = getattr(queueservice, 'arg_string')
        except AttributeError as _:
            self.argstring = ''
        if self.argstring:
            self.argstring = self.argstring.replace('None', '')

        self.ssh = sshresource.gsissh(host, user) if gsissh else sshresource.ssh(host, user, keyfile=keyfile)

    def __del__(self):
        """ Disconnect SSH connection on instance deletion

        """
        if hasattr(self, 'ssh') and self.ssh:
            del self.ssh

    def raw(self, *args, **kwargs):
        """ Run a raw command

        """
        return self.ssh.run(*args, **kwargs)

    def upload(self, srcPath, md5, target, srcHost=None, srcUser=None):
        """ Upload a file to the remote machine. This essentially warps the sshresource
        scpTo method.

        Args:
            srcPath: Path of the file(s) on the source machine
            md5: md5 of the file(s) to be uploaded
            target: target path
            srcHost: Optional source host
            srcUser: Optionsal source user

        Return:
            Returns true if the upload was successful

        """
        filename = os.path.basename(srcPath)
        self.ssh.scpTo(srcUser, srcHost, srcPath, target)
        if md5 and md5 == self.ssh.md5('/'.join(target, filename))[0]:
            return True
        return False

    @property
    def appdir(self):
        """ Property of the application dir specified for the resource

        Return:
            Path string of the application directory

        """
        try:
            stdout, stderr = self.raw('pwd')
            return '~/apps' if stdout.find('command not found') > -1 or stderr else os.path.join(stdout.strip(), 'apps')
        except AttributeError:
            pass

        return '~/apps'

    def uploadApp(self, srcPath, md5, srcHost=None, srcUser=None):
        """ Wrapper for the upload method. This specifically uploads the application to be run

        Args:
            srcPath: Path of the file(s) on the source machine
            md5: md5 of the file(s) to be uploaded
            srcHost: Optional source host
            srcUser: Optionsal source user

        Return:
            Returns true if the upload was successful

        """
        targetdir = os.path.join(self.appdir, md5) if md5 else self.appdir
        self.raw('mkdir %s' % self.appdir)
        self.targetfile = os.path.join(targetdir, os.path.basename(srcPath))

        # Test if file exists
        if md5 == self.ssh.md5(self.targetfile)[0]:
            return 2
        # Upload file and test md5
        self.ssh.scpTo(srcUser, srcHost, srcPath, targetdir)
        if md5 == self.ssh.md5(self.targetfile)[0]:
            return True
        return False

    def writefile(self, filename, input_string):
        """ Writes file to the remote machine given a string

        Args:
            filename: Name of the output filename on the target machine
            input_string: The string that is to be written out to the file

        Return:
            Returns true if the file was successfully written

        """
        stdout, stderr = self.raw('echo "%s" > %s' % (input_string, filename))
        if stdout:
            log.debug('stdout: %s', stdout)
            log.debug('stderr: %s', stderr)
            return False
        return True

    def createJobString(self, jobArray=None):
        """ creates the string to submit a job

        Args:
            jobArray: Array of the jobs to be run

        Return:
            Returns the string to run the job

        """
        jobstring = ''
        if jobArray is None:
            jobArray = self.jobs.iterkeys()
        elif not len(jobArray):
            return jobstring

        for i in jobArray:
            jobstring += self.jobstringsep + str(i)

        return jobstring[1:]

    def createJob(self, jobId, jobInfo=None):
        """ Adds the job the array of jobs for this resource

        Args:
            jobId: ID of the job
            jobInfo: Optional dictionary of job information

        Return:
            Returns the object in the array

        """
        jobInfo = jobInfo or {}
        if jobId not in self.jobs:
            self.jobs[jobId] = jobInfo

        return self.jobs[jobId]

    def createParamString(self, params):
        """ Creates the parameter string for job submission given
        the dictionary of parameters

        Args:
            params: Dictionary of parameters to pass to he job

        Return:
            Returns the string of parameters

        """
        paramstring = ''
        if params != None and len(params):
            for k, v in params.iteritems():
                if len(v):
                    paramstring += ' -%s %s' % (k, v)
                else:
                    paramstring += ' -%s' % k
        elif self.config.get('params'):
            for k, v in self.config['params'].items():
                if len(v):
                    paramstring += ' -%s %s' % (k, v)
                else:
                    paramstring += ' -%s' % k

        return paramstring


class sge(resource):
    def __init__(self, *args, **kwargs):
        resource.__init__(self, *args, **kwargs)
        # The regex parses out the IDs out of a string like so....
        # Your job 4244 ("runjava.sh") has been submitted
        self.jobre = re.compile('(?<=Your job )\d+')
        self.jobstringsep = ','
        if self.bindir:
            self.raw('source %s/../../default/common/settings.sh' % self.bindir)
        else:
            self.raw('source /opt/sge-6.2/default/common/settings.sh')
            self.raw('source /opt/sge6.2/default/common/settings.sh')
        self.JAT_state = {16: 'H', 64: 'Q', 2048: 'W', 128: 'R', 256: 'S', 65536: 'S'}

    # Parsing status XML
    def start_element(self, name, attrs):
        self.buffer = ''

    def char_data(self, data):
        self.buffer += data

    def end_element(self, name):
        if name == 'JB_job_number':
            self.getStatus_id = repr(self.buffer.rstrip())
            if self.getStatus_id.lower()[0] == 'u':
                self.getStatus_id = self
        elif name == 'JAT_status':
            statusstring = repr(self.buffer.rstrip())
            if statusstring.lower()[0] == 'u':
                statusstring = statusstring[1:]
            statusstring = statusstring.strip('\'')
            statuscode = int(statusstring)
            self.getStatus_status = self.JAT_state[statuscode] or 'Error'

        if self.getStatus_id and self.getStatus_status:
            self.statusdict[id] = statuscode
            self.statusstring += '%s: %s' % (id, statuscode)
            self.getStatus_id = None
            self.getStatus_status = None

    def getStatus(self):
        if len(self.jobs) == 0:
            return True, {}

        bindir = self.config.bindir if self.config.bindir else ''
        cmd = '%s/qstat -xml -j %s' % (bindir, self.createJobString())
        stdout, stderr = self.raw(cmd)
        if stderr:
            return False, stderr

        self.statusstring = ''
        self.statusdict = {}
        for i in self.jobs:
            self.statusdict[i] = ''
        self.getStatus_id = None
        self.getStatus_status = None
        parser = xmlparser.ParserCreate()
        parser.StartElementHandler = self.start_element
        parser.EndElementHandler = self.end_element
        parser.CharacterDataHandler = self.char_data
        parser.Parse(stdout)

        return True, self.statusdict

    def jobScript(self, appline, jobname='', output='', error=''):
        script = '#!/bin/bash\n'
        if error:
            script += '#$ -e ' + error + '\n'
        if output:
            script += '#$ -o ' + output + '\n'

        script += '#Run App\n'
        script += appline + '\n\n'

        script += 'echo "------------------------"\n'
        script += 'echo "Host: " $HOSTNAME\n'
        script += 'echo "------------------------"\n'
        #script += 'qstat -f $PBS_JOBID'

        return script

    def submitJob(self, params=None, app=None, arguments=None):
        arguments = arguments or []
        self.submitparams = self.createParamString(params)
        if not app:
            app = self.app

        argString = ' '.join(arguments)
        # The environment is not holding across exec_command calls....
        if self.argstring:
            self.argstring = self.argstring.replace('None','')
        cmd = 'source /opt/sge-6.2/default/common/settings.sh;'
        cmd += 'qsub %s %s -S /bin/bash %s %s' % (self.argstring or '', self.submitparams, app, argString)
        stdout, stderr = self.raw(cmd)
        jobstring = stdout
        m = self.jobre.search(jobstring)
        self.lastjob = []
        while m:
            jobid = m.group(0)
            self.createJob(jobid)
            self.lastjob.append(jobid)
            m = self.jobre.search(jobstring, m.end())

        if len(self.jobs) > 0:
            output = '%s jobs submitted.' % len(self.lastjob)
        else:
            output = 'No jobs submitted. Something could be wrong.'
            output += 'stdout:\n' + stdout
            output += '\nstderr:\n' + stderr

        return True, self.lastjob, output

    def getResults(self, filename=None):
        if filename is None:
            filename = self.outputfile
        cmd = 'cat %s' % filename
        stdout, stderr = self.raw(cmd)
        if stderr:
            return False, stderr
        return True, stdout

    def deleteJob(self):
        if len(self.jobs) == 0:
            return True, 'No jobs running or in queue.'
        else:
            cmd = 'qdel %s' % self.createJobString()
            stdout, _ = self.raw(cmd)
        result = "**** qstat -u ****\n%s\n****\n" % stdout
        return True, result


class pbs(resource):
    def __init__(self, *args, **kwargs):
        resource.__init__(self, *args, **kwargs)
        self.jobre = re.compile('(^\d+\.\w+)\.|\n(\d+)$|(\d+(\.(-|\w)+)+\.teragrid\.org)')
        self.jobstringsep = ' '

    def getStatus(self):
        if len(self.jobs) == 0:
            return True, {}

        bindir = self.config.bindir if self.config.bindir else ''
        cmd = '%sqstat %s' % (bindir, self.createJobString())
        stdout, stderr = self.raw(cmd)
        if stderr:
            return False, stderr

        linere = re.compile('^((-|=)|\s)+$')
        indata = False
        self.statusstring = ''
        jobs = {}
        for i in self.jobs:
            jobs[i] = ''
        for line in stdout.split('\n'):
            line = line.strip()
            if linere.search(line):
                indata = True
            elif indata:
                d = line.split()
                if len(d) > 4:
                    job_id = d[0]
                    status = d[4][0].upper() if d[4] else ''
                    jobs[job_id] = status
            else:
                # Header row
                pass

        return True, jobs

    def jobScript(self, appline, jobname='', output='', error=''):
        script = '#!/bin/bash\n'
        if error:
            script += '#PBS -e ' + error + '\n'
        if output:
            script += '#PBS -o ' + output + '\n'

        script += '#Run App\n'
        script += appline + '\n\n'

        script += 'echo "------------------------"\n'
        script += 'echo $PBS_JOBNAME "("$PBS_JOBID")"\n'
        script += 'echo "Host: " $PBS_O_HOST\n'
        script += 'echo "Working dir: " $PBS_O_WORKDIR\n'
        script += 'echo "------------------------"\n'
        script += 'qstat -f $PBS_JOBID'

        return script

    def submitJob(self, params=None, app=None, arguments=[]):
        """Submits a job to the remote resource's queuing mechanism.

        """
        if not app:
            app = self.app

        argumentString = ' '.join(arguments)
        self.submitparams = self.createParamString(params)
        self.config.bindir = '/home/torque/bin/'     # Must set bin dir since env is not holding across commands
        cmd = '%sqsub %s %s %s' % (self.config.bindir, self.submitparams, app, argumentString)
        stdout, stderr = self.raw(cmd)
        print 'output:', stdout
        m = self.jobre.search(stdout)
        self.lastjob = []
        while m:
            for match in m.groups():
                if match:
                    jobid = match
                    self.createJob(jobid)
                    self.lastjob.append(jobid)
                    m = self.jobre.search(stdout, m.end())
                    break

        if len(self.jobs) > 0:
            output = '%s jobs submitted.' % len(self.lastjob)
        else:
            output = 'No jobs submitted. Something could be wrong.'
            output += '\n' + stdout
            output += '\n' + stderr

        return True, self.lastjob, output

    def getResults(self, filename=None):
        if filename is None:
            filename = self.outputfile
        cmd = 'cat %s' % filename
        stdout, stderr = self.raw(cmd)
        if stderr:
            return False, stderr
        return True, stdout

    def deleteJob(self):
        if len(self.jobs) == 0:
            return True, 'No jobs running or in queue.'
        else:
            cmd = 'qdel %s' % self.createJobString()
            stdout, _ = self.raw(cmd)
        result = "**** qstat -u ****\n%s\n****\n" % stdout
        return True, result


class condor(resource):
    def __init__(self, *args, **kwargs):
        resource.__init__(self, *args, **kwargs)
        self.jobstringsep = ' '

    def getStatus(self):
        if len(self.jobs) == 0:
            return True, {}

        cmd = '/usr/local/pbs/bin/qstat %s' % self.createJobString()
        stdout, stderr = self.raw(cmd)
        if stderr:
            return False, stderr

        indata = False
        self.statusstring = ''
        for line in stdout.split('\n'):
            line = line.strip()
            if line.find('ID') > -1 and line.find('SUBMITTED' > -1):
                indata = True
            elif indata:
                d = line.split()
                if len(d) == 8:
                    self.statusstring += '%s: %s' % (d[0], d[5])

        return True, self.statusstring

    def getResults(self):
        return False, 'Not implemented in base class.'

    def submitJob(self):
        return False, [], 'Not implemented in base class.'


class lsf(resource):
    def __init__(self, *args, **kwargs):
        resource.__init__(self, *args, **kwargs)
        self.jobstringsep = ' '
        self.jobre = re.compile('(Job \<)\d+')

    def getStatus(self):
        if len(self.jobs) == 0:
            return True, {}

        bindir = self.config.bindir if self.config.bindir else ''
        cmd = '%sbjobs %s' % (bindir, self.createJobString())
        stdout, stderr = self.raw(cmd)
        if stderr:
            return False, stderr

        linere = re.compile('^((-|=)|\s)+$')
        indata = False
        self.statusstring = ''
        jobs = {}
        for i in self.jobs:
            jobs[i] = ''
        for line in stdout.split('\n'):
            line = line.strip()
            if linere.search(line):
                indata = True
            elif indata:
                d = line.split()
                if len(d) > 4:
                    job_id = d[0]
                    status = d[4][0].upper() if d[4] else ''
                    jobs[job_id] = status
            else:
                # Header row
                pass

        return True, jobs

    def jobScript(self, appline, jobname='', output='', error=''):
        script = '#!/bin/tcsh\n'
        if error:
            script += '#BSUB -e ' + error + '\n'
        if output:
            script += '#BSUB -o ' + output + '\n'

        script += '#BSUB -q normal\n'
        script += '#BSUB -W 7:00\n'
        script += '#BSUB -n 2\n'
        script += '#Run App\n'
        script += appline + '\n\n'

        return script

    def submitJob(self, params=None, app=None, arguments=[]):
        self.submitparams = self.createParamString(params) if params else ''
        if not app:
            app = self.app

        argString = ' '.join(arguments)
        # The environment is not holding across exec_command calls....
        cmd = 'bsub %s < %s' % (self.submitparams, app)
        stdout, stderr = self.raw(cmd)
        jobstring = stdout
        m = self.jobre.search(jobstring)
        self.lastjob = []
        while m:
            jobid = m.group(0)
            self.createJob(jobid)
            self.lastjob.append(jobid)
            m = self.jobre.search(jobstring, m.end())

        if len(self.jobs) > 0:
            output = '%s jobs submitted.' % len(self.lastjob)
        else:
            output = 'No jobs submitted. Something could be wrong.'
            output += 'stdout:\n' + stdout
            output += '\nstderr:\n' + stderr

        return True, self.lastjob, output


class torque(pbs):
    pass
