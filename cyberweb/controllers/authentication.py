import os
import sys
import re
import json
import logging

from pylons import request, response, session, app_globals, tmpl_context as c, config
from pylons.controllers.util import abort, redirect

from pylons.decorators import jsonify
from authkit.authorize.pylons_adaptors import authorize,authorized
import sqlalchemy as sa
from sqlalchemy.orm.attributes import manager_of_class as manager
from config import Config

from cyberweb.lib import auth        
from cyberweb.lib.base import BaseController, render
from cyberweb.model import meta, JobState, Job, Message, Group, \
        GroupDefinition, User, Service, ServiceName, Account, \
        Resource, Protocol

log = logging.getLogger(__name__)

myclass, myfunc = config.get('authkit.form.authenticate.user.encrypt', ':').split(':')
mysecret = config.get('authkit.form.authenticate.user.encrypt.secret', '')

try:
    exec('from %s import %s as encrypt' % (myclass, myfunc))
except:
    log.error('No encrypt function is being used for passwords!(%s.%s)', myclass, myfunc)
    encrypt = lambda x, y: x


class AuthenticationController(BaseController):

    @authorize(auth.is_valid_user)
    def __before__(self):
        pass

    def index(self):
        user_id = session.get('user_id')
        c.user = session['user']
        if not user_id:
            raise Exception

        c.title = config.get('project.shortname', 'CyberWeb') + ' User Page for: ' + session.get('user') or 'you'
        c.status = ""
        c.results = ""
        return render('/authentication/authentication.mako')

    def authentication(self):
        c.user = session['user']
        c.status = ""
        c.results = ""
        c.errmessage = ""
        return render('/authentication/authentication.mako')

###############################################################

    def reset_password(self):
        username = session.get('user') or ''
        user = meta.Session.query(User).filter(User.username == username).one()
        userkeys = manager(User)

        # Update values if any to update
        if len(request.params):
            update = False
            log.info(request.params.keys())
            for k, v in request.params.items():
                if k in userkeys and eval('user.%s' % k) != v:
                    try:
                        exec('user.%s = \'%s\'' % (k, v))
                        update = True
                    except:
                        c.error = True
                        c.message = 'Couldn\'t update key %s (%s). Please change your value and try again.' % (k, v)
                        update = False

            if update:
                try:
                    meta.Session.commit()
                except:
                    c.error = True
                    c.message = 'Can\'t commit to database.  RP'
                    log.error('Can\'t commit to database.  RP')
                    meta.Session.flush()
                else:
                    c.message = 'User info updated.  RP'
            else:
                c.error = True
                c.message = 'No change to be saved.  RP'

        # Populate values for website
        c.account = dict()
        c.pref = dict()
        c.info = dict()

        c.account['username'] = username
        c.account['firstname'] = user.firstname
        c.account['lastname'] = user.lastname
        c.account['institution'] = user.institution
        c.account['email'] = user.email
        c.info['User since'] = user.created.strftime('%b, %Y')
        c.info['Last logged in from'] = user.last_login_ip
        c.info['Last logged in on'] = user.last_login_date

        c.devmessage = 'Note: user preferenes and change password are under development. reset_password'
        meta.Session.close()
        return render('/authentication/reset_password.mako')

    def changePassword(self):
        try:
            username = session.get('user', '')
            user = meta.Session.query(User).filter(User.username == username).one()

            oldpassword = request.params.get('oldpassword')
            newpassword = request.params.get('newpassword')

            log.info(oldpassword)
            log.info(newpassword)

            if not oldpassword:
                meta.Session.close()
                return "{'Error': 'True', 'Message': 'Invalid user name or password.'}"

            if not newpassword:
                meta.Session.close()
                return "{'Error': 'True', 'Message': 'Invalid user name or password.'}"

            oldpassword = encrypt(oldpassword, mysecret)
            newpassword = encrypt(newpassword, mysecret)

            if not oldpassword == user.password:
                meta.Session.close()
                return "{'Error': 'True', 'Message': 'Invalid user name or password.'}"

            user.password = newpassword
            meta.Session.commit()
            meta.Session.close()
            return "{'Error': 'False', 'Message': 'Password changed Successfully.'}"
        except:
            c.error = True
            c.message = 'Can\'t commit to database.'
            log.error('Can\'t commit to database.')
            meta.Session.flush()