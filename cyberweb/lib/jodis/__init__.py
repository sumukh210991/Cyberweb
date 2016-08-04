'''
A module for interacting with compute resources that abstracts authentication middleware.

.. moduleauthor:: Carny Cheng <carny@me.com>

'''
import logging
import threading
import signal
import traceback
import sys

from pylons import session, app_globals
from config import Config
from paramiko import AuthenticationException, SSHException
from base import Jodis
from cyberweb.lib.jodis.resource_manager import Manager

from cyberweb.model import meta, Account

__all__ = ['init_jodis', 'Jodis', 'Manager']

log = logging.getLogger(__name__)
TIMEOUT = 60


class TimeoutError(Exception):
    """
    Exception to raise on a timeout
    """
    pass


def timeoutHandler(signum, frame):
    """
    Function called when a Jodis connection hits the timeout seconds.
    """
    raise TimeoutError('Jodis Connection Timeout')


def init_jodis(config):
    """
    Loads the jodis connections from the database. This function is typically called when CyberWeb is started.
    """
    cw_globals = config.get('pylons.app_globals')

    # Clear hashes. Servers may be leftovers from previous session.
    if not cw_globals.available_resources:
        cw_globals.available_resources = dict()

    # Initialize Jodis from database. Start a connection to all resources and check permission upon use.
    a = meta.Session.query(Account).filter(Account.active==True).order_by(Account.user_id,Account.group_id)
    if not a.count():
        log.warn('There are no account available in the database to start.')
        return None

    try:
        signal.signal(signal.SIGALRM, timeoutHandler)

        # Populate resources from database. Currently connect using all accounts
        # that match our criteria. We need/want to add logic to find the appropriate
        # account to use.
        for account in a.all():
            server = account.resource

            account_name = '(account name: %s)' % account.name if account.name else ''
            log.info('========= Making connection to %s@%s%s =========', account.username, server.name, account_name)
            if account.id not in cw_globals.available_resources:
                try:
                    signal.alarm(TIMEOUT)
                    if not cw_globals.jodis.manager.addMyResource(account.id, maxjobs=20, myglobals=cw_globals): raise
                except AuthenticationException as _:
                    log.warn('Authentication to %s failed for user %s.', server.name, account.username)
                    continue
                except SSHException as e:
                    log.warn('Connection to %s failed. %s', server.name, e)
                    continue
                except Exception as e:
                    log.warn('Connection to %s failed. %s', server.name, e)
                    #traceback.print_exc()
                    continue
                else:
                    cw_globals.available_resources[account.id] = {'hostname': server.hostname, 'name': server.name}
                    log.info('Connection to %s successful.', server.name)
                finally:
                    signal.alarm(0)   # Reset the alarm
            else:
                log.info('Connection to %s already exists' % server.name)

        # Create Jodis and manager singleton if not using database. This case is never used.
        if not cw_globals.jodis:
            log.info('!!!Starting using config file!!!')
            config = Config(file('cyberweb/lib/jodis/resources.cfg'))
            cw_globals.jodis = Jodis(Manager(config))

        log.info('Finished connecting to %s' % server.name)
    except Exception:
        log.error('Error thrown while trying to start Jodis connections.')
        traceback.print_exc(file=sys.stdout)
        return {}
