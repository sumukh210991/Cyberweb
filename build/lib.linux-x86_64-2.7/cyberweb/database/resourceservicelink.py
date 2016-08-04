import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, Resource, Service

class ResourceServiceLinkOperation(object):
    
    def add(self, parameters):
        if parameters:
            serviceNameId = 0
            protocolId = 0
            path = ''
            command = ''
            port = ''
            resourceId = 0
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'serviceNameId':
                    serviceNameId = int(value)
                elif key == 'protocolId':
                    protocolId = int(value)
                elif key == 'resourceId':
                    resourceId = int(value)
                elif key == 'path':
                    path = value
                elif key == 'command':
                    command = value
                elif key == 'port':
                    port = value
                elif key == 'active':
                    active = value
            
            if active == 'True':
                active = 1
            else:
                active = 0
                
            serviceObj = Service(serviceNameId,protocolId,resourceId,path,command,port,active)
            meta.Session.add(serviceObj)
            meta.Session.commit()
            #meta.Session.close()
        return '{"message":"Record Saved Successfully","dataId":"%d"}' % serviceObj.id
    
    def update(self, parameters):
        if parameters:
            serviceId = 0
            serviceNameId = 0
            protocolId = 0
            path = ''
            command = ''
            port = ''
            resourceId = 0
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'serviceId':
                    serviceId = int(value)
                elif key == 'serviceNameId':
                    serviceNameId = int(value)
                elif key == 'protocolId':
                    protocolId = int(value)
                elif key == 'resourceId':
                    resourceId = int(value)
                elif key == 'path':
                    path = value
                elif key == 'command':
                    command = value
                elif key == 'port':
                    port = value
                elif key == 'active':
                    active = value
                    
            if active == 'True':
                active = 1
            else:
                active = 0
                
            serviceObj = meta.Session.query(Service).filter(Service.id == serviceId).first()
            
            serviceObj.servicename_id = serviceNameId
            serviceObj.protocol_id = protocolId
            serviceObj.resource_id = resourceId
            serviceObj.path = path
            serviceObj.command = command
            serviceObj.port = port
            serviceObj.active = active
            #meta.Session.save(accountObj)
            meta.Session.commit()
            
            #meta.Session.close()
            
        return '{"message":"Record Saved Successfully"}'
    
    def delete(self, parameters):
        session = meta.Session()
        deleteCount = 1
        jdata = json.loads(parameters)
        ids = []
        for key, value in jdata.iteritems():
            if key == 'deleteId':
                my_splitter = shlex.shlex(value, posix=True)
                my_splitter.whitespace += ','
                my_splitter.whitespace_split = True
                ids = list(my_splitter)
                break
        for id in ids:
            id = id.replace("\0", "")
            if id:
                id = int(id)
                serviceObj = meta.Session.query(Service).filter(Service.id == id).first()
                session.delete(serviceObj)
                deleteCount = deleteCount + 1
        
        session.commit()
        #meta.Session.close()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        dataString = '['
        if parameters:
            resourceId = 0
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'resourceId':
                    resourceId = value
            
            service = [service for service in meta.Session.query(Service).filter(Service.resource_id == resourceId)];
            for serviceId in service:
                dataString += '{'
                dataString += '"id":"%s",' % serviceId.id
                if serviceId.service_name:
                    dataString += '"service_name":"%s",' % serviceId.service_name.name
                else:
                    dataString += '"service_name":"None",'
                    
                if serviceId.protocol:
                    dataString += '"protocol":"%s",' % serviceId.protocol.name
                else:
                    dataString += '"protocol":"None",'
                
                dataString += '"path":"%s",' % serviceId.path
                dataString += '"command":"%s",' % serviceId.command
                dataString += '"port":"%s",' % serviceId.port
                dataString += '"active":"%s",' % serviceId.active
                dataString += '"timestamp":"%s"' % serviceId.timestamp
                
                dataString += '},'
                
            if len(dataString) > 1 :
                dataString = dataString[0:len(dataString)-1];
                
        dataString += ']'
        return dataString