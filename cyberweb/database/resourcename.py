import logging
import DatabaseOperations
import json
import shlex
import sys
import re

from formalchemy import FieldSet, Grid
import sqlalchemy as sa
# import sqlalchemy.exceptions as sa_error

from pylons import config, request, response, session, app_globals, tmpl_context as c
from cyberweb.model import meta, Resource, Account
from config import Config

log = logging.getLogger(__name__)

class ResourceOperation(object):
        
    def add(self, parameters):
        if parameters:
            resourceName = ''
            hostName = ''
            institution = ''
            total_memory_gb = 1
            num_cpus = 1
            memory_per_cpu_gb = 1
            num_nodes = 1
            path = ''
            queue = ''
            active = False
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'resourceName':
                    resourceName = value
                elif key == 'hostName':
                    hostName = value
                elif key == 'institution':
                    institution = value
                elif key == 'total_memory_gb':
                    total_memory_gb = value
                elif key == 'num_cpus':
                    num_cpus = value
                elif key == 'memory_per_cpu_gb':
                    memory_per_cpu_gb = value
                elif key == 'num_nodes':
                    num_nodes = value
                elif key == 'path':
                    path = value
                elif key == 'queue':
                    queue = value
                elif key == 'active':
                    active = value
                    
            if active == 'True' or active == True:
                active = 1
            else:
                active = 0
                
            resourceObj = Resource(resourceName,hostName,institution,total_memory_gb,num_cpus,memory_per_cpu_gb,num_nodes,path,queue,active)
            meta.Session.add(resourceObj)
            meta.Session.commit()
            
        return '{"message":"Record Saved Successfully","dataId":"%d"}' % resourceObj.id
    
    def update(self, parameters):
        if parameters:
            resourceNameId = 0
            resourceName = ''
            hostName = ''
            institution = ''
            total_memory_gb = 1
            num_cpus = 1
            memory_per_cpu_gb = 1
            num_nodes = 1
            path = ''
            queue = ''
            active = True
            
            jdata = json.loads(parameters)
            for key, value in jdata.iteritems():
                if key == 'resourceNameId':
                    resourceNameId = value
                elif key == 'resourceName':
                    resourceName = value
                elif key == 'hostName':
                    hostName = value
                elif key == 'institution':
                    institution = value
                elif key == 'total_memory_gb':
                    total_memory_gb = value
                elif key == 'num_cpus':
                    num_cpus = value
                elif key == 'memory_per_cpu_gb':
                    memory_per_cpu_gb = value
                elif key == 'num_nodes':
                    num_nodes = value
                elif key == 'path':
                    path = value
                elif key == 'queue':
                    queue = value
                elif key == 'active':
                    active = value
            
            if active == 'True':
                active = 1
            else:
                active = 0
                
            resourceObj = meta.Session.query(Resource).filter(Resource.id == resourceNameId).first()
            
            resourceObj.name = resourceName
            resourceObj.hostname = hostName
            resourceObj.institution = institution
            resourceObj.total_memory_gb = total_memory_gb
            resourceObj.num_cpus = num_cpus
            resourceObj.memory_per_cpu_gb = memory_per_cpu_gb
            resourceObj.num_nodes = num_nodes
            resourceObj.path = path
            resourceObj.queue = queue
            resourceObj.active = active        
            meta.Session.commit()
            
            if active == 0:
                if app_globals.available_resources.has_key(resourceObj.hostname):
                    del(app_globals.available_resources[resourceObj.hostname])
            elif active == 1:
                self.jodis_connect(resourceNameId)
            
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
                resourceObj = meta.Session.query(Resource).filter(Resource.id == id).first()
                session.delete(resourceObj)
                if app_globals.available_resources.has_key(resourceObj.hostname):
                    del(app_globals.available_resources[resourceObj.hostname])
                deleteCount = deleteCount + 1
        
        session.commit()
        
        return '{"message":"%d records deleted"}' % deleteCount
    
    def view(self, parameters):
        resourceName = meta.Session.query(Resource).all()
        dataString = '['
        for resourceNames in resourceName:
            dataString += '{'
            dataString += '"id":"%s",' % resourceNames.id
            if resourceNames.name:
                dataString += '"resourceName":"%s",' % re.escape(resourceNames.name)
            else :
                dataString += '"resourceName":"None",'
            
            if resourceNames.hostname:
                dataString += '"hostName":"%s",' % re.escape(resourceNames.hostname)
            else:
                dataString += '"hostName":"None",'
            
            if resourceNames.institution:
                dataString += '"institution":"%s",' % re.escape(resourceNames.institution)
            else:
                dataString += '"institution":"None",'
                
            dataString += '"total_memory_gb":"%s",' % resourceNames.total_memory_gb
            dataString += '"num_cpus":"%s",' % resourceNames.num_cpus
            dataString += '"memory_per_cpu_gb":"%s",' % resourceNames.memory_per_cpu_gb
            dataString += '"num_nodes":"%s",' % resourceNames.num_nodes
            
            if resourceNames.path:
                dataString += '"path":"%s",' % re.escape(resourceNames.path)
            else :
                dataString += '"path":"None",'
            
            if resourceNames.queue:
                dataString += '"queue":"%s",' % re.escape(resourceNames.queue)
            else :
                dataString += '"queue":"None",'
            
            dataString += '"active":"%s",' % resourceNames.active
            dataString += '"timeStamp":"%s"' % resourceNames.insert_date                                                  
            dataString += '},'
            
        if len(dataString) > 1 :
            dataString = dataString[0:len(dataString)-1];
            
        dataString += ']'
        return dataString
    
    def jodis_connect(self, resource_id):
        config = Config(file('cyberweb/lib/jodis/resources.cfg'))
        a = meta.Session.query(Account).filter(Account.resource_id == resource_id);
        # Populate resources from Database. Currently connect using all accounts
        # that match our criteria. We need/want to add logic to find the appropriate
        # account to use.
        for account in a.all():
            server = account.resource
            if server.active == 1:
                log.info('Making connection to %s via %s',server.name, account.name)
                if True or not app_globals.available_resources.has_key(server.hostname):
                    if app_globals.jodis.manager.addMyResource(account.id, maxjobs=20, myglobals=app_globals):
                        app_globals.available_resources[account.id] = {'hostname': server.hostname, 'name': server.name}
                    log.info('%s successfully connected to %s.' % (session.get('user','cwguest'),server.name))
                else:
                    log.info('Connection to %s already exists' % server.name)

        log.info('Finished connecting to %s' % server.name)

        session.save()
        meta.Session.close()
