import os
import sys
import re
import json
import logging

###from pylons import request, response, session, app_globals, tmpl_context, url as c, config
from pylons import request, response, session, app_globals, tmpl_context as c, config, url
from pylons.controllers.util import abort, redirect

from pylons.decorators import jsonify
from authkit.authorize.pylons_adaptors import authorize,authorized
import sqlalchemy as sa
from sqlalchemy.orm.attributes import manager_of_class as manager
from config import Config

from cyberweb.lib.base import BaseController, render
from cyberweb.lib import auth, helpers as h
from cyberweb import model
from cyberweb.model import meta, JobState, Job, Message, Group, \
        GroupDefinition, User, Service, ServiceName, Account, \
        Resource, Protocol

log = logging.getLogger(__name__)

myclass, myfunc = config.get('authkit.form.authenticate.user.encrypt',':').split(':')
mysecret = config.get('authkit.form.authenticate.user.encrypt.secret','')

try:
    exec('from %s import %s as encrypt' % (myclass,myfunc))
except:
    log.error('No encrypt function is being used for passwords!(%s.%s)',myclass,myfunc)
    encrypt = lambda x,y: x

class GsicredsController(BaseController):

    @authorize(auth.is_valid_user)
    def __before__(self):
        pass

    def index(self):
        c.user = session['user']
        user_id = session.get('user_id')
        if not user_id:
            raise Exception
        return self.gsicreds()
        
    def gsicreds(self):
        c.user = session['user']
	###c.username = u.username
        c.results = "action: gsicreds"
        c.status = ""
        c.errmessage = ""
        c.gsidir = self._get_gsi_dir()
        c.title = config.get('project.shortname','CyberWeb') + ' User Page for: ' + session.get('user','you')
        
        return render('/authentication/gsicreds/gsicreds.mako')

    def _get_gsi_dir(self):
        # Populatries from the development.ini or production.ini
        #currently this is set up for local, but we can use jodis if the
        #   path is to a remote location
        user = session['user']
        gsidir = config.get('cw.cwproj_dir','.') + '/' + user + '/' + 'gsi'
        if not os.path.isdir(gsidir):
            try: os.makedirs(gsidir)
            except Exception:
                log.debug('Cannot create directory for user %s (%s)' % (user,gsidir))
            else:
                log.debug('Directory created for user %s (%s)' % (user,gsidir))
        return gsidir


