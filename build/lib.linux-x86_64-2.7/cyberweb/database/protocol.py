import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, Protocol

class ProtocolOperation(object):
        
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
                
            protocolObj = Protocol(name,description,active)
            meta.Session.add(protocolObj)
            meta.Session.commit()
            #meta.Session.close()
        return '{"message":"Record Saved Successfully","dataId":"%d"}' % protocolObj.id
    
    def update(self, parameters):
        if parameters:
            protocolId = 0
            name = ''
            description = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'protocolId':
                    protocolId = value
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
            protocolObj = meta.Session.query(Protocol).filter(Protocol.id == protocolId).first()
            
            protocolObj.name = name
            protocolObj.description = description
            protocolObj.active = active
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
                protocolObj = meta.Session.query(Protocol).filter(Protocol.id == id).first()
                session.delete(protocolObj)
                deleteCount = deleteCount + 1
        
        session.commit()
        #meta.Session.close()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        protocol = meta.Session.query(Protocol).all()
        dataString = '['
        for protocolNames in protocol:
            dataString += '{'
            dataString += '"id":"%s",' % protocolNames.id
            if protocolNames.name:
                dataString += '"name":"%s",' % re.escape(protocolNames.name)
            else :
                dataString += '"name":"None",'
            
            if protocolNames.description:    
                dataString += '"description":"%s",' % re.escape(protocolNames.description)
            else :
                dataString += '"description":"None",'
            
            dataString += '"active":"%s"' % protocolNames.active
            dataString += '},'
            
        if len(dataString) > 1 :
            dataString = dataString[0:len(dataString)-1];
            
        dataString += ']'
        return dataString