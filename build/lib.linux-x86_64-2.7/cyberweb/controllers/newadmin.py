import logging
import sys
import re

from pylons import config, request, response, session, app_globals, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify
from formalchemy import FieldSet, Grid
import sqlalchemy as sa
import sqlalchemy.exceptions as sa_error

# add authentication to control who can access this class.
from authkit.authorize.pylons_adaptors import authorize
from cyberweb.lib import auth

from cyberweb.lib.base import BaseController, render

from cyberweb import database

from cyberweb.database import account, authkey, user, group, usergroup, messagetype, message, protocol, servicetype, servicename, \
                        queueinfo, queueservice, queuesystem, queuetype, job, resourcename, resourceservicelink
from cyberweb.database.account import *
from cyberweb.database.authkey import *
from cyberweb.database.user import *
from cyberweb.database.group import *
from cyberweb.database.usergroup import *
from cyberweb.database.messagetype import *
from cyberweb.database.message import *
from cyberweb.database.protocol import *
from cyberweb.database.servicetype import *
from cyberweb.database.servicename import *
from cyberweb.database.queueinfo import *
from cyberweb.database.queueservice import *
from cyberweb.database.queuesystem import *
from cyberweb.database.queuetype import *
from cyberweb.database.job import *
from cyberweb.database.resourcename import *
from cyberweb.database.resourceservicelink import *

from cyberweb import model
from cyberweb.model import meta, User, GroupDefinition, resource, Account, \
                        AuthKey, ServiceType, ServiceName, service, User, Group, Protocol, MessageType, Message, QueueInfo, QueueType, QueueSystem, QueueService
from cyberweb.model.resource import Resource
from cyberweb.model.service import Service, ServiceName                       

from datetime import datetime

from webhelpers.html.builder import HTML, literal

database_dict = {
    'account': database.account.AccountOperation(),
    'authKey': database.authkey.AuthKeyOperation(),
    'user': database.user.UserOperation(),
    'group': database.group.GroupOperation(),
    'userGroup': database.usergroup.UserGroupOperation(),
    'messageType': database.messagetype.MessageTypeOperation(),
    'message': database.message.MessageOperation(),
    'protocol': database.protocol.ProtocolOperation(),
    'serviceType': database.servicetype.ServiceTypeOperation(),
    'serviceName': database.servicename.ServiceNameOperation(),
    'queueType': database.queuetype.QueueTypeOperation(),
    'queueInfo': database.queueinfo.QueueInfoOperation(),
    'queueSystem': database.queuesystem.QueueSystemOperation(),
    'queueService': database.queueservice.QueueServiceOperation(),
    'job': database.job.JobOperation(),
    'resourceName': database.resourcename.ResourceOperation(),
    'resourceServiceLink': database.resourceservicelink.ResourceServiceLinkOperation()
}

class UserAdmin(FieldSet):
    def __init__(self):
        FieldSet.__init__(self, User)
        self.add(Field('passwd1'))
        self.add(Field('passwd2'))
        include = [self.username,
                   self.passwd1.password().label(u'Password'),
                   self.passwd2.password().label(u'Confirm').\
                        validate(validators.passwords_match('passwd1')),
                   self.email,
                   self.firstname,
                   self.lastname,
                ]
        self.configure(include=inc)

