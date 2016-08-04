import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, QueueType, QueueSystem

class QueueSystemOperation(object):
        
    def add(self, parameters):
        if parameters:
            name = ''
            path = ''
            submit = ''
            delete = ''
            status = ''
            other1 = ''
            other2 = ''
            queueTypeId = 0
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'name':
                    name = value
                elif key == 'path':
                    path = value
                elif key == 'submit':
                    submit = value
                elif key == 'deleteQueue':
                    delete = value
                elif key == 'status':
                    status = value
                elif key == 'other1':
                    other1 = value
                elif key == 'other2':
                    other2 = value
                elif key == 'queueTypeId':
                    queueTypeId = value
                elif key == 'active':
                    active = value
            
            if active == 'True':
                active = 1
            else:
                active = 0
            queueSystemObj = QueueSystem()
            queueSystemObj.name = name
            queueSystemObj.path = path
            queueSystemObj.submit = submit
            queueSystemObj.delete = delete
            queueSystemObj.status = status
            queueSystemObj.other1 = other1
            queueSystemObj.other2 = other2
            queueSystemObj.queuetype_id = queueTypeId
            queueSystemObj.active = active
            meta.Session.add(queueSystemObj)
            meta.Session.commit()
            
        return '{"message":"Record Saved Successfully","dataId":"%d"}' % queueSystemObj.id
    
    def update(self, parameters):
        if parameters:
            queueSystemId = 0
            name = ''
            path = ''
            submit = ''
            delete = ''
            status = ''
            other1 = ''
            other2 = ''
            queueTypeId = 0
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'queueSystemId':
                    queueSystemId = value
                elif key == 'name':
                    name = value
                elif key == 'path':
                    path = value
                elif key == 'submit':
                    submit = value
                elif key == 'deleteQueue':
                    delete = value
                elif key == 'status':
                    status = value
                elif key == 'other1':
                    other1 = value
                elif key == 'other2':
                    other2 = value
                elif key == 'queueTypeId':
                    queueTypeId = value
                elif key == 'active':
                    active = value
            
            if active == 'True':
                active = 1
            else:
                active = 0
                
            queueSystemObj = meta.Session.query(QueueSystem).filter(QueueSystem.id == queueSystemId).first()
            
            queueSystemObj.name = name
            queueSystemObj.path = path
            queueSystemObj.submit = submit
            queueSystemObj.delete = delete
            queueSystemObj.status = status
            queueSystemObj.other1 = other1
            queueSystemObj.other2 = other2
            queueSystemObj.queuetype_id = queueTypeId
            queueSystemObj.active = active
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
                queueSystemObj = meta.Session.query(QueueSystem).filter(QueueSystem.id == id).first()
                session.delete(queueSystemObj)
                deleteCount = deleteCount + 1
        
        session.commit()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        queueSystem = meta.Session.query(QueueSystem).all()
        dataString = '['
        for queueSystemNames in queueSystem:
            dataString += '{'
            dataString += '"id":"%s",' % queueSystemNames.id
            dataString += '"name":"%s",' % re.escape(queueSystemNames.name)
            dataString += '"path":"%s",' % re.escape(queueSystemNames.path)
            dataString += '"submit":"%s",' % re.escape(queueSystemNames.submit)
            dataString += '"deleteQueue":"%s",' % re.escape(queueSystemNames.delete)
            dataString += '"status":"%s",' % re.escape(queueSystemNames.status)
            dataString += '"other1":"%s",' % re.escape(queueSystemNames.other1)
            dataString += '"other2":"%s",' % re.escape(queueSystemNames.other2)
            
            if queueSystemNames.queuetype:
                dataString += '"queueType":"%s",' % re.escape(queueSystemNames.queuetype.name);
            else :
                dataString += '"queueType":"None",';
            
            dataString += '"active":"%s"' % queueSystemNames.active
            dataString += '},'
            
        if len(dataString) > 1 :
            dataString = dataString[0:len(dataString)-1];
            
        dataString += ']'
        return dataString