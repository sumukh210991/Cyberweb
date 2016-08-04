import logging
import os
import sys
import re
import json

from pylons import request, response, session, app_globals, tmpl_context as c, config
from pylons.decorators import jsonify
from authkit.authorize.pylons_adaptors import authorize,authorized
import sqlalchemy as sa
from sqlalchemy.orm.attributes import manager_of_class as manager
from config import Config

from cyberweb.lib.base import BaseController, render
from cyberweb.lib import auth, helpers as h, jobs as j
from cyberweb import model
from cyberweb.model import meta, JobState, Job, Message, Group, \
        GroupDefinition, User, Service, ServiceName, Account, \
        Resource, Protocol

from cyberweb import database
from cyberweb.database import account
from cyberweb.database.account import *

log = logging.getLogger(__name__)

myclass, myfunc = config.get('authkit.form.authenticate.user.encrypt',':').split(':')
mysecret = config.get('authkit.form.authenticate.user.encrypt.secret','')

try:
    exec('from %s import %s as encrypt' % (myclass,myfunc))
except:
    log.error('No encrypt function is being used for passwords!(%s.%s)',myclass,myfunc)
    encrypt = lambda x,y: x
    

database_dict = {
    'account': database.account.AccountOperation()
}


class UserController(BaseController):

    @authorize(auth.is_valid_user)
    def __before__(self):
        pass

    # Populate jobs
    def index(self):
        user_id = session.get('user_id')
        if not user_id:
            raise Exception

        # title
        c.title = config.get('project.shortname','CyberWeb') + ' User Page for: ' + session.get('user','you')
        # Messages
        num_messages = 5
        messages = meta.Session.query(Message).filter(sa.or_(Message.recipient_group_id.in_(session['user_groups']),\
                                                             Message.recipient_user_id == session['user_id'],\
                                                             sa.and_(Message.recipient_group_id == sa.null(), Message.recipient_user_id == sa.null())))\
                                                             .order_by().limit(num_messages)
        c.messageheaders = ['Date','Message']
        c.messages = [ {'Date':i.date.strftime("%B %d,%Y"), 'Message':i.message} for i in messages ]
        # Recent jobs

        numJobs = 10
        c.jobheaders       =j.getJobHeaders()
        c.jobs         = j.jobMonitor(self,session.get('user_id'),numJobs)
        c.jobstates    = j.getJobStateNames()
        c.jobstatekeys = j.getJobStateKeys()
        d=dict()
        for i in range(len( c.jobstatekeys )):
             d[c.jobstatekeys[i]]= c.jobstates[i]
        c.jobstateheaders = d

        # User Info
        user = meta.Session.query(User).filter(User.id == session.get('user_id')).one()
        c.info = dict()
        c.info['Last login'] = user.last_login_date
        c.info['from'] = user.last_login_ip
        c.myproxy_cmd=""
        
        c.user_resources = h.get_active_user_resources(session['user_id'])
        log.info('Active PKI Accts: %s', c.user_resources)
        return render('/account/mycyberweb.mako')

    #############################################
    #  Send and review messages between group and users
    #############################################
    @jsonify
    def send_message(self):
        recipient = request.params.get('recipient',None)
        message = request.params.get('message',None)

        if not recipient:
            return {'error':True, 'message':'Please specify a recipient.'}
        if not message:
            return {'error':True, 'message':'Please specify a message to send.'}

        # Retrieve recipient data.
        recipient_group = True if recipient.startswith('g') else False
        recipientid = int(recipient[1:])

        if recipient == 'b0':
            recipient_name = 'Broadcast'
            recipientid = None
        elif recipient_group:
            recipient_name = meta.Session.query(Group).filter(Group.id == recipientid).one().groupname
            log.debug('Sending message from %s to group %s' % (session.get('user','!!!'),recipient_name))
        else:
            recipient_name = meta.Session.query(User).filter(User.id == recipientid).one().username
            log.debug('Sending message from %s to %s' % (session.get('user','!!!'),recipient_name))

        # Write message to database
        m = Message(session['user_id'],recipientid,message,recipient_group)
        if True:
            # Commit to database
            meta.Session.add(m)
            meta.Session.commit()
        try:
            pass
        except:
            meta.Session.rollback()
            log.error('Message failed from %s to %s' % (session.get('user','!!!'),recipient_name))
            return {'error':True, 'message':'Error writing message'}

        meta.Session.close()
        return {'error':False, 'message':'Message successfully sent.'}


    def messages(self):
        # Grab the list of possible recipients (for sending). Includes both users and groups
        # title
        c.title = config.get('project.shortname','CyberWeb') + ' Messages for: ' + session.get('user','you')
        
        c.recipients = [{'name':i.username,'value':'u%d' % i.id} for i in meta.Session.query(User)]
        # Admins can see all groups, but non-admins can only see their own groups.
        if authorized(auth.is_admin):
            for i in meta.Session.query(GroupDefinition):
                c.recipients.append({'name':'%s (group)' % i.name,'value':'g%d' % i.id})
            c.recipients.append({'name':'Broadcast','value':'b0'})
        else:
            for i in meta.Session.query(Group).filter(Group.user_id == session['user_id']):
                c.recipients.append({'name':'%s (group)' % i.group_definition.name,'value':'g%d' % i.group_definition_id})

        # Grab the list of messages
        messages = meta.Session.query(Message).filter(sa.or_(Message.recipient_group_id.in_(session['user_groups']),\
                                                           Message.recipient_user_id == session['user_id'],\
                                                           sa.and_(Message.recipient_group_id == sa.null(), Message.recipient_user_id == sa.null())))\
                                                           .order_by()
        c.messages = [ {'Date':i.date.strftime("%b %d,%y %H %M %p"), 'Message':i.message, 'From':i.author.username} for i in messages ]
        c.messageheaders = ['Date','From','Message']
        meta.Session.close()
        return render('/account/messages.mako')

    #############################################
    #  Manage CyberWeb Resources
    #############################################
    def resources(self):
        return self.services()
        #return render('/account/services.mako')

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
    
    def configureAccount(self):
        resourceString = '['
        for resource in meta.Session.query(Resource).all():
            resourceString += '{'
            resourceString += '"resourceId":"%s",' % resource.id
            resourceString += '"resourceName":"%s",' % resource.name
            services = meta.Session.query(Service).filter(Service.resource_id == resource.id).all();
            
            serviceString = '['
            for service in services:
                if service.service_name:
                    serviceString += '{'
                    serviceString += '"serviceId":"%s",' % service.id
                    serviceString += '"serviceName":"%s"' % service.service_name.name
                    serviceString += '},'
                
            if len(serviceString) > 1 :
                serviceString = serviceString[0:len(serviceString)-1];
                
            serviceString += ']'
            resourceString += '"services":%s' % serviceString
            resourceString += '},'
            
        if len(resourceString) > 1 :
            resourceString = resourceString[0:len(resourceString)-1];
            
        resourceString += ']'
        c.resourceString = re.escape(resourceString)
        c.user = session['user']
        c.userId = session['user_id']
        return render('/account/accountconfig.mako')
    
    def forwardRequest(self):
        
        type = request.params.get('type')
        method = request.params.get('method')
        parameter = request.params.get('parameter')
        
        object = database_dict[type]

        #if method == 'load':
            #return object.load(parameter)
        #elif method == 'add':
        if method == 'add':
            return object.add(parameter)
        elif method == 'save':
            return object.update(parameter)
        elif method == 'delete':
            return object.userDelete(parameter)
        elif method == 'view':
            return object.userView(parameter)
        else:
            return ''

    #############################################
    #  Manage CyberWeb User Preferences
    #############################################
    def settings(self):
        username = session.get('user','')
        user = meta.Session.query(User).filter(User.username == username).one()
        userkeys = manager(User)

        # Update values if any to update
        if len(request.params):
            update = False
            log.info(request.params.keys())
            for k,v in request.params.items():
                if userkeys.has_key(k) and eval('user.%s' % k) != v:
                    try:
                        exec('user.%s = \'%s\'' % (k,v))
                        update = True
                    except:
                        c.error = True
                        c.message = 'Couldn\'t update key %s (%s). Please change your value and try again.' % (k,v)
                        update = False

            if update:
                try:
                    meta.Session.commit()
                except:
                    c.error = True
                    c.message = 'Can\'t commit to database.'
                    log.error('Can\'t commit to database.')
                    meta.Session.flush()
                else:
                    c.message = 'User info updated.'
            else:
                c.error = True
                c.message = 'No change to be saved.'


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

        c.devmessage = 'Note: user preferenes and change password are under development'
        meta.Session.close()
        return render('/account/settings.mako')



    # this has been moved to Authentication controller
    def changePassword_deprecated(self):
        try:
            username = session.get('user','')
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
            
            oldpassword = encrypt(oldpassword,mysecret)
            newpassword = encrypt(newpassword,mysecret)
            
            if not oldpassword == user.password:
                meta.Session.close()
                return "{'Error': 'True', 'Message': 'Invalid user name or password.'}"
            
            user.password = newpassword
            
            #meta.Session.save(user)
            meta.Session.commit()
            
            log.info(user.password)
            log.info(oldpassword)
            log.info(newpassword)
            meta.Session.close()
            return "{'Error': 'False', 'Message': 'Password changed Successfully.'}"
        except:
            c.error = True
            c.message = 'Can\'t commit to database.'
            log.error('Can\'t commit to database.')
            meta.Session.flush()

    ####
    # Connect jodis accounts
    ###
    @jsonify
    def connect_account(self):
        account_id_str = request.params.get('account_id')
        try:
            account_id = int(account_id_str)
        except (ValueError, TypeError) as _:
            log.error('Received non integer input for account id (%s)' % account_id_str)
            return {'success': False, 'message': 'Received non-integer input for account id (%s)' % account_id_str}
        try:
            account = meta.Session.query(Account).filter(Account.id==account_id).one()
            server = account.resource
        except Exception as e:
            log.error('Received invalid account id (%d)' % account_id)
            return {'success': False, 'message': 'Received invalid account id (%d)' % account_id}
        
        try:
            app_globals.jodis.manager.addMyResource(account_id)
            app_globals.available_resources[account_id] = {'hostname': server.hostname, 'name': server.name}
        except Exception as e:
            log.error('Error connecting to account. %s', e)
            return {'success': False, 'message': 'Error. Cannot connect to account'}
        
        return {'success': True, 'message': 'Successfully connected to %s' % server.hostname}
        
    @jsonify
    def jodis_connect(self):
        '''
        Connect to the resource referenced by the service ID that is passed to this function.
        '''
        service_string = request.params.get('service', '1')

        try:
            service_id = int(service_string)
        except (ValuError, TypeError) as _:
            log.error('Received non integer input for service id (%s)' % service_string)

        a = meta.Session.query(Service).filter(Service.service_id == service_id)
        if a.count() == 0:
            log.error('Can\'t find your specified service. $d' % service_id)
        elif a.count() > 1:
            log.error('This is strange. Your service id is not unique!')

        service = a.one()
        hostname = service.resource.hostname

        a = meta.Session.query(Account).filter(sa.and_(
                                            Account.resource_id == service.resource.resource_id,
                                            sa.or_(Account.id.in_(session['user_groups']),
                                                Account.user_id == session['user_id']))
                                            ).order_by([Account.user_id,Account.id])

        if a.count() == 0:
            message = 'There are no accounts available on resource %s' % service.resource.name
            log.info(message)
            return {'error': True, 'message': message, 'resources': session['available_resources'].keys()}
        elif a.count() == 1:
            account = a.one()

            user = account.username
            password = account.password
            key = account.key if account.key else None
        else:
            log.error('TODO: Manage account ordering!!!')

            account = a.one()
            user = account.username
            password = account.password
            key = account.key if account.key else None

        try:
            config = Config(file('cyberweb/lib/jodis/resources.cfg'))

            # Populate resources from Database. Currently connect using all accounts
            # that match our criteria. We need/want to add logic to find the appropriate
            # account to use.
            for account in a.all():
                server = account.resource
                if server.active == 1:
                    log.info('Making connection to %s via %s',server.name, account.accountname)
                    if True or not app_globals.resourcelist.has_key(server.name):
                        try:
                            app_globals.manager.addMyResource(server.name,20)
                        except:
                            log.error('Error adding resources: %s' % server.name)
                        else:
                            session['available_resources'][server.name] = app_globals.resourcelist[server.name]
                            log.info('%s successfully connected to %s.' % (session.get('user','cwguest'),server.name))
                    else:
                        log.info('Connection to %s already exists' % server.name)

            # set globals
            self.jodis = app_globals.jodis
            self.manager = app_globals.manager
            log.info('Finished connecting to %s' % server.name)
        except:
            log.error('Error thrown while trying to start Jodis connections.')
            return {'error': True, 'message': 'Unknown Exception', 'resources': session['available_resources'].keys()}

        session.save()
        meta.Session.close()
        return {'error': False, 'message': 'success', 'resources': session['available_resources'].keys()}

    @jsonify
    def my_resources(self):
        if not session.get('user',None):
            return []

        #meta.Session.query(Account).filter(sa.or_(Account.cw_user_id == 1,Account.group_id.in_([5,4,6,3]))
        #meta.Session.close()
        my_resources = []
        return my_resources

    @jsonify
    def session_id(self):
        c.test = 'hi'
        return session.id
