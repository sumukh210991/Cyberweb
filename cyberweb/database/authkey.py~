import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, AuthKey, User

class AuthKeyOperation(object):
        
    def add(self, parameters):
        if parameters:
            username = ''
            userId = 0
            privatekey = ''
            publickey = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'private_key':
                    privatekey = value
                elif key == 'userId':
                    userId = value
                elif key == 'public_key':
                    publickey = value
                elif key == 'active':
                    active = value
            
            if active == 'True':
                active = 1
            else:
                active = 0
                      
            authKeyObj = AuthKey(privatekey,publickey,userId,active)
            meta.Session.add(authKeyObj)
            meta.Session.commit()
            #meta.Session.close()

        return '{"message":"Record Saved Successfully","dataId":"%d"}' % authKeyObj.id
    
    def update(self, parameters):
        if parameters:
            username = ''
            userId = 0
            privatekey = ''
            publickey = ''
            authKeyId = 0
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'authKeyId':
                    authKeyId = value
                elif key == 'private_key':
                    privatekey = value
                elif key == 'userId':
                    userId = value
                elif key == 'public_key':
                    publickey = value
                elif key == 'active':
                    active = value
            
            if active == 'True':
                active = 1
            else:
                active = 0
                       
            authKeyObj = meta.Session.query(AuthKey).filter(AuthKey.id == authKeyId).first()
            
            authKeyObj.private_key = privatekey
            authKeyObj.public_key = publickey
            authKeyObj.user_id = userId
            authKeyObj.active = active
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
                authKeyObj = meta.Session.query(AuthKey).filter(AuthKey.id == id).first()
                session.delete(authKeyObj)
                deleteCount = deleteCount + 1
        
        session.commit()
        #meta.Session.close()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        authKey = meta.Session.query(AuthKey).all()
        dataString = '['
        for authKeyNames in authKey:
            userObj = meta.Session.query(User).filter(User.id == authKeyNames.user_id).first();
            dataString += '{'
            dataString += '"authKeyId":"%s",' % authKeyNames.id
            dataString += '"private_key":"%s",' % re.escape(authKeyNames.private_key)
            dataString += '"public_key":"%s",' % re.escape(authKeyNames.public_key)
            dataString += '"userName":"%s",' % userObj.username
            dataString += '"active":"%s"' % authKeyNames.active
            dataString += '},'
            
        if len(dataString) > 1 :
            dataString = dataString[0:len(dataString)-1];
            
        dataString += ']'
        return dataString