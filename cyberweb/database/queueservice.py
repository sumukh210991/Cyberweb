import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
# import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, QueueSystem, QueueInfo, QueueService, Resource

class QueueServiceOperation(object):
        
    def add(self, parameters):
        if parameters:
            queueSystemId = 0
            queueInfoId = 0
            resourceId = 0
            bin_dir = ''
            arg_string = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'queueSystemId':
                    queueSystemId = value
                elif key == 'queueInfoId':
                    queueInfoId = value
                elif key == 'resourceId':
                    resourceId = value
                elif key == 'bin_dir':
                    bin_dir = value
                elif key == 'arg_string':
                    arg_string = value
                elif key == 'active':
                    active = value
                    
            if active == 'True':
                active = 1
            else:
                active = 0
                
            queueServiceObj = QueueService()
            queueServiceObj.queuesystem_id = queueSystemId
            queueServiceObj.queueinfo_id = queueInfoId
            queueServiceObj.resource_id = resourceId
            queueServiceObj.bin_dir = bin_dir
            queueServiceObj.arg_string = arg_string
            queueServiceObj.active = active
            meta.Session.add(queueServiceObj)
            meta.Session.commit()
            #meta.Session.close()
        return '{"message":"Record Saved Successfully","dataId":"%d"}' % queueServiceObj.id
    
    def update(self, parameters):
        if parameters:
            queueServiceId = 0
            queueSystemId = 0
            queueInfoId = 0
            resourceId = 0
            bin_dir = ''
            arg_string = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'queueServiceId':
                    queueServiceId = value
                elif key == 'queueSystemId':
                    queueSystemId = value
                elif key == 'queueInfoId':
                    queueInfoId = value
                elif key == 'resourceId':
                    resourceId = value
                elif key == 'bin_dir':
                    bin_dir = value
                elif key == 'arg_string':
                    arg_string = value
                elif key == 'active':
                    active = value
                    
            if active == 'True':
                active = 1
            else:
                active = 0
                
            queueServiceObj = meta.Session.query(QueueService).filter(QueueService.id == queueServiceId).first()
            
            queueServiceObj.queuesystem_id = queueSystemId
            queueServiceObj.queueinfo_id = queueInfoId
            queueServiceObj.resource_id = resourceId
            queueServiceObj.bin_dir = bin_dir
            queueServiceObj.arg_string = arg_string
            queueServiceObj.active = active
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
                queueServiceObj = meta.Session.query(QueueService).filter(QueueService.id == id).first()
                session.delete(queueServiceObj)
                deleteCount = deleteCount + 1
        
        session.commit()
        #meta.Session.close()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        queueService = meta.Session.query(QueueService).all()
        dataString = '['
        for queueServiceNames in queueService:
            
            dataString += '{'
            dataString += '"id":"%s",' % queueServiceNames.id
            dataString += '"bin_dir":"%s",' % queueServiceNames.bin_dir
            dataString += '"arg_string":"%s",' % queueServiceNames.arg_string
            
            if queueServiceNames.queuesystem and queueServiceNames.queuesystem.name:
                dataString += '"queueSystemName":"%s",' % re.escape(queueServiceNames.queuesystem.name);
            else :
                dataString += '"queueSystemName":"None",';
                
            if queueServiceNames.queueinfo and queueServiceNames.queueinfo.name:
                dataString += '"queueInfoName":"%s",' % re.escape(queueServiceNames.queueinfo.name);
            else :
                dataString += '"queueInfoName":"None",'
                
                
            if queueServiceNames.resource and queueServiceNames.resource.name:
                dataString += '"resourceName":"%s",' % re.escape(queueServiceNames.resource.name);
            else :
                dataString += '"resourceName":"None",'
            
            dataString += '"active":"%s"' % queueServiceNames.active
            dataString += '},';
            
        if len(dataString) > 1 :
            dataString = dataString[0:len(dataString)-1];
            
        dataString += ']'
        return dataString