###############################################################
#  OLD CODE
###############################################################

    def old_index(self):
        user_id = session.get('user_id')
        c.user = session['user']
        if not user_id:
            raise Exception
        

        # User Info
        user = meta.Session.query(User).filter(User.id == session.get('user_id')).one()
        
        accounts = meta.Session.query(Account).filter(sa.and_(Account.authkey_id != None , Account.user_id == session.get('user_id')));
        dataString = []
        accountHost = {}
        for account in accounts:
            if accountHost.get(account.resource.hostname, True):
                accountDict = {}
                accountDict['name'] = account.name
                accountDict['hostname'] = account.resource.hostname
                dataString.append(accountDict)
                accountHost[account.resource.hostname] = False
       ## c.passwordLessAccount = dataString
        
        meta.Session.close()
        c.status = "index"
        c.results = ""
        #return render('/authentication/gsicreds/gsicreds.mako')
        redirect(url(controller='gsicreds', action='gsicreds'))



    def gsicreds_info(self):
        c.user = session['user']
        c.results = "action: gsicreds_info"
        c.status = ""
        c.errmessage = ""
        c.user = session['user']
        c.userdir  = config.get('cw.cwuser_loc','.')
        c.gsidir =  c.userdir + '/' + session['user'] + '/gsi'
        # Populatries from the development.ini or production.ini
        #currently this is set up for local, but we can use jodis if the
        #   path is to a remote location
        user = session['user']
        gsidir = config.get('cw.cwproj_dir','.') + '/' + user + '/' + 'gsi'
        if not os.path.isdir(c.gsidir):
            try: os.makedirs(c.gsidir)
            except Exception:
                log.debug('Cannot create directory for user %s (%s)' % (c.user,c.gsidir))
            else:
                log.debug('Directory created for user %s (%s)' % (c.user,c.gsidir))
        c.title = config.get('project.shortname','CyberWeb') + ' User Page for: ' + session.get('user','you')
        c.gsidump=''
        return render('/authentication/gsicreds/gsicreds_info.mako')

    def gsicreds_create(self):
        c.user = session['user']
        c.results = "action: gsicreds_create"
        c.status = ""
        c.errmessage = ""
        c.user = session['user']
        c.userdir  = config.get('cw.cwuser_loc','.')
        c.gsidir =  c.userdir + '/' + session['user'] + '/gsi'
        c.title = config.get('project.shortname','CyberWeb') + ' User Page for: ' + session.get('user','you')
        return render('/authentication/gsicreds/gsicreds_create.mako')

    def gsicreds_del(self):
        c.user = session['user']
        c.results = "action: gsicreds_del"
        c.status = ""
        c.errmessage = ""
        c.user = session['user']
        c.userdir  = config.get('cw.cwuser_loc','.')
        c.gsidir =  c.userdir + '/' + session['user'] + '/gsi'
        c.title = config.get('project.shortname','CyberWeb') + ' User Page for: ' + session.get('user','you')
        c.request_params = ''
        return render('/authentication/gsicreds/gsicreds_del.mako')

    def gsicreds_del_action(self):
        c.user = session['user']
        c.results = "action: gsicreds_del_action"
	c.request_params=''
    	mylist = []
        for k in request.params.keys():
		mylist.append(k)
        c.status = ""
	c.request_params=mylist
        c.errmessage = ""
        c.user = session['user']
        c.userdir  = config.get('cw.cwuser_loc','.')
        c.gsidir =  c.userdir + '/' + session['user'] + '/gsi'
        c.title = config.get('project.shortname','CyberWeb') + ' User Page for: ' + session.get('user','you')
        return render('/authentication/gsicreds/gsicreds_del.mako')


    def gsicreds_renew(self):
        c.user = session['user']
        c.results = "action: gsicreds_renew"
        c.status = ""
        c.errmessage = ""
        c.user = session['user']
        c.userdir  = config.get('cw.cwuser_loc','.')
        c.gsidir =  c.userdir + '/' + session['user'] + '/gsi'
        c.title = config.get('project.shortname','CyberWeb') + ' User Page for: ' + session.get('user','you')
        return render('/authentication/gsicreds/gsicreds_renew.mako')

    def gsicreds_stat(self):
        c.user = session['user']
        c.results = "action: gsicreds_del"
        c.status = ""
        c.errmessage = ""
        c.user = session['user']
        c.userdir  = config.get('cw.cwuser_loc','.')
        c.gsidir =  c.userdir + '/' + session['user'] + '/gsi'
        c.title = config.get('project.shortname','CyberWeb') + ' User Page for: ' + session.get('user','you')
        return render('/authentication/gsicreds/gsicreds_stat.mako')

    def gsicreds_upload(self):
        c.user = session['user']
        c.results = "action: gsicreds_upload"
        c.status = ""
        c.errmessage = ""
        c.user = session['user']
        c.userdir  = config.get('cw.cwuser_loc','.')
        c.gsidir =  c.userdir + '/' + session['user'] + '/gsi'
        c.title = config.get('project.shortname','CyberWeb') + ' User Page for: ' + session.get('user','you')
        return render('/authentication/gsicreds/gsicreds_upload.mako')

    #######################################################
    #this function is called from gsicreds_create.mako which
    #is invoked when myproxy_logon.mako is rendered
    def myproxy_logon_action(self):
        import pexpect

        ###
        # set up user data, paths, etc.
        c.user = session['user']
        userdir  = config.get('cw.cwuser_loc','.')
        gsidir =  userdir + '/' + session['user'] + '/gsi'
        try:
            if not os.path.isdir(gsidir):
                os.makedirs(gsidir)
            else:
                log.error('DirCreate exists for %s' % gsidir)
        except OSError:
            log.error('DirCreate FAIL for %s' % gsidir)
        else:
            log.info("DirCreate PASS for %s " % gsidir)

        ###
        # process form data
        log.info( "MyProxyLogon: validating GSI credential ")
        c.errmessage = ''
        errflag = 0
        if request.params.get('myproxy_username'):
            c.mp_username = request.params.get('myproxy_username')
        else:
            errstr = "MyProxy Error: username required."
            c.errmessage =  c.errmessage + errstr
            log.debug( errstr )
            errflag = 1

        if request.params.get('myproxy_password'):
            c.mp_password = request.params.get('myproxy_password')
        else:
            errstr = "MyProxy Error: password required."
            c.errmessage =  c.errmessage + errstr
            log.debug( errstr )
            errflag = 1

        if request.params.get('myproxy_hostname'):
            c.mp_hostname = request.params.get('myproxy_hostname')
        else:
            errstr = "MyProxy Error: hostname required."
            c.errmessage =  c.errmessage + errstr
            log.debug( errstr )
            errflag = 1

        if request.params.get('myproxy_port'):
            c.mp_port = request.params.get('myproxy_port')
        else:
            errstr = "MyProxy Error: port required."
            c.errmessage =  c.errmessage + errstr
            log.debug( errstr )
            errflag = 1

        if request.params.get('myproxy_lifetime'):
            c.mp_lifetime = request.params.get('myproxy_lifetime')
        else:
            c.mp_lifetime = 8760

        if errflag:
            c.myproxy_cmd=""
            return render('/authentication/gsicreds/gsicreds_create.mako')


        ############
        # Build the MYPROXY COMMAND
        #  -d option instructs the server to associate the user DN to the proxy, 
        #  -n option avoids the use of a passphrase to access the long-term proxy, 
        #        so that the CyberWeb server can perform the renewal automatically
        # use pexpect to run the command in 'interactive' mode
        #############
        myproxy_bin = "/usr/local/globus-5.0.2/bin/myproxy-logon"   #ubuntu, fall 2010 updates
        #myproxy_bin = "/usr/local/globus4.2.1/bin/myproxy-logon"  #pipe3
        #myproxy_bin = "/usr/local/globus-4.0.6/bin/myproxy-logon"  #osX
        myproxy_cmd =  myproxy_bin + " -T "
        myproxy_cmd =  myproxy_cmd + " -l " + c.mp_username
        myproxy_cmd =  myproxy_cmd + " -t " + c.mp_lifetime
        myproxy_cmd =  myproxy_cmd + " -p " + c.mp_port
        myproxy_cmd =  myproxy_cmd + " -s " + c.mp_hostname
        userdir  = config.get('cw.cwuser_loc','.')
        ### note: the output file should contain DN information to ensure that the name is unique. 
        ### either that or we user random numbers to name
        ### right now we only allow one hardcoded gsi credential.

        c.gsi_outfile =  userdir + '/'  + c.user + "/gsi/x509proxy_" + c.user

        #myproxy_cmd =  myproxy_cmd + " -o " + userdir + '/'  + c.user + "/gsi/x509up_" + c.user
        myproxy_cmd =  myproxy_cmd + " -o " + c.gsi_outfile

        ###################
        # pexpect input, output, error response strings. 
        # must be treated as constants.
        #
        iostr1 = 'Enter MyProxy pass phrase:'
        ###iostr2 = 'A credential has been received for user thomasm in /tmp/x509up_u501.'
        iostr2 = ("A credential has been received for user: %s  in %s " % (c.user, c.gsi_outfile))
        ##iostr3 = ('Trust roots have been installed in %s' % '/Users/mthomas/.globus/certificates/.')
        iostr3 = ('Trust roots have been installed in /home/carny/.globus/certificates/.')

        errstr1  = 'Failed to receive credentials.'
        errstr2  = 'ERROR from myproxy-server (' + c.mp_hostname + '):'
        errstr3  = 'PAM authentication failed: Permission denied'
        errstr4  = 'unknown myproxy username: ' + c.mp_username
        errstr5  = 'No credentials for renewal authorization.'
        errstr6  = 'Unable to perform password negotiation with server.'
        errstr7  = "Unable to respond to server's authentication challenge."
        errstr8  = 'Error entering passphrase.'
        errstr9  = 'Passphrase must be at least 6 characters long.'
        errstr10 = 'Unknown host "'  + c.mp_hostname + '"'
        errstr11 = 'Error trying to run myproxy-logon command.'

        #### bad mp_port number...not sure how to handle this one
        ####errstr11, 12, 13? = '
        ####Unable to connect to 141.142.15.131:8512
        ####Unable to connect to myproxy.teragrid.org
        ####Operation timed out

        ####
        # use pexpect to run external application and to interact with it
        ###
        c.myproxy_cmd = myproxy_cmd
        child = pexpect.spawn( myproxy_cmd )
        log.debug('MyProxyLogon: (1) Running command time: %' + myproxy_cmd)
        c.status='fail1'
        try:
            i = child.expect([iostr1, errstr11, errstr10,
                              pexpect.TIMEOUT, pexpect.EOF])
            log.debug('MyProxyLogon: (1)child.after::  [' +  str(child.after) + ']')
        except Exception, e:
            log.debug('MyProxyLogon: EXCEPTION:: pexpect.spawn(1):: unknown error with call.')
            log.debug('MyProxyLogon: (2)child.before::  [' +  str(child.before) + ']')
            log.debug('MyProxyLogon: (2)child:: [' +  str(child) + ']')
            log.debug('MyProxyLogon: (2)child.after::  [' +  str(child.after) + ']')
            c.results='MyProxy Logon: Unknown Error. Please try again or contact web administrator.'
            c.status='fail2 i=' + str(i)
            return render('/authentication/gsicreds/gsicreds.mako')
            ###return render('/account/myproxy_logon.mako')

        log.debug('#############################################################')
        log.debug( 'MyProxyLogon: pexpect connection ok, condition = '+ str(i) +', iostr1::' + iostr1)
        c.status='myproxy connection ok'

        if i == 0:
            log.debug('MyProxyLogin: status i='+str(i)+':: child.sendline:: sending passphrase: %s' % c.mp_password)
            c.status = 'Sending Password'
            try:
                child.sendline(c.mp_password)
                j=child.expect([pexpect.TIMEOUT,iostr2, iostr3, errstr1, errstr8, errstr9,
                                pexpect.EOF], timeout=50)
                #log.debug('MyProxyLogin: (3)child.before::  [%s' % str(child.before) )
                log.debug('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                log.debug('MyProxyLogin: [j= %s]:: send pwd child::  [%s]' % (j, str(child)))
                log.debug('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                #log.debug('MyProxyLogin: (3)child.after::  [%s]' % str(child.after) )
                c.status='gsi credential generated'
                c.results = 'A GSI credential has been received for user ' + c.user + '.'
                c.mp_dn = 'DN info'
                outstr = 'login: ' + c.mp_username + '\n'
                outstr = outstr + 'hostname: ' + c.mp_hostname + '\n'
                outstr = outstr + 'dn: ' + c.mp_dn + '\n'
                fname = ('%s/%s/gsi/x509proxy_%s_info' % (userdir, c.user, c.user )  )
                #fname = "/home/carny/cyberweb/cw_user_data/mary/gsi/x509proxy_mary_info"
                log.debug ("Writing info file for %s GSI proxy to file: %s" % (c.mp_username, fname))
                try:
                    fout = open( fname, 'w') 
                    try:
                        #fout.write("This is a test")
                        fout.write( outstr ) 
                    finally:
                        fout.close()
                except Exception, e:
                    errstr = ("Problem writing info file for %s GSI proxy to file: %s" % (c.mp_username, fname))
                    log.debug (errstr)
                    log.debug ("File Open/Write Exception: %s " % e)
                    cla, exc, trbk = sys.exc_info()
                    excName = cla.__name__
                    try:
                        excArgs = exc.__dict__["args"]
                    except KeyError:
                        excArgs = "<no args>"
                    excTb = traceback.format_tb(trbk, 5)
                    log.debug ( "[ExcName: %s]   [excArgs: %s]  [excTb%s]" % (excName, excArgs, excTb))
                    c.results = errstr
                return render('/authentication/gsicreds/gsicreds.mako')
                ##return render('/account/myproxy_logon.mako')
            except Exception, e:
                log.debug('MyProxyLogin: EXCEPTION:: pexpect.spawn(2):: child.expect failed: exception= %s ' % e)
                #log.debug('MyProxyLogin: (4)child.before::  [' +  str(child.before) + "]")
                #log.debug('MyProxyLogin: (4)child::  [' +  str(child) + "]")
                #log.debug('MyProxyLogin: (4)child.after::  [' +  str(child.after) + "]")
                c.status='password send exception'
                log.debug('MyProxyLogin exception: %s', c.status)
                return render('/authentication/gsicreds/gsicreds.mako')
                ###return render('/account/myproxy_logon.mako')
            log.debug('=============================================================')
            log.debug('MyProxyLogin:  STATUS: '+ str(j) )
            log.debug('=============================================================')
            if j == 1:   # its all ok
                log.debug("MyProxyLogin:  SUCCESS!"+iostr2)
                c.status='fail i= ' + str(i) + ', j= ' + str(j)
            elif j == 3:  # something wrong with c.mp_password: error entering passphrase
                log.debug('MyProxyLogin:  err[j='+str(j)+']:: bad input: \n  '+ errstr8)
                c.status='fail i= ' + str(i) + ', j= ' + str(j)
            elif j == 4:  # something wrong:  c.mp_password too short
                log.debug('MyProxyLogin:  err[j='+str(j)+']:: bad input: \n  '+ errstr9)
                c.status='fail i= ' + str(i) + ', j= ' + str(j)
            elif j == 6:   #aksing for c.mp_password again
                log.debug('MyProxyLogin:  err[j=6], asking for c.mp_password again')
                c.status='fail i= ' + str(i) + ', j= ' + str(j)
            elif j == 2:  # something wrong
                c.status='fail i= ' + str(i) + ', j= ' + str(j)
                log.debug('MyProxyLogin:  err[j= '+str(j)+'] somethings wrong.')
                k=child.expect([errstr2, errstr3, errstr4, errstr5, errstr6, errstr7])
                if k == 2:
                    log.debug('MyProxyLogin:  err[k= '+str(k)+']:: bad mp_username.\n  '+ errstr1+ '\n  '+ errstr4)
                elif k == 3:
                    log.debug('MyProxyLogin:  err[k= '+str(k)+']:: bad c.mp_password.\n  '+errstr1+'\n  '+errstr5+'\n  '+errstr6+'\n  '+errstr7)
                else:
                    c.status='fail i= ' + str(i) + ', j= ' + str(j)
                    log.debug('MyProxyLogin:  err[k= '+str(k)+']:: unknown, k='+ str(k))
            else:
                c.status='fail i= ' + str(i)
                log.debug('MyProxyLogin:  err[j= '+str(j)+']:: unkown password/user problem')
        elif i == 1:  # somethings wrong with c.mp_hostname
            c.results = '<p>MyProxyLogin Err[i='+str(i)+']::'  +  errstr10
            log.debug( c.results )
            c.status='fail i= ' + str(i)
        #elif i == 3: # Timeout
        #    c.results ='<p>MyProxyLogin Err['+str(i)+']:: timeout. could not contact myproxy server. '
        #    c.results = c.results + 'Might be bad port number causing a timeout.'
        #    log.debug( c.results )
        #    c.status='fail i= ' + str(i)
        else:
            log.debug('======================================================================')
            log.debug('MyProxyLogin: child::  [' +  str(child) + "]")
            c.status='Communication failure: response = ' + str(i)
            log.debug('MyProxyLogin:  err[i= '+str(i)+']: unknown system/host issue')
        return render('/authentication/gsicreds/gsicreds.mako')
        #return render('/account/myproxy_logon.mako')

    def grid_proxy_info(self):
        c.results=""
        c.user = session['user']
        #system should get list of credentials from users dir (or db when that is written)
        return render('/authentication/gsicreds/grid_proxy_info.mako')
        ##return render('/authentication/gsicreds/gsicreds.mako')


    def grid_proxy_info_action(self):
        c.user = session['user']
        
        if request.params.get('myproxy_username'):
                c.mp_username = request.params.get('myproxy_username')
        else:
            errstr = "MyProxy Error: username required."
            c.errmessage =  c.errmessage + errstr
            log.debug( errstr )
            errflag = 1

        ## now run the unix command, capture the output and pass to mako file - sample
        #cmd = 'grid-proxy-info -f /home/carny/cyberweb/trunk/cw_user_data/mary/gsi/x509up_mary'
        #credir = '/home/carny/cyberweb/trunk/cw_user_data/' + c.user + '/gsi/'
        c.user = session['user']
        userdir  = config.get('cw.cwuser_loc','.')
        gsidir =  userdir + '/' + session['user'] + '/gsi'
        c.gsi_outfile =  userdir + '/'  + c.user + "/gsi/x509proxy_" + c.user
        c.userdir = userdir
        try:
            globus_dir='/usr/local/globus-5.0.2/bin'
            cmd = globus_dir + '/grid-proxy-info'   #pipe3
            cmd = cmd + ' -f ' + c.gsi_outfile
            c.general = 'CMD: ' + cmd
            fi,foe = os.popen4( cmd, mode='t' )
            results = foe.readlines()
            c.results = results
            fi.close(); foe.close()
        except:
            errstr = ("There are no GSI Credentials for grid user ID: %s" % c.mp_username)
            log.debug (errstr)
            c.results = errstr
        return render('/authentication/gsicreds/gsicreds.mako')
        return render('/authentication/gsicreds/grid_proxy_info.mako')


    #############################################
    #  Manage CyberWeb Services
    #############################################
    def services(self):
        # Gather the list of services
        c.services = meta.Session.query(ServiceName).distinct().order_by(ServiceName.name)

        c.resources = {}
        for resource in meta.Session.query(Resource).filter(Resource.active == 1).distinct().order_by(Resource.name):
            c.resources[resource.name] = {}
            
        # Gather the list of services on each resource
        for i in meta.Session.query(Service).distinct():
            if i.resource:
                c.resources.setdefault(i.resource.name, {})[str(i.service_name)] = i.id
        
        dataString = '['
        resources = meta.Session.query(Resource).filter(Resource.active == 1).distinct().order_by(Resource.name);
        for resource in resources:
            try:
                service = [service for service in meta.Session.query(Service).filter(Service.resource_id == resource.id)];
                if len(service) > 0:
                    dataString += '{'
                    dataString += '"Resource Id":"%s",' % resource.id
                    dataString += '"Resource Name":"%s",' % resource.name
                    if session.get('available_resources', {}).has_key(resource.name) or resource.name in session.get('available_resources', {}).values():
                        dataString += '"isResourceAvailable":"true",'
                    else:
                        dataString += '"isResourceAvailable":"false",'
                    dataString += '"Services":['
                    for serviceId in service:
                        dataString += '{'
                        protocol = meta.Session.query(Protocol).filter(Protocol.id == serviceId.protocol_id).first();
                        dataString += '"protocol":"%s",' % protocol.name
                        servicename = [servicename for servicename in meta.Session.query(ServiceName).filter(ServiceName.id == serviceId.servicename_id).all()];
                        for serviceNameId in servicename:
                            try:
                                dataString += '"serviceName":"%s",' % serviceNameId.name
                                #servicetype = meta.Session.query(ServiceType).filter(ServiceType.id == serviceNameId.service_type_id).first();
                                dataString += '"serviceType":"%s"' % serviceNameId.service_type.name
                            except:
                                dataString += '"serviceType":""'
                        dataString += '},'
                    dataString = dataString[0:len(dataString)-1];
                    dataString += ']'
                    dataString += '},'
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise
        if len(dataString) > 1:
            dataString = dataString[0:len(dataString)-1];
        dataString += ']'
        
        c.resourceServiceJson = dataString
        meta.Session.close()
        return render('/account/services.mako')

