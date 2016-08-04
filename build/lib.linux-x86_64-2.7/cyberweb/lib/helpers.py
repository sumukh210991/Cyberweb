"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
import traceback
import simplejson as json
import sqlalchemy as sa
from sqlalchemy.sql.expression import desc


#x#from pylons import config, request, response, session, app_globals, url, tmpl_context as c
#x#from pylons.controllers.util import redirect
import sqlalchemy as sa

from pylons import url, session, request, response  as c
from pylons import config, request, response, session, app_globals, url, tmpl_context as c

from webhelpers import html

from cyberweb.lib.base import BaseController, render

from cyberweb import model
from cyberweb.model import meta, Job, JobState, Account, Resource
from cyberweb.lib.base import BaseController, render
from cyberweb.lib.jodis import sshresource as myssh, resources
#from cyberweb.lib import auth, Gccom, BaseJob as basejob 

import logging
log = logging.getLogger(__name__)


__all__ = ['html', 'getJobs', 'jobmonitor']


def getCWConfig(prefix='cw', config={}):
    cw_configs = dict()
    prefix += '.'
    for k in config.keys():
        if k.startswith(prefix):
            cw_configs[k[len(prefix):]] = config[k]
    return cw_configs


def get_user_resources(user_id):
    return app_globals.user_resources(user_id)


def get_active_resources(user_id):
    available_resources_user = dict()
    accounts = meta.Session.query(Account).filter(sa.and_(Account.authkey_id != None, Account.user_id == user_id));
    accountHost = {}
    for account in accounts:
        if accountHost.get(account.resource.hostname, True) and account.resource.active == True:
            ## check the ssh /gsissh connections
            available_resources_user[account.resource.hostname] = account.resource.name
    meta.Session.close()
    return available_resources_user


def get_active_user_resources(user_id):
    accounts = meta.Session.query(Account).filter(sa.and_(Account.authkey_id != None, Account.user_id == user_id));
    acctlist = []
    accountHost = {}
    for account in accounts:
        if accountHost.get(account.resource.hostname, True) and account.resource.active == True:
            accountDict = {}
            accountDict['account_name'] = account.name
            accountDict['hostname'] = account.resource.hostname
            # at some point add default auth mech, or ssh=T/F, gsi=T/F....
            acctlist.append(accountDict)
            accountHost[account.resource.hostname] = False
    meta.Session.close()
    return acctlist