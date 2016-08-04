import logging
import commands
import os

from pylons import request, response, session, tmpl_context as c, url, app_globals
from pylons.controllers.util import abort, redirect
from authkit.authorize.pylons_adaptors import authorize,authorized

from cyberweb.lib.base import BaseController, render
from cyberweb.lib.jodis.sshresource import ssh
from cyberweb.lib import auth
from cyberweb.model import meta, AuthKey, Resource

log = logging.getLogger(__name__)

class ProxyController(BaseController):

    @authorize(auth.is_valid_user)
    def __before__(self):
        pass

    def index(self):
        # Return a rendered template
        #return render('/proxy.mako')
        # or, return a string
        return self.publicprivatekey()

    def publicprivatekey(self):
        '''
        Allows a user to create an ssh key pair and then push that public key to 
        any resource in the eco-system
        '''
        #c.createkey = request.params.has_key('CreateKey')
        c.resource_id = request.params.get('host') or ''
        c.user = request.params.get('user') or ''
        password = request.params.get('password') or ''
        c.resources = meta.Session.query(Resource).all()
        c.error = ''
        
        if request.method == 'POST':
            try: c.resource_id = int(c.resource_id)
            except Exception as _: c.error = 'Problems interpreting resource ID.'
            
            if not c.resource_id:
                c.error = 'Please select a host'
            elif not c.user:
                c.error = 'Please enter a username'
            elif not password:
                c.error = 'Please enter a password'

        c.current_keys = meta.Session.query(AuthKey).filter(AuthKey.user_id == session['user_id']).all()
        c.has_key = bool(c.current_keys)
        c.keymade = False
        #if c.createkey and not c.current_keys:
        if not c.current_keys:
            #c.keymade = True
            if self._create_key():
                c.error = ''
                c.current_keys = meta.Session.query(AuthKey).filter(AuthKey.user_id == session['user_id']).all()
                c.has_key = True
            else:
                c.error = 'Could not generate a key'
            
        c.connection_error = ''
        if request.method == 'POST' and c.has_key and not c.error:
            try:
                resource = meta.Session.query(Resource).get(c.resource_id)
                sshconnect = ssh(resource.hostname, c.user, password=password)
                for key in c.current_keys:
                    keys_file = "~/.ssh/authorized_keys"
                    id_string = 'CyberWeb Key %d for %s' % (key.id, c.user)
                    grep = sshconnect.run('grep "%s" %s' % (id_string, keys_file))
                    if id_string not in grep[0]:
                        sshconnect.run('echo "ssh-dss %s # %s" >> %s' % (key.public_key, id_string, keys_file))
                    else:
                        c.error = 'Key already exists for user %s!' % c.user
            except Exception as e:
                c.error = e
            else:
                c.error = 'Success!'
        return render('/proxy/publicprivatekey.mako')


    def _create_key(self):
        private_keyfile = 'keyfile_generation_%d' % session['user_id']
        public_keyfile = private_keyfile + '.pub'
        status, output = commands.getstatusoutput('ssh-keygen -t dsa -f %s -N ""' % private_keyfile)
        if os.path.isfile(private_keyfile) and os.path.isfile(public_keyfile):
            with open(private_keyfile,'r') as fh:
                private_key = fh.readlines()
            private_key = ''.join(private_key).strip()

            with open(public_keyfile,'r') as fh:
                key_line = fh.readlines()
            key_line = ''.join(key_line).strip()
            public_key = key_line.split(' ')[1]

            key = AuthKey(private_key, public_key, session['user_id'])
            try:
                meta.Session.add(key)
                meta.Session.commit()
            except Exception, e:
                log.error('Failed to insert key for %s. %s' % (session['user'], e))
                meta.Session.rollback()
            else:
                log.debug('Successfully created public/private key pair for %s' % session['user'])
                commands.getstatusoutput('rm -f %s %s' % (private_keyfile,public_keyfile))
            meta.Session.close()
            return True
        else:
            log.error('Failed to create key for %s.' % session['user'])
        return False
