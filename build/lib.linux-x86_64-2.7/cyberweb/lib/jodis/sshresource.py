"""
.. module:: sshresource

.. moduleauthor:: Carny Cheng <carny@me.com>

The SSH Resource module abstracts the communication used by a resource. A resource may use any of the implemented
protocols of commmunication. This is currently SSH and GSISSH.

"""
import os
import time
import pexpect
import paramiko
import logging

log = logging.getLogger(__name__)

class ssh_exception(Exception):
    pass


class basessh:
    """ The base SSH class for Jodis. This is an abstract class and should not be called directly.

    """
    def __init__(self, host, user, keyfile=None, password=None, debug=False):
        self.jobs = []
        self.host = host
        self.user = user
        self.keyfile = keyfile
        self.password = password
        self.appdir = 'apps'
        self.outputfile = 'output'
        self.scpcmd = 'scp'
        self.scpparams = '-rvp' if debug else '-rp'

    def scp(self, srcUser, srcHost, srcPath, tgtUser, tgtHost, tgtPath):
        """ Method mimics the commandline secure copy command.

        Args:
            srcUser: Username on source machine
            srcHost: Hostname of source machine
            srcPath: Path of the file(s) on the source machine
            tgtUser: Username on target machine
            tgtHost: Hostname of target machine
            tgtPath: Path of the file(s) on the target machine

        Return:
            Returns the output of the scp command

        """
        sourceStr = srcPath
        if srcHost:
            sourceStr = srcHost + ':' + sourceStr
        if srcUser:
            sourceStr = srcUser + '@' + sourceStr

        targetStr = tgtPath
        if tgtHost:
            targetStr = tgtHost + ':' + targetStr
        if tgtUser:
            targetStr = tgtUser + '@' + targetStr

        if self.keyfile:
            cmd = '%s -i %s %s %s %s' % (self.scpcmd, self.keyfile, self.scpparams, sourceStr, targetStr)
        else:
            cmd = '%s %s %s %s' % (self.scpcmd, self.scpparams, sourceStr, targetStr)
        
        #temporary codt to debug scp - smita
        log.debug("SCP Command: %s", cmd)
        
        return pexpect.run(cmd)

    def scpTo(self, user, host, srcPath, tgtPath):
        """ A helper method does a secure copy from the local server to a remote server.

        Args:
            user: target hostusername
            host: target hostname
            srcPath: Path of the file(s) on the source machine
            tgtPath: Path of the file(s) on the target machine

        Return:
            Returns the same output as scp method

        """
        return self.scp(user, host, srcPath, self.user, self.host, tgtPath)

    def scpFrom(self, user, host, srcPath, tgtPath):
        """ A helper method does a secure copy from a remote server to the local server.

        Args:
            user: source hostusername
            host: source hostname
            srcPath: Path of the file(s) on the source machine
            tgtPath: Path of the file(s) on the target machine

        Return:
            Returns the same output as scp method

        """
        return self.scp(self.user, self.host, srcPath, user, host, tgtPath)

    def move(self, srcPath, tgtPath):
        """ Local move command

        Args:
            srcPath: Path of the source file(s)
            tgtPath: Path of the target file(s)

        Return:
            Returns the output of the mv command

        """
        cmd = 'mv %s %s' % (srcPath, tgtPath)
        return self.run(cmd)

    def run(self, command):
        """ Stub function to run a command.

        Args:
            command: Command string

        Returns:
            This is a stub function. It returns None

        """
        return


class ssh(basessh):
    """ The SSH class wraps SSH calls via the paramiko library

    """
    def __init__(self, host, user, keyfile=None, password=None, debug=False):
        basessh.__init__(self, host, user, keyfile)
        self.scpcmd = 'scp'
        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh = self.connect(password=password)

    def __del__(self):
        if self.sshclient:
            self.sshclient.close()

    def connect(self, password=None):
        """ Open the SSH connection

        Args:
            password: Optional password string

        Return:
            Returns the connection object

        """
        if password:
            try:
                self.sshclient.connect(self.host, username=self.user, password=password)
            except (paramiko.BadHostKeyException, paramiko.AuthenticationException, Exception)  as _:
                raise
        else:
            try:
                self.sshclient.connect(self.host, username=self.user, key_filename=self.keyfile)
            except (paramiko.BadHostKeyException, paramiko.AuthenticationException, Exception)  as _:
                raise
        return self.sshclient

    def uploadApp(self, srcPath, srcIP=None, srcUser=None):
        """ Upload a file from the web server machine to the target resource.

        Args:
            srcPath: Path of the file(s) on the source machine
            srcIP: IP/hostname of the source machine
            srcUser: Username on the source machine


        Return:
            Boolean based on md5

        """

        if srcIP is None:
            srcIP = self.host
        if srcUser is None:
            srcUser = self.user

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(srcIP, username=srcUser)
        except paramiko.BadHostKeyException as _:
            print 'Cannot connect to host'
            raise False
        except paramiko.AuthenticationException as _:
            print 'Authentication failed'
            raise

        _, stdout, _ = ssh.exec_command('md5sum %s' % srcPath)
        ssh.close()

        md5src = stdout.read().strip().split(' ')[0]

        if len(md5src) != 32:
            error = 'Invalid MD5: %s' % stdout
            print error
            return False, error

        tgtPath = '%s/%s' % (self.appdir, md5src)
        _, stdout, stderr = self.sshclient.exec_command('ls -d %s' % self.appdir)
        if stderr.read().find('No such file') > 0:
            _, stdout, stderr = self.sshclient.exec_command('mkdir %s' % self.appdir)
            cmd = '%s %s %s@%s:%s %s@%s:%s' % (self.scpcmd, self.scpparams, srcUser, srcIP, srcPath, self.user, self.host, self.appdir)
            error = pexpect.run(cmd)

        _, stdout, stderr = self.sshclient.exec_command('ls -d %s' % tgtPath)
        if stderr.read().find('No such file') > 0:
            _, stdout, stderr = self.sshclient.exec_command('mkdir %s' % tgtPath)
            cmd = '%s %s %s@%s:%s %s@%s:%s' % (self.scpcmd, self.scpparams, srcUser, srcIP, srcPath, self.user, self.host, tgtPath)
            error = pexpect.run(cmd)
        else:
            error = 'File exists. No need to copy'

        filename = os.path.basename(srcPath)
        self.app = '%s/%s' % (tgtPath, filename)
        _, stdout, stderr = self.sshclient.exec_command('md5sum %s' % self.app)
        md5tgt = stdout.read().strip().split(' ')[0]

        if (md5src == md5tgt):
            retVal = True
        else:
            retVal = False

        return retVal, error

    def run(self, command):
        """ Run a command on a remote machine.

        Args:
            command: string command

        Return:
            Tuple of stdout and stderr

        """
        try:
            _, stdout, stderr = self.sshclient.exec_command(command)
        except:
            self.connect()

        return stdout.read().strip(), stderr.read().strip()

    def md5(self, filename):
        """ Return md5sum of a file

        """
        _, stdout, stderr = self.sshclient.exec_command('md5sum %s' % filename)
        out = stdout.read()
        err = stderr.read()
        if err == '':
            md5, md5file = out.split()
            if md5file == filename:
                return md5, ''

        return '', err


