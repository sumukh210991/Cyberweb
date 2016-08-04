import logging
import os
import sys
import time
import numpy
import math

from pylons import request, response, session, app_globals, tmpl_context as c, config
from pylons.decorators import jsonify
from authkit.authorize.pylons_adaptors import authorize,authorized
import sqlalchemy as sa
from sqlalchemy.orm.attributes import manager_of_class as manager
from config import Config

from cyberweb.lib.base import BaseController, render
from cyberweb.lib import auth, helpers as h
from cyberweb import model
from cyberweb.model import meta,JobState, Job, Message, Group, GroupDefinition, User, Service, ServiceName, Account

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
    
log = logging.getLogger(__name__)

class GnugraphsController(BaseController):

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
        c.jobs['Queued'] = h.getJobs(JobState.queued,user_id,num_jobs)
        c.jobs['Running'] = h.getJobs(JobState.running,user_id,num_jobs)
        c.jobs['Finished'] = h.getJobs(JobState.finished,user_id,num_jobs)
        c.jobs['Crashed'] = h.getJobs(JobState.error,user_id,num_jobs)
        c.jobheaders = h.getJobHeaders()
        # User Info
        user = meta.Session.query(User).filter(User.id == session.get('user_id')).one()
        c.info = dict()
        c.info['Last login'] = user.last_login_date
        c.info['from'] = user.last_login_ip
        c.myproxy_cmd=""
        meta.Session.close()
        
        f = open('/home/cyberweb/cwdata/cwusers/mary/ucoam/serucoam_ref_data/dolphin/job.139617/TDATA/timer_serUCOAM.dat', 'r')
        for line in f.readlines(): 
            line = line.strip()                   
            line = line.replace('[', ' ')
            line = line.replace(']', ' ')
            line = line.strip()
            line = line.split(',', 1)
            str2 = line[1].split(' ', 1)
            if str2[0] == 'TPres':
                CumulativeSum = [0]
                CumulativeSumEveryNth = [0]
                x = 0
                str3 = str2[1].split('}  {')
                for i in range(len(str3)):
                    str3[i] = str3[i].replace('{', '')
                    str3[i] = str3[i].replace('}', '')
                    data = str3[i].split(',')
                    initial = eval(data[1].strip())
                    end = eval(data[2].strip())
                    if(len(CumulativeSum) == 1 and x == 0): 
                        CumulativeSum[0] = math.fabs(end - initial)
                        CumulativeSumEveryNth[0] = math.fabs(end - initial)
                        x = 1
                    else:
                        if(i%200 == 0):
                            CumulativeSumEveryNth.append(math.fabs(end - initial + CumulativeSum[i-1]))
                        CumulativeSum.append(math.fabs(end - initial + CumulativeSum[i-1]))  
            if str2[0] == 'TVel':
                CumulativeSumVel = [0]
                CumulativeSumVelEveryNth = [0]
                x = 0
                str4 = str2[1].split('}  {')
                for i in range(len(str4)):
                    str4[i] = str4[i].replace('{', '')
                    str4[i] = str4[i].replace('}', '')
                    data = str4[i].split(',')
                    initial = eval(data[1].strip())
                    end = eval(data[2].strip())
                    if(len(CumulativeSumVel) == 1 and x == 0): 
                        CumulativeSumVel[0] = math.fabs(end - initial)
                        CumulativeSumVelEveryNth[0] = math.fabs(end - initial)
                        x = 1
                    else: 
                        if(i%400 == 0):
                            CumulativeSumVelEveryNth.append(math.fabs(end - initial + CumulativeSumVel[i-1]))
                        CumulativeSumVel.append(math.fabs(end - initial + CumulativeSumVel[i-1]))
            if str2[0] == 'Tfile':
                CumulativeSumFile = [0]
                x = 0
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

        f.close()
                
        filename = "/home/cyberweb/cwdata/cwusers/mary/ucoam/serucoam_ref_data/dolphin/job.139617/TDATA/parsing.dat"
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
        
        filenamePressEveryNth = "/home/cyberweb/cwdata/cwusers/mary/ucoam/serucoam_ref_data/dolphin/job.139617/TDATA/parsingPressEveryNth.dat"
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
          
        filename1 = "/home/cyberweb/cwdata/cwusers/mary/ucoam/serucoam_ref_data/dolphin/job.139617/TDATA/parsingVel.dat"
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
    
        filenameVelocityEveryNth = "/home/cyberweb/cwdata/cwusers/mary/ucoam/serucoam_ref_data/dolphin/job.139617/TDATA/filenameVelocityEveryNth.dat"
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
    
        filename2 = "/home/cyberweb/cwdata/cwusers/mary/ucoam/serucoam_ref_data/dolphin/job.139617/TDATA/parsingFile.dat"
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
        g.plot(Gnuplot.File(filename, with_='lines'))
        g.hardcopy('/images/parsing.svg', terminal='svg')    
        g.plot(Gnuplot.File(filename, with_='lines'))
        g.hardcopy('/images/parsing.ps', mode='eps')
        
        g.title('Velocity Timing plot')
        g.xlabel('MaxFileNo * Writeout freq.')
        g.ylabel('Y-Axis')
        g.plot(Gnuplot.File(filename1, with_='lines'))
        #g.plot(Gnuplot.File(filename, every=5, with_='lines'))
        g.hardcopy('/images/parsingVel.svg', terminal='svg')
        g.plot(Gnuplot.File(filename1, with_='lines'))
        g.hardcopy('/images/parsingVel.ps', mode='eps')
    
        g.title('File I/O plot')
        g.xlabel('MaxFileNo * Writeout freq.')
        g.ylabel('Y-Axis')
        g.plot(Gnuplot.File(filename2, with_='lines'))
        #g.plot(Gnuplot.File(filename, every=5, with_='lines'))
        g.hardcopy('/images/parsingFile.svg', terminal='svg')
        g.plot(Gnuplot.File(filename2, with_='lines'))
        g.hardcopy('/images/parsingFile.ps', mode='eps')  
        
        return render('/graphs/gnugraphs.mako')
        





 