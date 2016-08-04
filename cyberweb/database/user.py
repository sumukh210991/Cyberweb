import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
# import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, User
from config import Config

myclass, myfunc = config.get('authkit.form.authenticate.user.encrypt',':').split(':')
mysecret = config.get('authkit.form.authenticate.user.encrypt.secret','')

try:
    exec('from %s import %s as encrypt' % (myclass,myfunc))
except:
    log.error('No encrypt function is being used for passwords!(%s.%s)',myclass,myfunc)
    encrypt = lambda x,y: x

class UserOperation(object):
        
    def add(self, parameters):
        if parameters:
            username = ''
            password = ''
            name = ''
            email = ''
            institution = ''
            active = False
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'username':
                    username = value
                elif key == 'password':
                    password = encrypt(value,mysecret)
                elif key == 'name':
                    name = value
                elif key == 'email':
                    email = value
                elif key == 'institution':
                    institution = value
                elif key == 'active':
                    active = value  
            
            if active == 'True':
                active = 1
            else:
                active = 0
                  
            name = name.encode('ascii','ignore')
            names = name.split()
            if len(names) > 0:
                firstName = names[0]
            else:
                firstName = ''
                
            if len(names) == 2:
                lastName = names[1]
            else:
                lastName = ''
            
            userObj = User(username,password,email,firstName,lastName,institution,active)
            meta.Session.add(userObj)
            meta.Session.commit()
            #meta.Session.close()
        return '{"message":"Record Saved Successfully","dataId":"%d"}' % userObj.id
    
    def update(self, parameters):
        if parameters:
            userId = 0
            username = ''
            password = ''
            name = ''
            email = ''
            institution = ''
            active = False
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'username':
                    username = value
                elif key == 'password':
                    password = encrypt(value,mysecret)
                elif key == 'name':
                    name = value
                elif key == 'email':
                    email = value
                elif key == 'institution':
                    institution = value
                elif key == 'userId':
                    userId = value
                elif key == 'active':
                    active = value
                    
            if active == 'True':
                active = 1
            else:
                active = 0
                
            name = name.encode('ascii','ignore')
            names = name.split()
            if len(names) > 0:
                firstName = names[0]
            else:
                firstName = ''
                
            if len(names) == 2:
                lastName = names[1]
            else:
                lastName = ''
                
            userObj = meta.Session.query(User).filter(User.id == userId).first()
            
            userObj.username = username
            if password != '':
                userObj.password = password
            userObj.firstname = firstName
            userObj.lastname = lastName
            userObj.email = email
            userObj.institution = institution
            userObj.active = active
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
                userObj = meta.Session.query(User).filter(User.id == id).first()
                session.delete(userObj)
                deleteCount = deleteCount + 1
        
        session.commit()
        #meta.Session.close()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        user = meta.Session.query(User).all()
        dataString = '['
        for userNames in user:
            dataString += '{'
            dataString += '"id":"%s",' % userNames.id
            dataString += '"userName":"%s",' % re.escape(userNames.username)
            dataString += '"fullName":"%s %s",' % (re.escape(userNames.firstname),re.escape(userNames.lastname))
            dataString += '"email":"%s",' % re.escape(userNames.email)
            dataString += '"institution":"%s",' % userNames.institution
            dataString += '"active":"%s",' % userNames.active
            dataString += '"created":"%s"' % userNames.created
            dataString += '},'
            
        if len(dataString) > 1 :
            dataString = dataString[0:len(dataString)-1];
            
        dataString += ']'
        return dataString
