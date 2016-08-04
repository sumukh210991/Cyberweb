import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, QueueInfo

class QueueInfoOperation(object):
        
    def add(self, parameters):
        if parameters:
            name = ''
            policy = ''
            no = 0
            max_walltime = 0
            max_jobs = 0
            max_CPUsPerJob = 0
            avg_waittime = 0
            num_nodes = 0
            cpus_per_node = 0
            param = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'name':
                    name = value
                elif key == 'policy':
                    policy = value
                elif key == 'no':
                    no = value
                elif key == 'max_walltime':
                    max_walltime = value
                elif key == 'max_jobs':
                    max_jobs = value
                elif key == 'max_CPUsPerJob':
                    max_CPUsPerJob = value
                elif key == 'avg_waittime':
                    avg_waittime = value
                elif key == 'num_nodes':
                    num_nodes = value
                elif key == 'cpus_per_node':
                    cpus_per_node = value
                elif key == 'parameters':
                    param = value
                elif key == 'active':
                    active = value
            
            if active == 'True':
                active = 1
            else:
                active = 0
                   
            queueInfoObj = QueueInfo()
            queueInfoObj.name = name
            queueInfoObj.policy = policy
            queueInfoObj.no = no
            queueInfoObj.max_walltime = max_walltime
            queueInfoObj.max_jobs = max_jobs
            queueInfoObj.max_CPUsPerJob = max_CPUsPerJob
            queueInfoObj.avg_waittime = avg_waittime
            queueInfoObj.num_nodes = num_nodes
            queueInfoObj.cpus_per_node = cpus_per_node
            queueInfoObj.parameters = param
            queueInfoObj.active = active
            meta.Session.add(queueInfoObj)
            meta.Session.commit()
            
        return '{"message":"Record Saved Successfully","dataId":"%d"}' % queueInfoObj.id
    
    def update(self, parameters):
        if parameters:
            queueInfoId = 0
            name = ''
            policy = ''
            no = 0
            max_walltime = 0
            max_jobs = 0
            max_CPUsPerJob = 0
            avg_waittime = 0
            num_nodes = 0
            cpus_per_node = 0
            param = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'queueInfoId':
                    queueInfoId = value
                elif key == 'name':
                    name = value
                elif key == 'policy':
                    policy = value
                elif key == 'no':
                    no = value
                elif key == 'max_walltime':
                    max_walltime = value
                elif key == 'max_jobs':
                    max_jobs = value
                elif key == 'max_CPUsPerJob':
                    max_CPUsPerJob = value
                elif key == 'avg_waittime':
                    avg_waittime = value
                elif key == 'num_nodes':
                    num_nodes = value
                elif key == 'cpus_per_node':
                    cpus_per_node = value
                elif key == 'parameters':
                    param = value
                elif key == 'active':
                    active = value
            
            if active == 'True':
                active = 1
            else:
                active = 0
            queueInfoObj = meta.Session.query(QueueInfo).filter(QueueInfo.id == queueInfoId).first()
            
            queueInfoObj.name = name
            queueInfoObj.policy = policy
            queueInfoObj.no = no
            queueInfoObj.max_walltime = max_walltime
            queueInfoObj.max_jobs = max_jobs
            queueInfoObj.max_CPUsPerJob = max_CPUsPerJob
            queueInfoObj.avg_waittime = avg_waittime
            queueInfoObj.num_nodes = num_nodes
            queueInfoObj.cpus_per_node = cpus_per_node
            queueInfoObj.parameters = param
            queueInfoObj.active = active
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
                queueInfoObj = meta.Session.query(QueueInfo).filter(QueueInfo.id == id).first()
                session.delete(queueInfoObj)
                deleteCount = deleteCount + 1
        
        session.commit()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        queueInfo = meta.Session.query(QueueInfo).all()
        dataString = '['
        for queueInfoNames in queueInfo:
            dataString += '{'
            dataString += '"id":"%s",' % queueInfoNames.id
            if queueInfoNames.name:
                dataString += '"name":"%s",' % re.escape(queueInfoNames.name)
            else :
                dataString += '"name":"None",'
                
            dataString += '"no":"%s",' % queueInfoNames.no
            
            if queueInfoNames.policy:
                dataString += '"policy":"%s",' % re.escape(queueInfoNames.policy)
            else:
                dataString += '"policy":"None",'
                
            dataString += '"max_walltime":"%s",' % queueInfoNames.max_walltime
            dataString += '"max_jobs":"%s",' % queueInfoNames.max_jobs
            dataString += '"max_CPUsPerJob":"%s",' % queueInfoNames.max_CPUsPerJob
            dataString += '"avg_waittime":"%s",' % queueInfoNames.avg_waittime
            dataString += '"num_nodes":"%s",' % queueInfoNames.num_nodes
            dataString += '"cpus_per_node":"%s",' % queueInfoNames.cpus_per_node
            
            if queueInfoNames.parameters:
                dataString += '"parameters":"%s",' % re.escape(queueInfoNames.parameters)
            else :
                dataString += '"parameters":"None",'
            
            dataString += '"active":"%s",' % queueInfoNames.active
            dataString += '"timeStamp":"%s"' % queueInfoNames.timestamp                                                  
            dataString += '},'
            
        if len(dataString) > 1 :
            dataString = dataString[0:len(dataString)-1];
            
        dataString += ']'
        return dataString