class gsissh(basessh):
    """ The GSISSH class wraps GSISSH calls using pexpect.
    """
    def __init__(self, host, user, keyfile=None, debug=False):
        basessh.__init__(self, host, user)
        self.scpcmd = 'gsiscp'
        self.sshcmd = 'gsissh'
        self.myexpectStr = '%sWhatACoincidence!' % self.user
        myString = '\'%s\'' % self.myexpectStr
        myendStr = '%s\r\n' % self.myexpectStr
        self.delimiterlist = [myString, myendStr, pexpect.EOF, pexpect.TIMEOUT]
        self.ssh = self.connect(host, user, self.myexpectStr, self.delimiterlist)

    def __del__(self):
        if self.sshclient:
            self.sshclient.sendline('exit')
            self.sshclient.close()

    def connect(self, host=None, user=None, myexpectStr=None, delimiterlist=None, sshcmd=None):
        """ Open the SSH connection

        Return:
            Return the connection object

        """
        host = host or self.host
        user = user or self.user
        sshcmd = sshcmd or self.sshcmd or 'gsissh'
        myexpectStr = myexpectStr or self.myexpectStr
        delimiterlist = delimiterlist or self.delimiterlist or []

        cmd = '%s %s' % (sshcmd, host)
        self.sshclient = pexpect.spawn(cmd)
        self.sshclient.setecho(True)
        self.sshclient.sendline('echo \'%s\'' % myexpectStr)

        # Check for expect string
        state = self.sshclient.expect(delimiterlist)
        while state != 1:
            if state == 2:
                raise ssh_exception
            state = self.sshclient.expect(delimiterlist)

        return self.sshclient

    def uploadApp(self, srcPath, srcIP=None, srcUser=None):
        pass

    def run(self, command):
        """ Run a command on a remote machine.

        Returns:
            stdout and stderr of the command that was run

        """
        outputStr = ''
        error = ''
        mycommand = '%s;echo \'%s\'' % (command, self.myexpectStr)

        try:
            self.sshclient.sendline(mycommand)
        except Exception as e:
            raise
            error = e

        count = 0
        timedout = False
        while True:
            count += 1
            time.sleep(.8)
            state = self.sshclient.expect(self.delimiterlist)
            if state == 0:
                # Continue to wait
                pass
            elif state == 1:
                outputArr = self.sshclient.before.splitlines()[1:]
                outputStr = '\n'.join(outputArr)
                break
            elif state == 2:
                error = 'Pexpect error EOF reached.'
                break
            elif state == 3:
                if timedout:
                    error = 'Pexpect error TIMEOUT reached.'
                    break
                else:
                    timedout = True
            else:
                error = 'Unexpected error'
                break

        return outputStr, error

    def md5(self, filename):
        """ Return md5sum of a file

        Return:
            Tuple of md5sum and error string

        """
        output, error = self.run('md5sum %s' % filename)

        md5arr = output.split()
        if len(md5arr) > 1 and md5arr[-1] == filename:
            for md5 in md5arr[0:-1]:
                if len(md5) == 32:
                    return md5, ''

        return '', error

    def sshCredentials(self, keys=None):
            directory = "~/.ssh"
            keys_file = "~/.ssh/authorized_keys"
            for key in keys or []:
                self.run('if [ ! -d .ssh ]; then mkdir .ssh; chmod 700 .ssh; fi')
                id_string = 'CyberWeb Key %d for %s' % (key.id, userName)
                grep = self.run('grep "%s" %s' % (id_string, keys_file))
                if id_string not in grep[0]:
                    self.run('echo "ssh-dss %s # %s" >> %s; chmod 600 %s' % (key.public_key, id_string, keys_file, keys_file))
                    c.warning = ''
                else:
                    c.warning = 'Key already exists for user, Over writing Key !!'
                    self.run("sed '/%s/d' %s > %s/authorized_keys_new" % (id_string, keys_file, directory))
                    self.run('rm %s' % keys_file)
                    self.run('mv %s/authorized_keys_new %s' % (directory, keys_file))
                    self.run('echo "ssh-dss %s # %s" >> %s; chmod 600 %s' % (key.public_key, id_string, keys_file, keys_file))