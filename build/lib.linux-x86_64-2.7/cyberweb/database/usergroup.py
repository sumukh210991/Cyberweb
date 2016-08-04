import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, User, GroupDefinition, Group

class UserGroupOperation(object):
        
    def add(self, parameters):
        if parameters:
            user_id = ''
            group_id = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'user_id':
                    user_id = value
                elif key == 'group_id':
                    group_id = value
                elif key == 'active':
                    active = value
                    
            if active == 'True':
                active = 1
            else:
                active = 0
                
            userGroupObj = Group(user_id,group_id,active)
            meta.Session.add(userGroupObj)
            meta.Session.commit()
            #meta.Session.close()
        return '{"message":"Record Saved Successfully","dataId":"%d"}' % userGroupObj.id
    
    def update(self, parameters):
        if parameters:
            userGroupId = 0
            user_id = ''
            group_id = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'userGroupId':
                    userGroupId = value
                elif key == 'user_id':
                    user_id = value
                elif key == 'group_id':
                    group_id = value
                elif key == 'active':
                    active = value
                    
            if active == 'True':
                active = 1
            else:
                active = 0
                
            userGroupObj = meta.Session.query(Group).filter(Group.id == userGroupId).first()
            
            userGroupObj.user_id = user_id
            userGroupObj.group_definition_id = group_id
            userGroupObj.active = active
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
                userGroupObj = meta.Session.query(Group).filter(Group.id == id).first()
                session.delete(userGroupObj)
                deleteCount = deleteCount + 1
        
        session.commit()
        #meta.Session.close()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        userGroup = meta.Session.query(Group).all()
        dataString = '['
        for userGroupNames in userGroup:
            userObj = meta.Session.query(User).filter(User.id == userGroupNames.user_id)
            groupObj = meta.Session.query(GroupDefinition).filter(GroupDefinition.id == userGroupNames.group_definition_id)
            
            if userObj.count() == 1 and groupObj.count() == 1:
                userData = userObj.one()
                groupData = groupObj.one()
                dataString += '{'
                dataString += '"id":"%s",' % userGroupNames.id
                dataString += '"userId":"%s",' % userData.id
                dataString += '"userName":"%s",' % re.escape(userData.username)
                dataString += '"groupId":"%s",' % groupData.id
                dataString += '"groupName":"%s",' % re.escape(groupData.name)
                dataString += '"active":"%s"' % userGroupNames.active
                dataString += '},'
            
        if len(dataString) > 1 :
            dataString = dataString[0:len(dataString)-1];
            
        dataString += ']'
        return dataString