class NewadminController(BaseController):

    @authorize(auth.is_admin)
    def __before__(self):
        pass

    def __init__(self):
        self.verified = False

    def index(self):
        return ''

    def user(self):
        group_definitions = []
        for i in meta.Session.query(GroupDefinition).all():
            group_definitions.append((i.name, i.id))

        u = meta.Session.query(User).all()
        grid = Grid(User, u)
        grid.configure(pk=False,
                     options=[grid.groups.dropdown(size=1, options=group_definitions)],
                     exclude=[grid.password, grid.last_login_date, grid.created, grid.last_login_ip, grid.messages_sent, grid.messages_by_user])

        c.form_data = literal(grid.render())
        return render('/admin/admin_tables.mako')

    def group(self):
        g = meta.Session.query(GroupDefinition).all()
        grid = Grid(GroupDefinition, g)
        grid.configure(pk=False, exclude=[grid.members]) 
        c.form_data = literal(grid.render())
        return render('/admin/admin_tables.mako')

    def resource(self):
        g = meta.Session.query(Resource).all()
        grid = Grid(Resource, g)
        grid.configure(pk=False) 
        c.form_data = literal(grid.render())
        return render('/admin/admin_tables.mako')

    def account(self):
        g = meta.Session.query(Account).all()
        grid = Grid(Account, g)
        grid.configure(pk=False) 
        c.form_data = literal(grid.render())
        return render('/admin/admin_tables.mako')

    def service_type(self):
        g = meta.Session.query(ServiceType).all()
        grid = Grid(Account, g)
        grid.configure(pk=False) 
        c.form_data = literal(grid.render())
        return render('/admin/admin_tables.mako')

    def service_name(self):
        g = meta.Session.query(ServiceName).all()
        grid = Grid(Account, g)
        grid.configure(pk=False) 
        c.form_data = literal(grid.render())
        return render('/admin/admin_tables.mako')
    
    def getNewAdmin(self):
        c.resource = [resource for resource in meta.Session.query(Resource).all()];
        c.service = [service for service in meta.Session.query(ServiceName).all()];
        return render('/admin/Queue.mako')
    
    def resourceDetails(self):
        c.resource = [resource for resource in meta.Session.query(Resource).all()];
        
        queueSystemString = '['
        for queueSystem in meta.Session.query(QueueSystem).all():
            queueSystemString += '{'
            queueSystemString += '"queueSystemId":"%s",' % queueSystem.id
            queueSystemString += '"queueSystemName":"%s"' % queueSystem.name
            queueSystemString += '},'
            
        if len(queueSystemString) > 1 :
            queueSystemString = queueSystemString[0:len(queueSystemString)-1];
            
        queueSystemString += ']'
        c.queueSystemString = re.escape(queueSystemString)
        return render('/admin/Resource.mako')
    
    def resourceServiceLinkDetails(self):
        c.resource = [resource for resource in meta.Session.query(Resource).all()];
        
        serviceString = '['
        for service in meta.Session.query(ServiceName).all():
            serviceString += '{'
            serviceString += '"serviceId":"%s",' % service.id
            serviceString += '"serviceName":"%s"' % service.name
            serviceString += '},'
            
        if len(serviceString) > 1 :
            serviceString = serviceString[0:len(serviceString)-1];
            
        serviceString += ']'
        c.serviceString = re.escape(serviceString)
        
        protocolString = '['
        for protocol in meta.Session.query(Protocol).all():
            protocolString += '{'
            protocolString += '"protocolId":"%s",' % protocol.id
            protocolString += '"protocolName":"%s"' % protocol.name
            protocolString += '},'
            
        if len(protocolString) > 1 :
            protocolString = protocolString[0:len(protocolString)-1];
            
        protocolString += ']'
        c.protocolString = re.escape(protocolString)
        
        return render('/admin/ResourceServiceLink.mako')
    
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
            return object.delete(parameter)
        elif method == 'view':
            return object.view(parameter)
        else:
            return ''
    
    def resourceSearch(self):
        dataString = '['
        resourceIds = request.params.get('resources')
        if resourceIds:
            listResourceIds = resourceIds.split(',')
            for resourceId in listResourceIds:
                try:
                    resource = meta.Session.query(Resource).filter(Resource.id == resourceId).one();
                    dataString += '\n\t{'
                    dataString += '\n\t\t"Resource Id":"%s",' % resourceId
                    dataString += '\n\t\t"Resource Name":"%s",' % resource.name
                    dataString += '\n\t\t"Services":[\n'
                    service = [service for service in meta.Session.query(Service).filter(Service.resource_id == resourceId)];
                    for serviceId in service:
                        dataString += '\n\t\t\t{'
                        protocol = meta.Session.query(Protocol).filter(Protocol.id == serviceId.protocol_id).first();
                        dataString += '\n\t\t\t\t"protocol":"%s",' % protocol.name
                        dataString += '\n\t\t\t\t"path":"%s",' % serviceId.path
                        dataString += '\n\t\t\t\t"command":"%s",' % serviceId.command
                        dataString += '\n\t\t\t\t"port":"%s",' % serviceId.port
                        servicename = [servicename for servicename in meta.Session.query(ServiceName).filter(ServiceName.id == serviceId.servicename_id).all()];
                        for serviceNameId in servicename:
                            try:
                                dataString += '\n\t\t\t\t"serviceName":"%s",' % serviceNameId.name
                                servicetype = meta.Session.query(ServiceType).filter(ServiceType.id == serviceNameId.service_type_id).one();
                                dataString += '\n\t\t\t\t"serviceType":"%s"' % servicetype.name
                            except:
                                dataString += '\n\t\t\t\t"serviceType":""'
                        dataString += '\n\t\t\t},'
                    dataString = dataString[0:len(dataString)-1];
                    dataString += '\n\t\t]'
                    dataString += '\n\t},'
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
            dataString = dataString[0:len(dataString)-1];
        dataString += '\n]'
        return dataString
    
    def serviceSearch(self):
        try:
            dataString = '['
            serviceIds = request.params.get('services')
            if serviceIds:
                listServiceIds = serviceIds.split(',')
                for serviceNameId in listServiceIds:
                    serviceName = meta.Session.query(ServiceName).filter(ServiceName.id == serviceNameId).first();
                    serviceList = [service for service in meta.Session.query(Service).filter(Service.servicename_id == serviceNameId)];
                    dataString += '\n\t{'
                    dataString += '\n\t\t"Service Id":"%s",' % serviceNameId
                    dataString += '\n\t\t"Service Name":"%s",' % serviceName.name
                    dataString += '\n\t\t"Resources":[\n'
                    for serviceId in serviceList:
                        resource = meta.Session.query(Resource).filter(Resource.id == serviceId.resource_id).first();
                        if resource:
                            dataString += '\n\t\t\t{'
                            dataString += '\n\t\t\t\t"resourceName":"%s",' % resource.name
                            dataString += '\n\t\t\t\t"hostName":"%s",' % resource.hostname
                            dataString += '\n\t\t\t\t"institution":"%s",' % resource.institution
                            dataString += '\n\t\t\t\t"path":"%s",' % resource.path
                            dataString += '\n\t\t\t\t"queue":"%s",' % resource.queue
                            dataString += '\n\t\t\t\t"timeStamp":"%s"' % resource.insert_date
                            dataString += '\n\t\t\t},'
                    dataString = dataString[0:len(dataString)-1];
                    dataString += '\n\t\t]'
                    dataString += '\n\t},'
                dataString = dataString[0:len(dataString)-1];
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        
        dataString += '\n]'
        return dataString 
    
    def accountDetails(self):
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
        
        userString = '['
        for users in meta.Session.query(User).all():
            userString += '{'
            userString += '"userId":"%s",' % users.id
            userString += '"userName":"%s"' % users.username
            userString += '},'
            
        if len(userString) > 1 :
            userString = userString[0:len(userString)-1];
            
        userString += ']'
        c.userString = re.escape(userString)
        
        c.resources = meta.Session.query(Resource).all();
        c.user = session['user']
        return render('/admin/Account.mako')
            
    def groupDetails(self):
        userString = '['
        for user in meta.Session.query(User).all():
            userString += '{'
            userString += '"id":"%s",' % user.id
            userString += '"userName":"%s"' % user.username
            userString += '},'
            
        if len(userString) > 1 :
            userString = userString[0:len(userString)-1];
            
        userString += ']'
        c.userString = re.escape(userString)
        
        groupString = '['
        for group in meta.Session.query(GroupDefinition).all():
            groupString += '{'
            groupString += '"id":"%s",' % group.id
            groupString += '"groupName":"%s"' % group.name
            groupString += '},'
            
        if len(groupString) > 1 :
            groupString = groupString[0:len(groupString)-1];
            
        groupString += ']'
        c.groupString = re.escape(groupString)
        
        return render('/admin/Group.mako')
    
    def protocolDetails(self):
        return render('/admin/Protocol.mako')
    
    def jobDetails(self):
        return render('/admin/Job.mako')
    
    def messageDetails(self):
        userString = '['
        for user in meta.Session.query(User).all():
            userString += '{'
            userString += '"id":"%s",' % user.id
            userString += '"userName":"%s"' % user.username
            userString += '},'
            
        if len(userString) > 1 :
            userString = userString[0:len(userString)-1];
            
        userString += ']'
        c.userString = re.escape(userString)
        
        groupString = '['
        for group in meta.Session.query(GroupDefinition).all():
            groupString += '{'
            groupString += '"id":"%s",' % group.id
            groupString += '"groupName":"%s"' % group.name
            groupString += '},'
            
        if len(groupString) > 1 :
            groupString = groupString[0:len(groupString)-1];
            
        groupString += ']'
        c.groupString = re.escape(groupString)
        
        messageTypeString = '['
        for messageType in meta.Session.query(MessageType).all():
            messageTypeString += '{'
            messageTypeString += '"id":"%s",' % messageType.id
            messageTypeString += '"messageTypeName":"%s"' % messageType.name
            messageTypeString += '},'
            
        if len(messageTypeString) > 1 :
            messageTypeString = messageTypeString[0:len(messageTypeString)-1];
            
        messageTypeString += ']'
        c.messageTypeString = re.escape(messageTypeString)
        return render('/admin/Message.mako')
    
    def serviceDetails(self):
        c.service = [service for service in meta.Session.query(ServiceName).all()];
        
        serviceTypeString = '['
        for serviceType in meta.Session.query(ServiceType).all():
            serviceTypeString += '{'
            serviceTypeString += '"id":"%s",' % serviceType.id
            serviceTypeString += '"serviceTypeName":"%s"' % serviceType.name
            serviceTypeString += '},'
            
        if len(serviceTypeString) > 1 :
            serviceTypeString = serviceTypeString[0:len(serviceTypeString)-1];
            
        serviceTypeString += ']'
        c.serviceTypeString = re.escape(serviceTypeString)
        return render('/admin/Service.mako')
    
