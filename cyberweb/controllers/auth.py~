import logging

import os
import re
from datetime import datetime

from pylons import config, request, response, session, url, tmpl_context as c
from pylons.controllers.util import redirect
from pylons.decorators.secure import https

from cyberweb.lib.base import BaseController, render
import cyberweb.model as model
import cyberweb.model.meta as meta

log = logging.getLogger(__name__)

myclass, myfunc = config.get('authkit.form.authenticate.user.encrypt',':').split(':')
mysecret = config.get('authkit.form.authenticate.user.encrypt.secret','')

try:
    exec('from %s import %s as encrypt' % (myclass,myfunc))
except:
    log.error('No encrypt function is being used for passwords!(%s.%s)',myclass,myfunc)
    encrypt = lambda x,y: x

class AuthController(BaseController):

    #@https()
    def signup(self):
        c.username = request.params.get('cw_username','').strip().lower()
        c.password = request.params.get('password','')
        c.password_verify = request.params.get('password_verify','')
        c.firstname = request.params.get('firstname','').strip()
        c.lastname = request.params.get('lastname','').strip()
        c.institution = request.params.get('institution','').strip()
        c.email = request.params.get('email','').strip()
        c.reason = request.params.get('reason','').strip()
        c.status = 0
        c.statusinfo = ''

        # Check to see if we have all the params
        if not len(request.params):
            return render('/account/reqacct.mako')
        elif not c.username or not c.password or not c.firstname or not c.lastname \
                or not c.institution or not c.email or not c.email:
            c.statusinfo = 'You are missing a field in your account request data. Please try again.'
            log.error(c.statusinfo)
            return render('/account/reqacct.mako')
        
        #Check for valid username and if the username exists in database
        exists = meta.Session.query(model.User).filter(model.User.username == c.username).count()
        if not re.match('[a-zA-Z]\w+$',c.username):
            c.statusinfo = 'Username can only contain letters, numbers and underscore(_) and must being with a letter.'
        elif exists:
            c.statusinfo = 'Username %s already exists. Please choose another.' % c.username
        elif c.email.find('@') == -1:
            c.statusinfo = 'Please enter a valid email address.'
        elif len(c.password) < 8:
            c.statusinfo = 'Password must be at least 8 characters.'
        elif c.password != c.password_verify:
            c.statusinfo = 'Your passwords do not match. Please try it again.'
        # User data looks valid. Let's create an account!
        else:
            # Add the user to the database
            encrypted_password = encrypt(c.password,mysecret)
            user = model.User(c.username,encrypted_password,firstname=c.firstname,\
                              lastname=c.lastname,institution=c.institution,email=c.email)
            try:
                meta.Session.add(user)
                meta.Session.commit()
            except:
                c.statusinfo = 'Couldn\'t write cw user (%s) to database.' % user.username
                log.error(c.statusinfo)
            else:
                meta.Session.close()
                # @todo: We actually want to avoid showing the form now
                c.status = 1
                c.statusinfo = 'A user account has been created for %s.' % c.username
                log.info('New account id %d created for %s (%s %s)' % (user.id,user.username,user.firstname,user.lastname))

        return render('/account/reqacct.mako')

    #@https()
    def signin(self):
        username = request.params.get('username', '').strip()
        password = request.params.get('password', '').strip()
        
        if not len(request.params):
            return render('/account/signin.mako')
        elif not (username and password):
            c.message = "You must specify a username and password"
            return render('/account/signin.mako')

        # Query the database for the user
        u = meta.Session.query(model.User).filter(model.User.username == username)
        if u.count() < 1:
            c.message = 'Invalid username/password. Please try again.'
            return render('/account/signin.mako')

        u = u.one()
        if u.password == encrypt(password,mysecret):
            # User is verified!
            # Set cookie, which sets REMOTE_USER
            request.environ['paste.auth_tkt.set_user'](username)
            response.set_cookie('cwsession', 'hello_%s' % username, max_age=24*3600)
            # Populate simple session data
            session['user'] = username
            session['user_id'] = u.id
            session['user_groups'] = [i.id for i in u.groups]
            session.save()

            # log last login date and ip
            try:
                u.last_login_ip = request.environ.get('REMOTE_ADDR')
                u.last_login_date = datetime.now()
                meta.Session.commit()
            except:
                log.error('Can\'t save user %s\'s last IP (%s)' % (u.username,u.last_login_ip))

            ###
            # check for user file and data spaces; create if not there
            # there are two types:
            #    1. internal data managed by cyberweb. this should be out of web space.
            #    2. for users to store data generated by system; viewable by web pages.
            ###

            #get directories from the development.ini or production.ini
            #currently this is set up for local, but we can use jodis if the
            #   path is to a remote location
            cwdatadir   = config.get('cw.data_dir','.')
            ###cwdatadir   = config.get('cw.userdata_path_local','.')  # undefined
            cwusersdir  = config.get('cw.cwuser_loc','.')

            userdir = cwusersdir + '/' + username
            if not os.path.isdir(userdir):
                try: os.makedirs(userdir)
                except Exception:
                    log.debug('Cannot create directory for user %s (%s)' % (u.username,userdir))
                else:
                    log.debug('Directory created for user %s (%s)' % (u.username,userdir))

            # @todo: get directories from the development.ini or production.ini
            datadir = cwdatadir + '/' + username
            if not os.path.isdir(datadir):
                try: os.makedirs(datadir)
                except OSError:
                    log.debug('Cannot create directory for user %s (%s)' % (u.username,userdir))
                else:
                    log.debug('Directory created for user %s (%s)' % (u.username,userdir))

            # Redirect the user to wherever they were going
            forward_to = request.headers.get('REFERER', '/')
            if (forward_to[-7:] == '/signin'): forward_to = '/'
            return redirect(forward_to)

        c.message = 'Invalid username/password. Please try again.'
        c.username = username
        meta.Session.close()
        return render("/account/signin.mako")

    def signout(self):
        user = session.get('user') or request.environ.get('REMOTE_USER')
        if user:
            log.info("%s signed out." % user)
            # Hack to confirm logout of user.
            session.clear()
            session.save()
            if request.environ.has_key('REMOTE_USER'):
                del request.environ['REMOTE_USER']

        # The actual removal of the AuthKit cookie occurs when the response passes
        # through the AuthKit middleware, we simply need to display a page
        # confirming the user is signed out
        session.invalidate()

        redirect(url(controller='homepage', action='index'))
