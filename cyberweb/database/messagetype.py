import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
# import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, MessageType

class MessageTypeOperation(object):
        
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
            messageTypeObj = MessageType(name,description,active)
            meta.Session.add(messageTypeObj)
            meta.Session.commit()
            #meta.Session.close()
        return '{"message":"Record Saved Successfully","dataId":"%d"}' % messageTypeObj.id
    
    def update(self, parameters):
        if parameters:
            messageTypeId = 0
            name = ''
            description = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'messageTypeId':
                    messageTypeId = value
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
                
            messageTypeObj = meta.Session.query(MessageType).filter(MessageType.id == messageTypeId).first()
            
            messageTypeObj.name = name
            messageTypeObj.description = description
            messageTypeObj.active = active
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
                messageTypeObj = meta.Session.query(MessageType).filter(MessageType.id == id).first()
                session.delete(messageTypeObj)
                deleteCount = deleteCount + 1
        
        session.commit()
        #meta.Session.close()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        messageType = meta.Session.query(MessageType).all()
        dataString = '['
        for messageTypeNames in messageType:
            dataString += '{'
            dataString += '"id":"%s",' % messageTypeNames.id
            dataString += '"name":"%s",' % re.escape(messageTypeNames.name)
            dataString += '"description":"%s",' % re.escape(messageTypeNames.description)
            dataString += '"active":"%s"' % messageTypeNames.active
            dataString += '},'
            
        if len(dataString) > 1 :
            dataString = dataString[0:len(dataString)-1];
            
        dataString += ']'
        return dataString