#    def getResourceTypeDetails(self):
#        resourceType = meta.Session.query(ResourceType).all()
#        dataString = '['
#        for resourceTypeNames in resourceType:
#            dataString += '{'
#            dataString += '"id":"%s",' % resourceTypeNames.id
#            dataString += '"name":"%s",' % re.escape(resourceTypeNames.name)
#            dataString += '"description":"%s",' % re.escape(resourceTypeNames.description)
#            dataString += '},'
#            
#        if len(dataString) > 1 :
#            dataString = dataString[0:len(dataString)-1];
#            
#        dataString += ']'
#        return dataString

    def queueDetails(self):
        resourceString = '['
        for resource in meta.Session.query(Resource).all():
            resourceString += '{'
            resourceString += '"id":"%s",' % resource.id
            resourceString += '"resourceName":"%s"' % resource.name
            resourceString += '},'
            
        if len(resourceString) > 1 :
            resourceString = resourceString[0:len(resourceString)-1];
            
        resourceString += ']'
        c.resourceString = re.escape(resourceString)
        
        queueTypeString = '['
        for queueType in meta.Session.query(QueueType).all():
            queueTypeString += '{'
            queueTypeString += '"id":"%s",' % queueType.id
            queueTypeString += '"queueTypeName":"%s"' % queueType.name
            queueTypeString += '},'
            
        if len(queueTypeString) > 1 :
            queueTypeString = queueTypeString[0:len(queueTypeString)-1];
            
        queueTypeString += ']'
        c.queueTypeString = re.escape(queueTypeString)
        
        queueInfoString = '['
        for queueInfo in meta.Session.query(QueueInfo).all():
            queueInfoString += '{'
            queueInfoString += '"id":"%s",' % queueInfo.id
            queueInfoString += '"queueInfoName":"%s"' % queueInfo.name
            queueInfoString += '},'
            
        if len(queueInfoString) > 1 :
            queueInfoString = queueInfoString[0:len(queueInfoString)-1];
            
        queueInfoString += ']'
        c.queueInfoString = re.escape(queueInfoString)
        
        queueSystemString = '['
        for queueSystem in meta.Session.query(QueueSystem).all():
            queueSystemString += '{'
            queueSystemString += '"id":"%s",' % queueSystem.id
            queueSystemString += '"queueSystemName":"%s"' % queueSystem.name
            queueSystemString += '},'
            
        if len(queueSystemString) > 1 :
            queueSystemString = queueSystemString[0:len(queueSystemString)-1];
            
        queueSystemString += ']'
        c.queueSystemString = re.escape(queueSystemString)
        return render('/admin/Queue.mako')
    