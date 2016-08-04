import logging
import commands
import os

from pylons import request, response, session, app_globals, tmpl_context as c, config, url
from pylons.controllers.util import abort, redirect
from authkit.authorize.pylons_adaptors import authorize, authorized
import sqlalchemy as sa

from cyberweb.lib.base import BaseController, render
from cyberweb.lib.jodis.sshresource import ssh
from cyberweb.lib import auth
from cyberweb.model import meta, AuthKey, Resource, Account

log = logging.getLogger(__name__)


class PkiproxyController(BaseController):

    @authorize(auth.is_valid_user)
    def __before__(self):
        pass

    def index(self):
        return self.pkiproxy()

    def pkiproxy(self):
        c.user = session['user']
        c.status = ''
        c.results = ''
        c.message = ''
        c.err = ''
        c.cmd = ''
        c.outerr='outerr '
        c.ssherr='ssherr'
        c.err='err'
        c.user = session['user']
        c.debug = 1
        c.res_pki = {}
        c.res_nonpki = {}
        c.res_all = {}

        c.results = ''
        c.keys_file = ''
        res_acct = ''
        current_keys = meta.Session.query(AuthKey).filter(AuthKey.user_id == session['user_id']).all()
        res_all = meta.Session.query(Resource).filter(Resource.active == 1)
        accts_all = meta.Session.query(Account).filter(Account.user_id == session['user_id']).all()
        for res in res_all:
            try:
                resource = meta.Session.query(Resource).get(res.id)
                for account in accts_all:
                    acct_resource = meta.Session.query(Resource).get(account.resource_id)
                    c.res_all[account.id] = [res.hostname, account.name, '', '']
                    if acct_resource.hostname == resource.hostname:
                        log.debug('PKIProxy:Resource: %s,  Account: Res: %s, Name: %s ' % 
                                (resource.hostname, acct_resource.hostname, account.name))
                        for key in current_keys:
                            keys_file = "~/.ssh/authorized_keys"
                            id_string = 'CyberWeb Key %d for %s' % (key.id, c.user)
                            #c.cmd = 'date; hostname; whoami; pwd'
                            c.cmd = 'grep -i "cyberweb" %s' % (keys_file)
                            try:
                                output, error = app_globals.jodis.manager.getResource(resource.hostname).raw(c.cmd)
                                c.status = 1 
                                # need to compare this credential to the one stored
                                c.results = output.splitlines()
                                #hand case of multiple keys
                                for index, item in enumerate(c.results):
                                    idx = res.name + '-' + str(index)
                                    c.res_pki[idx] = [res.hostname, account.name, 'PKI key found.', index, item]
                            except Exception as e:
                                c.ssherr = e.message
                                c.res_nonpki[account.id] = [res.hostname, account.name, "No key in authorized keys file.",'']
                    else:
                        c.res_all[res.name] = [res.id, res.hostname, account.name,"No account on host.",'']
            except Exception as e:
                c.err = e

        return render('/authentication/pkiproxy/pkiproxy.mako')

    def _getpkiresources(self, user):
        pkires = {}
        return pkires

    def pkiproxy_addresource(self):
        c.user = session['user']
        c.status = "action: pkiproxy_addresource"
        c.results = ""
        c.errmessage = ""
        c.user = session['user']
        c.userdir = config.get('cw.user_dir','.')
        c.proxydir = c.userdir + '/' + session['user'] + '/proxy'
        return render('/authentication/pkiproxy/pkiproxy_addresource.mako')

    def pkiproxy_info(self):
        c.user = session['user']
        c.status = "action: pkiproxy_info"
        c.results = ''
        c.errmessage = ''
        c.current_keys = ''
        c.user = session['user']
        c.pkires = {}
        c.pkires['a'] = ['aaa']
        c.pkires['b'] = ['bzbzbzbza']
        c.pkires['c'] = ['hahahaha']
        c.current_keys = meta.Session.query(AuthKey).filter(AuthKey.user_id == session['user_id']).all()
        return render('/authentication/pkiproxy/pkiproxy_info.mako')

    def pkiproxy_create(self):
        c.user = session['user']
        c.status = "action: pkiproxy_create"
        c.results = ""
        c.errmessage = ""
        c.user = session['user']
        c.userdir = config.get('cw.user_dir','.')
        c.proxydir = c.userdir + '/' + session['user'] + '/proxy'
        return render('/authentication/pkiproxy/pkiproxy_create.mako')

    def publicprivatekey(self):
        '''
        Allows a user to create an ssh key pair and then push that public key to 
        any resource in the system
        '''
        log.error('PKIProxy: publicprivatekey ')
        #c.createkey = request.params.has_key('CreateKey')
        c.resource_id = request.params.get('host') or ''
        c.user = request.params.get('user') or ''
        password = request.params.get('password') or ''
        c.resources = meta.Session.query(Resource).all()
        c.message = ''
        c.user_id = session['user_id'] 

        if request.method == 'POST':
            try: c.resource_id = int(c.resource_id)
            except Exception as _: c.message = 'Problems interpreting resource ID.'

            c.msg = ''
            if not c.resource_id:
                c.msg = c.msg + 'host  '
            if not c.user:
                c.msge = c.msg +  'username  '
            if not password:
                c.msg = c.msg + 'password'
            if  c.msg:
                c.message = 'Please select the following: ' + c.msg

        c.current_keys = meta.Session.query(AuthKey).filter(AuthKey.user_id == session['user_id']).all()
        c.has_key = bool(c.current_keys)
        c.keymade = False
        #if c.createkey and not c.current_keys:
        if not c.current_keys:
            #c.keymade = True
            if self._create_key():
                c.message = ''
                c.current_keys = meta.Session.query(AuthKey).filter(AuthKey.user_id == session['user_id']).all()
                c.has_key = True
            else:
                c.message = 'Could not generate a key'
        ###c.message=c.message + "   [[ GOT HERE ]] "
        c.connection_error = ''
        if request.method == 'POST' and c.has_key and not c.message:
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
                        c.message = 'Key already exists for user %s!' % c.user
            except Exception as e:
                c.message = e  #paramiko error, eg. authentication failed
            else:
                c.message = 'Success!'
        return render('/authentication/pkiproxy/publicprivatekey.mako')

    def _create_key(self):
        log.error('PKIProxy: _creat_key ')
        private_keyfile = 'keyfile_generation_%d' % session['user_id']
        public_keyfile = private_keyfile + '.pub'
        log.error('PubKey File Name:  %s' % (public_keyfile))
        log.error('PubKey File Name:  %s' % (private_keyfile))
        status, output = commands.getstatusoutput('ssh-keygen -t dsa -f %s -N ""' % private_keyfile)
        if os.path.isfile(private_keyfile) and os.path.isfile(public_keyfile):
            with open(private_keyfile, 'r') as fh:
                private_key = fh.readlines()
            private_key = ''.join(private_key).strip()

            with open(public_keyfile, 'r') as fh:
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
                commands.getstatusoutput('rm -f %s %s' % (private_keyfile, public_keyfile))
            meta.Session.close()
            return True
        else:
            log.error('Failed to create key for %s.' % session['user'])
        return False
