import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
# import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, ServiceType

class ServiceTypeOperation(object):
        
    def add(self, parameters):
        if parameters:
            name = ''
            description = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'name':
                    name = value
                elif key == 'description':
                    description = value
                elif key == 'active':
                    active = value
                    
            if active == 'True':
                active = 1
            else:
                active = 0
                
            serviceTypeObj = ServiceType(name,description,active)
            meta.Session.add(serviceTypeObj)
            meta.Session.commit()
            #meta.Session.close()
        return '{"message":"Record Saved Successfully","dataId":"%d"}' % serviceTypeObj.id
    
    def update(self, parameters):
        if parameters:
            serviceTypeId = 0
            name = ''
            description = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'serviceTypeId':
                    serviceTypeId = value
                elif key == 'name':
                    name = value
                elif key == 'description':
                    description = value
                elif key == 'active':
                    active = value
                    
            if active == 'True':
                active = 1
            else:
                active = 0
                
            serviceTypeObj = meta.Session.query(ServiceType).filter(ServiceType.id == serviceTypeId).first()
            
            serviceTypeObj.name = name
            serviceTypeObj.description = description
            serviceTypeObj.active = active
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
                serviceTypeObj = meta.Session.query(ServiceType).filter(ServiceType.id == id).first()
                session.delete(serviceTypeObj)
                deleteCount = deleteCount + 1
        
        session.commit()
        #meta.Session.close()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        serviceType = meta.Session.query(ServiceType).all()
        dataString = '['
        for serviceTypeNames in serviceType:
            dataString += '{'
            dataString += '"id":"%s",' % serviceTypeNames.id
            dataString += '"name":"%s",' % re.escape(serviceTypeNames.name)
            dataString += '"description":"%s",' % re.escape(serviceTypeNames.description)
            dataString += '"active":"%s"' % serviceTypeNames.active
            dataString += '},'
            
        if len(dataString) > 1 :
            dataString = dataString[0:len(dataString)-1];
            
        dataString += ']'
        return dataString
