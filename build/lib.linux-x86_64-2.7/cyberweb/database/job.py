import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, Job, JobState

class JobOperation(object):
    
    def add(self, parameters):
        pass
    def update(self, parameters):
        pass
    
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
                jobObj = meta.Session.query(Job).filter(Job.id == id).first()
                session.delete(jobObj)
                deleteCount = deleteCount + 1
        
        session.commit()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        job = meta.Session.query(Job).all()
        dataString = '['
        for jobNames in job:
            dataString += '{'
            dataString += '"id":"%s",' % jobNames.id
            if jobNames.name:
                dataString += '"name":"%s",' % re.escape(jobNames.name)
            else :
                dataString += '"name":"None",'
            
            if jobNames.user:
                dataString += '"userName":"%s",' % re.escape(jobNames.user.username)
            else:
                dataString += '"userName":"None",'
                
            if jobNames.service and jobNames.service.service_name:
                dataString += '"serviceName":"%s",' % re.escape(jobNames.service.service_name.name)
            else:
                dataString += '"serviceName":"None",'
                    
            dataString += '"parent_job_id":"%s",' % jobNames.parent_job_id
            dataString += '"state":"%s",' % JobState.get_name(jobNames.state)
            dataString += '"submit_time":"%s",' % jobNames.submit_time
            dataString += '"start_time":"%s",' % jobNames.start_time
            dataString += '"end_time":"%s",' % jobNames.end_time                                                
            dataString += '},'
            
        if len(dataString) > 1 :
            dataString = dataString[0:len(dataString)-1];
            
        dataString += ']'
        return dataString