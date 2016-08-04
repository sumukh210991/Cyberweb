import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, QueueType

class QueueTypeOperation(object):
        
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
                
            queueTypeObj = QueueType()
            queueTypeObj.name = name
            queueTypeObj.description = description
            queueTypeObj.active = active
            meta.Session.add(queueTypeObj)
            meta.Session.commit()
            
        return '{"message":"Record Saved Successfully","dataId":"%d"}' % queueTypeObj.id
    
    def update(self, parameters):
        if parameters:
            queueTypeId = 0
            name = ''
            description = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'queueTypeId':
                    value = value.replace("\0", "")
                    queueTypeId = int(value)
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
                
            queueTypeObj = meta.Session.query(QueueType).filter(QueueType.id == queueTypeId).first();
            
            queueTypeObj.name = name
            queueTypeObj.description = description
            queueTypeObj.active = active
            
            meta.Session.commit()
            
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
                queueTypeObj = meta.Session.query(QueueType).filter(QueueType.id == id).first()
                session.delete(queueTypeObj)
                deleteCount = deleteCount + 1
        
        session.commit()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        queueType = meta.Session.query(QueueType).all()
        dataString = '['
        for queueTypeNames in queueType:
            dataString += '{'
            dataString += '"id":"%s",' % queueTypeNames.id
            dataString += '"name":"%s",' % re.escape(queueTypeNames.name)
            dataString += '"description":"%s",' % re.escape(queueTypeNames.description)
            dataString += '"active":"%s"' % queueTypeNames.active
            dataString += '},'
            
        if len(dataString) > 1 :
            dataString = dataString[0:len(dataString)-1];
            
        dataString += ']'
        return dataString