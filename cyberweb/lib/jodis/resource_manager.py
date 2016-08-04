'''
.. module:: resource_manager

.. moduleauthor:: Carny Cheng <carny@me.com>

'''
import logging
import os
from config import Config
from pylons import app_globals, config as pyconfig
import sqlalchemy as sa

import resources
from cyberweb.model import meta, Resource, Account, QueueService

log = logging.getLogger(__name__)


class Manager:
    '''
    This class is the core back end of the gateway. The web service and
    WSDL will plug into this class
    '''

    def __init__(self, config=None):
        self.config = config or {}
        self.resources = {}
        self.resourcemax = {}
        self.maxJobs = 0

        if not meta:
            log.error('I cannot import the CyberWeb database. Please check your environment.')
            self.cwenv = False
            return None

    def addResource(self, account_id, name, host, user, queuesystem, maxjobs, config=None, keyfile=None, gsissh=False, account=None, queueservice=None):
        config = config or {}
        # Each resource should be a singleton. Return existing instance if present.
        if host in self.resources:
            log.debug('Host %s already exists.', host)
            return self.resources[account_id]

        log.debug('Host %s (%s) does not exist. Adding...', host, queuesystem)
        self.resources[account_id] = getattr(resources, queuesystem)(host, user, config=config, keyfile=keyfile, gsissh=gsissh, account=account, queueservice=queueservice, name=name)
        if account_id not in self.resources:
            log.error('Can\'t find hash for %s', name)
            return None

        # Set the job and rsource maximums
        maxjobs = maxjobs or 0
        self.resourcemax[host] = maxjobs
        self.maxJobs += maxjobs

        return self.resources[account_id]

    def addMyResource(self, account_id, maxjobs=0, myglobals=None):
        myglobals = myglobals or app_globals
        a = meta.Session.query(Account).filter(Account.id == account_id).one()
        c = Config()
        try:
            queueservice = meta.Session.query(QueueService).filter(QueueService.resource_id == a.resource.id).one()
            c.type = queueservice.queuesystem.name.lower()
        except (AttributeError, sa.orm.exc.NoResultFound) as _:
            log.warn('Assume base resource. No queue service for resource %s', a.resource.name)
            queueservice = None
            c.type = 'resource'
        except Exception as e:
            import traceback
            log.error('Unknown error while adding resource (account id: %d): %s', account_id, e)
            log.error(traceback.format_exc())
            queueservice = None
            c.type = 'resource'
        c.name = a.name or '%s@%s' % (a.username, a.resource.hostname)
        c.host = a.resource.hostname
        c.user = a.username

        # Write out the appropriate auth key
        if a.authkey:
            try:
                keydir = myglobals.cwusersdir
                c.keyfile = keydir + os.path.sep + '%s_%s' % (c.user, c.host)
                if not os.path.isdir(keydir):
                    os.makedirs(keydir)
                elif os.path.isfile(c.keyfile):
                    os.remove(c.keyfile)
                with open(c.keyfile, 'w') as fh:
                    fh.write(a.authkey.private_key)
                os.chmod(c.keyfile, 0600)    # Octal for owner read only
            except IOError:
                import traceback
                log.error('Can\'t write keyfile %s\n%s', c.keyfile, traceback.format_exc())
                c.keyfile = None
        else:
            c.keyfile = None

        maxjobs = maxjobs or c.get('nodes') or 0
        gsissh = a.service_name.name.lower() == 'gsissh'
        return self.addResource(account_id, c.name, c.host, c.user, c.type, maxjobs, config=c, keyfile=c.keyfile, gsissh=gsissh, account=a, queueservice=queueservice)

    def uploadApp(self, srcPath, md5, srcHost=None, srcUser=None):
        '''
        Upload a file from the web server machine to the target resource.
        '''
        retVal = True
        if os.path.isfile(srcPath):
            for resource in self.resources.values():
                status = resource.uploadApp(srcPath, md5, srcHost, srcUser)
                if status:
                    log.debug("Upload complete. %s", resource.host)
                else:
                    retVal = False
                    log.warn("Upload failed. %s.", resource.host)
        else:
            log.error('%s is not a valid file.', srcPath)

        return retVal

    def getStatus(self):
        output = None
        retVal = True
        for resource in self.resources.values():
            status, _ = resource.getStatus()
            if not status:
                retVal = False
                log.warn("Status failed. %s", resource.host)

        return retVal, output

    def getResourceNames(self):
        return [i.name or i.host for i in self.resources.values()]

    def iterResources(self):
        return self.resources.iteritems()

    def getResource(self, account_id):
        return self.resources.get(account_id) or None

    def getHostMax(self, account_id):
        return self.resnurcemax.get(account_id) or 0

    def getMaxJobs(self):
        return self.maxJobs

    def getResults(self):
        for v in self.resources.values():
            _ = v.getResults()

    def disconnect(self, account_id):
        if account_id not in self.resources:
            log.warn('User trying to disconnect from unknown account %s.' % account_id)
            return False

        # Key exists. Close the connection and remove the key.
        log.debug('Closing connection to account %s.' % account_id)

        del self.resources[account_id]
        del app_globals.available_resources[account_id]

        return True

    def disconnect_all(self):
        return False not in [bool(self.disconnect(i)) for i in self.resources.keys()]
    