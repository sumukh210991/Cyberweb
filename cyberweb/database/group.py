import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
# import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, GroupDefinition

class GroupOperation(object):
        
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
                
            groupObj = GroupDefinition(name,description,active)
            meta.Session.add(groupObj)
            meta.Session.commit()
            #meta.Session.close()

        return '{"message":"Record Saved Successfully","dataId":"%d"}' % groupObj.id
    
    def update(self, parameters):
        if parameters:
            groupId = 0
            name = ''
            description = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'groupId':
                    groupId = value
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
                    
            groupObj = meta.Session.query(GroupDefinition).filter(GroupDefinition.id == groupId).first()
            
            groupObj.name = name
            groupObj.description = description
            groupObj.active = active
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
                groupObj = meta.Session.query(GroupDefinition).filter(GroupDefinition.id == id).first()
                session.delete(groupObj)
                deleteCount = deleteCount + 1
        
        session.commit()
        #meta.Session.close()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        group = meta.Session.query(GroupDefinition).all()
        dataString = '['
        for groupNames in group:
            dataString += '{'
            dataString += '"id":"%s",' % groupNames.id
            dataString += '"name":"%s",' % re.escape(groupNames.name)
            dataString += '"description":"%s",' % re.escape(groupNames.description)
            dataString += '"active":"%s"' % groupNames.active
            dataString += '},'
            
        if len(dataString) > 1 :
            dataString = dataString[0:len(dataString)-1];
            
        dataString += ']'
        return dataString
