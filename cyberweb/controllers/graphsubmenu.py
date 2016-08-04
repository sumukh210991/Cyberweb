import logging
import sys
import os, time, math, tempfile
import numpy as np

from pylons import request, response, session, app_globals, tmpl_context as c, config
from pylons.decorators import jsonify
from authkit.authorize.pylons_adaptors import authorize,authorized
import sqlalchemy as sa
from sqlalchemy.orm.attributes import manager_of_class as manager
from config import Config

from cyberweb.lib.base import BaseController, render
from cyberweb.lib import auth, helpers as h, jobs as j
from cyberweb import model
from cyberweb.model import meta,JobState, Job, Message, Group, GroupDefinition, User, Service, ServiceName, Account

log = logging.getLogger(__name__)

try:
    import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
except ImportError:
    # kludge in case Gnuplot hasn't been installed as a module yet:
    import __init__
    Gnuplot = __init__
    import PlotItems
    Gnuplot.PlotItems = PlotItems
    import funcutils
    Gnuplot.funcutils = funcutils
    

CWPROJPATH = '/u06/cwproj/users/'
SESS_KEY = 'filebrowser_data'
    
class GraphsubmenuController(BaseController):

    @authorize(auth.is_valid_user)
    def __before__(self):
        pass

    def index(self):
        user_id = session.get('user_id')
        if not user_id:
            raise Exception
        
        # title
        # c.title = config.get('project.shortname','CyberWeb') + ' User Page for: ' + session.get('user','you')        
        c.title = 'Graphs'
        
        # Messages
        num_messages = 10
        messages = meta.Session.query(Message).filter(sa.or_(Message.recipient_group_id.in_(session['user_groups']),\
                                                             Message.recipient_user_id == session['user_id'],\
                                                             sa.and_(Message.recipient_group_id == sa.null(), Message.recipient_user_id == sa.null())))\
                                                             .order_by().limit(num_messages)
        c.messageheaders = ['Date','Message']
        c.messages = [ {'Date':i.date.strftime("%B %d,%Y"), 'Message':i.message} for i in messages ]
        # Recent jobs
        num_jobs = 4
        c.jobs = dict()
        c.jobs['Queued'] = j.getJobs(JobState.queued,user_id,num_jobs)
        c.jobs['Running'] = j.getJobs(JobState.running,user_id,num_jobs)
        c.jobs['Finished'] = j.getJobs(JobState.finished,user_id,num_jobs)
        c.jobs['Crashed'] = j.getJobs(JobState.error,user_id,num_jobs)
        c.jobheaders = j.getJobHeaders()
        # User Info
        user = meta.Session.query(User).filter(User.id == session.get('user_id')).one()
        c.info = dict()
        c.info['Last login'] = user.last_login_date
        c.info['from'] = user.last_login_ip
        c.myproxy_cmd=""
        meta.Session.close()
                
        box = request.params.get('box')
        path = request.params.get('path')
        hostname = request.params.get('host')

        if hostname and box:
            if not session[SESS_KEY][box].has_key('host') or session[SESS_KEY][box]['host'] != hostname:
                path = None

            session[SESS_KEY][box]['host'] = hostname
            session[SESS_KEY][box]['path'] = path
            session.save()
            return self._updatelisting(box)

        c.data = session[SESS_KEY]

       
        return render('/graphs/viz.mako')
    
    def drawgraph(self):
        path = request.params.get('path','')
        file = request.params.get('filename','')
        f = open(path + '/' + file, 'r')
        str = f.readline().strip()
        str = str.replace('[', '')
        str = str.replace(']', '')
        str = str.strip()
        str = str.split(',', 1)
        str2 = str[1].split(' ', 1)
        #print str2[0]
        
        str = f.readline().strip()
        str = str.replace('[', '')
        str = str.replace(']', '')
        str = str.strip()
        str = str.split(',', 1)
        str2 = str[1].split(' ', 1)
        #print str2[0]
        
        str = f.readline().strip()
        str = str.replace('[', '')
        str = str.replace(']', '')
        str = str.strip()
        str = str.split(',', 1)
        str2 = str[1].split(' ', 1)
        #print str2[0]
        
        str = f.readline().strip()
        str = str.replace('[', '')
        str = str.replace(']', '')
        str = str.strip()
        str = str.split(',', 1)
        str2 = str[1].split(' ', 1)
        #print str2[0]
        
        CumulativeSum = [0]
        CumulativeSumEveryNth = [0]
        x = 0
        if str2[0] == 'TPres':
            str3 = str2[1].split('}  {')
            for i in range(len(str3)):
                str3[i] = str3[i].replace('{', '')
                str3[i] = str3[i].replace('}', '')
                data = str3[i].split(',')
                #print i 
                #print '\t'
                initial = eval(data[1].strip())
                #print initial 
                #print '\t'
                end = eval(data[2].strip())
                #print end 
                #print '\t'
                if(len(CumulativeSum) == 1 and x == 0): 
                    CumulativeSum[0] = math.fabs(end - initial)
                    CumulativeSumEveryNth[0] = math.fabs(end - initial)
                    x = 1
                else:
                    if(i%200 == 0):
                        CumulativeSumEveryNth.append(math.fabs(end - initial + CumulativeSum[i-1]))
                    CumulativeSum.append(math.fabs(end - initial + CumulativeSum[i-1]))
                #print CumulativeSum[i]
                #print '\n'
        
        
        str = f.readline().strip()
        str = str.replace('[', '')
        str = str.replace(']', '')
        str = str.strip()
        str = str.split(',', 1)
        str2 = str[1].split(' ', 1)
        #print str2[0]
        
        CumulativeSumVel = [0]
        CumulativeSumVelEveryNth = [0]
        x = 0
        if str2[0] == 'TVel':
            str4 = str2[1].split('}  {')
            for i in range(len(str4)):
                str4[i] = str4[i].replace('{', '')
                str4[i] = str4[i].replace('}', '')
                data = str4[i].split(',')
                #print i 
                #print '\t'
                initial = eval(data[1].strip())
                #print initial 
                #print '\t'
                end = eval(data[2].strip())
                #print end 
                #print '\t'
                if(len(CumulativeSumVel) == 1 and x == 0): 
                    CumulativeSumVel[0] = math.fabs(end - initial)
                    CumulativeSumVelEveryNth[0] = math.fabs(end - initial)
                    x = 1
                else: 
                    if(i%400 == 0):
                        CumulativeSumVelEveryNth.append(math.fabs(end - initial + CumulativeSumVel[i-1]))
                    CumulativeSumVel.append(math.fabs(end - initial + CumulativeSumVel[i-1]))
    
        str = f.readline().strip()
        str = str.replace('[', '')
        str = str.replace(']', '')
        str = str.strip()
        str = str.split(',', 1)
        str2 = str[1].split(' ', 1)
    
        CumulativeSumFile = [0]
        x = 0
        if str2[0] == 'Tfile':
            str4 = str2[1].split('}  {')
            for i in range(len(str4)):
                str4[i] = str4[i].replace('{', '')
                str4[i] = str4[i].replace('}', '')
                data = str4[i].split(',')
                initial = eval(data[1].strip())
                end = eval(data[2].strip())
                if(len(CumulativeSumFile) == 1 and x == 0): 
                    CumulativeSumFile[0] = math.fabs(end - initial)
                    x = 1
                else: 
                    CumulativeSumFile.append(math.fabs(end - initial + CumulativeSumFile[i-1]))
    
                
        #print 'Elements in CumulativeSum: %d' % len(CumulativeSum)
        f.close()
        
        filename = path + '/' + "parsing.dat"
        try:
            FILE = open(filename,"w")
        except:
            print "File parsing.dat cant be opened."
        for i in range(len(CumulativeSum)):
            FILE.write("%i" % i )
            FILE.write('\t')
            FILE.write("%f" % CumulativeSum[i])
            FILE.write('\n')
        
        FILE.close()
    
    
        filenamePressEveryNth = path + '/' + "parsingPressEveryNth.dat"
        try:
            FILE = open(filenamePressEveryNth,"w")
        except:
            print "File parsing.dat cant be opened."
        for i in range(len(CumulativeSumEveryNth)):
            y = i*200
            FILE.write("%i" % y)
            FILE.write('\t')
            FILE.write("%f" % CumulativeSumEveryNth[i])
            FILE.write('\n')
        
        FILE.close()
    
        filename1 = path + '/' + "parsingVel.dat"
        try:
            FILE = open(filename1,"w")
        except:
            print "File parsing.dat cant be opened."
        for i in range(len(CumulativeSumVel)):
            FILE.write("%i" % i )
            FILE.write('\t')
            FILE.write("%f" % CumulativeSumVel[i])
            FILE.write('\n')
        
        FILE.close()
    
        filenameVelocityEveryNth = path + '/' + "filenameVelocityEveryNth.dat"
        try:
            FILE = open(filenameVelocityEveryNth,"w")
        except:
            print "File parsing.dat cant be opened."
        for i in range(len(CumulativeSumVelEveryNth)):
            y = i*400
            FILE.write("%i" %  y)
            FILE.write('\t')
            FILE.write("%f" % CumulativeSumVelEveryNth[i])
            FILE.write('\n')
        
        FILE.close()
    
        filename2 = path + '/' + "parsingFile.dat"
        try:
            FILE = open(filename2,"w")
        except:
            print "File parsing.dat cant be opened."
        for i in range(len(CumulativeSumFile)):
            FILE.write("%i" % i )
            FILE.write('\t')
            FILE.write("%f" % CumulativeSumFile[i])
            FILE.write('\n')
        
        FILE.close()
    
    
        
        #ploting file
        g = Gnuplot.Gnuplot(debug=1)
        g.clear()
        g.title('Pressure Timing plot')
        g.xlabel('MaxFileNo * Writeout freq.')
        g.ylabel('Y-Axis')
        g.plot(Gnuplot.File('/home/cyberweb/cwdata/cwusers/mary/ucoam/serucoam_ref_data/dolphin/job.139617/TDATA/parsing.dat', with_='lines'))
        g.hardcopy('/home/smita/cyberweb_new/cyberweb/public/images/parsing.svg', terminal='svg')    
        
        g.title('Velocity Timing plot')
        g.xlabel('MaxFileNo * Writeout freq.')
        g.ylabel('Y-Axis')
        g.plot(Gnuplot.File('/home/cyberweb/cwdata/cwusers/mary/ucoam/serucoam_ref_data/dolphin/job.139617/TDATA/parsingVel.dat', with_='lines'))
        #g.plot(Gnuplot.File(filename, every=5, with_='lines'))
        g.hardcopy('/home/smita/cyberweb_new/cyberweb/public/images/parsingVel.svg', terminal='svg')
        
        g.title('File I/O plot')
        g.xlabel('MaxFileNo * Writeout freq.')
        g.ylabel('Y-Axis')
        g.plot(Gnuplot.File('/home/cyberweb/cwdata/cwusers/mary/ucoam/serucoam_ref_data/dolphin/job.139617/TDATA/parsingFile.dat', with_='lines'))
        #g.plot(Gnuplot.File(filename, every=5, with_='lines'))
        g.hardcopy('/home/smita/cyberweb_new/cyberweb/public/images/parsingFile.svg', terminal='svg')
        
        image = '/images/parsing.svg'
        return ('<img src=%s alt="image" style="width: 700px; height: 500px;"/>' % image)
        




