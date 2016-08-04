import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
# import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, Message, MessageType, User, GroupDefinition

class MessageOperation(object):
        
    def add(self, parameters):
        if parameters:
            message = ''
            messageTypeId = 0
            authorId = 0
            recipientId = 0
            recipientType = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'message':
                    message = value
                elif key == 'messageTypeId':
                    messageTypeId = value
                elif key == 'authorId':
                    authorId = value
                elif key == 'recipientId':
                    recipientId = value
                elif key == 'recipientType':
                    recipientType = value
                elif key == 'active':
                    active = value
            
            if active == 'True':
                active = 1
            else:
                active = 0
                    
            if recipientType.lower() == 'group':
                messageObj = Message(authorId,recipientId,message,True,messageTypeId,active)
            elif recipientType.lower() == 'user':
                messageObj = Message(authorId,recipientId,message,False,messageTypeId,active)
            else:
                messageObj = Message(authorId,None,message,False,messageTypeId,active)
                
            meta.Session.add(messageObj)
            meta.Session.commit()
            #meta.Session.close()
        return '{"message":"Record Saved Successfully","dataId":"%d"}' % messageObj.id
    
    def update(self, parameters):
        if parameters:
            messageId = 0
            message = ''
            messageTypeId = 0
            authorId = 0
            recipientId = 0
            recipientType = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'messageId':
                    messageId = value
                elif key == 'message':
                    message = value
                elif key == 'messageTypeId':
                    messageTypeId = value
                elif key == 'authorId':
                    authorId = value
                elif key == 'recipientId':
                    recipientId = value
                elif key == 'recipientType':
                    recipientType = value
                elif key == 'active':
                    active = value
                    
            if active == 'True':
                active = 1
            else:
                active = 0
                
            messageObj = meta.Session.query(Message).filter(Message.id == messageId).first()
            
            messageObj.message = message
            messageObj.message_type_id = messageTypeId
            messageObj.author_id = authorId
            messageObj.active = active

            if recipientType.lower() == 'group':
                messageObj.recipient_user_id = None
                messageObj.recipient_group_id = recipientId
            elif recipientType.lower() == 'user':
                messageObj.recipient_user_id = recipientId
                messageObj.recipient_group_id = None
            else:
                messageObj.recipient_user_id = None
                messageObj.recipient_group_id = None
                
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
                messageObj = meta.Session.query(Message).filter(Message.id == id).first()
                session.delete(messageObj)
                deleteCount = deleteCount + 1
        
        session.commit()
        #meta.Session.close()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        message = meta.Session.query(Message).all()
        dataString = '['
        for messageNames in message:
            authorObj = meta.Session.query(User).filter(User.id == messageNames.author_id)
            userObj = meta.Session.query(User).filter(User.id == messageNames.recipient_user_id)
            groupObj = meta.Session.query(GroupDefinition).filter(GroupDefinition.id == messageNames.recipient_group_id)
            messageTypeObj = meta.Session.query(MessageType).filter(MessageType.id == messageNames.message_type_id).first()
            
            dataString += '{'
            dataString += '"id":"%s",' % messageNames.id
            dataString += '"message":"%s",' % re.escape(messageNames.message)
            if messageTypeObj:
                dataString += '"messageType":"%s",' % re.escape(messageTypeObj.name)
            else:
                dataString += '"messageType":"None",'
                
            if authorObj.count() == 1 :
                authorData = authorObj.one();
                dataString += '"author":"%s",' % re.escape(authorData.username);
            else :
                dataString += '"author":"None",';
                
            if userObj.count() == 1 :
                userData = userObj.one();
                dataString += '"recipient":"%s",' % re.escape(userData.username);
                dataString += '"recipient_type":"User",'
            elif groupObj.count() == 1 :
                groupData = groupObj.one();
                dataString += '"recipient":"%s",' % re.escape(groupData.name);
                dataString += '"recipient_type":"Group",'
            else :
                dataString += '"recipient":"None",'
                dataString += '"recipient_type":"None",'
            
            dataString += '"active":"%s",' % messageNames.active
            dataString += '"creationDate":"%s"' % messageNames.date;
            dataString += '},';
            
        if len(dataString) > 1 :
            dataString = dataString[0:len(dataString)-1];
            
        dataString += ']'
        return dataString
