import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
# import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, ServiceType, ServiceName

class ServiceNameOperation(object):
        
    def add(self, parameters):
        if parameters:
            name = ''
            serviceTypeId = 0
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'name':
                    name = value
                elif key == 'serviceTypeId':
                    serviceTypeId = value
                elif key == 'active':
                    active = value
            
            if active == 'True':
                active = 1
            else:
                active = 0
                
            serviceNameObj = ServiceName(name,serviceTypeId,active)
            meta.Session.add(serviceNameObj)
            meta.Session.commit()
            #meta.Session.close()
        return '{"message":"Record Saved Successfully","dataId":"%d"}' % serviceNameObj.id
    
    def update(self, parameters):
        if parameters:
            groupId = 0
            name = ''
            description = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'serviceNameId':
                    serviceNameId = value
                elif key == 'name':
                    name = value
                elif key == 'serviceTypeId':
                    serviceTypeId = value
                elif key == 'active':
                    active = value
                    
            if active == 'True':
                active = 1
            else:
                active = 0
                
            serviceNameObj = meta.Session.query(ServiceName).filter(ServiceName.id == serviceNameId).first()
            
            serviceNameObj.name = name
            serviceNameObj.service_type_id = serviceTypeId
            serviceNameObj.active = active
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
                serviceNameObj = meta.Session.query(ServiceName).filter(ServiceName.id == id).first()
                session.delete(serviceNameObj)
                deleteCount = deleteCount + 1
        
        session.commit()
        #meta.Session.close()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        serviceName = meta.Session.query(ServiceName).all()
        dataString = '['
        for serviceNames in serviceName:
            dataString += '{'
            dataString += '"id":"%s",' % serviceNames.id
            dataString += '"name":"%s",' % re.escape(serviceNames.name)
            
            if serviceNames.service_type:
                dataString += '"serviceType":"%s",' % re.escape(serviceNames.service_type.name);
            else :
                dataString += '"serviceType":"None",';
            
            dataString += '"active":"%s"' % serviceNames.active
            dataString += '},'
            
        if len(dataString) > 1 :
            dataString = dataString[0:len(dataString)-1];
            
        dataString += ']'
        return dataString
