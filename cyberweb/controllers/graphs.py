import logging
import os
import sys
import time
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
from mpl_toolkits.axes_grid1 import host_subplot
from pylab import *
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

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

log = logging.getLogger(__name__)

class GraphsController(BaseController):

    @authorize(auth.is_valid_user)
    def __before__(self):
        pass

    def index(self):
        user_id = session.get('user_id')
        if not user_id:
            raise Exception
        
        # title
        # c.title = config.get('project.shortname','CyberWeb') + ' User Page for: ' + session.get('user','you')
        if 1:
        
            host = host_subplot(111, axes_class=AA.Axes)
            plt.subplots_adjust(right=0.75)
        
            par1 = host.twinx()
            par2 = host.twinx()
        
            offset = 60
            new_fixed_axis = par2.get_grid_helper().new_fixed_axis
            par2.axis["right"] = new_fixed_axis(loc="right",
                                                axes=par2,
                                                offset=(offset, 0))
        
            par2.axis["right"].toggle(all=True)
        
        
        
            host.set_xlim(0, 2)
            host.set_ylim(0, 2)
        
            host.set_xlabel("Distance")
            host.set_ylabel("Density")
            par1.set_ylabel("Temperature")
            par2.set_ylabel("Velocity")
        
            p1, = host.plot([0, 1, 2], [0, 1, 2], label="Density")
            p2, = par1.plot([0, 1, 2], [0, 3, 2], label="Temperature")
            p3, = par2.plot([0, 1, 2], [50, 30, 15], label="Velocity")
        
            par1.set_ylim(0, 4)
            par2.set_ylim(1, 65)
        
            host.legend()
        
            host.axis["left"].label.set_color(p1.get_color())
            par1.axis["right"].label.set_color(p2.get_color())
            par2.axis["right"].label.set_color(p3.get_color())
        
            plt.draw()
            plt.savefig('/Users/smitamore/cyberweb/cyberweb/public/images/test1.png')
        
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
       
        return render('/graphs/graphs.mako')





    def graph1(self):
        user_id = session.get('user_id')
        if not user_id:
            raise Exception


        matplotlib.rcParams['xtick.direction'] = 'out'
        matplotlib.rcParams['ytick.direction'] = 'out'
        
        delta = 0.025
        x = np.arange(-3.0, 3.0, delta)
        y = np.arange(-2.0, 2.0, delta)
        X, Y = np.meshgrid(x, y)
        Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
        Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
        # difference of Gaussians
        Z = 10.0 * (Z2 - Z1)
        
        
        
        # Create a simple contour plot with labels using default colors.  The
        # inline argument to clabel will control whether the labels are draw
        # over the line segments of the contour, removing the lines beneath
        # the label
        plt.figure()
        CS = plt.contour(X, Y, Z)
        plt.clabel(CS, inline=1, fontsize=10)
        plt.title('Simplest default with labels')
        
        plt.savefig('/Users/smitamore/cyberweb/cyberweb/public/images/contour1.png')
        
        # You can force all the contours to be the same color.
        plt.figure()
        CS = plt.contour(X, Y, Z, 6,
                         colors='k', # negative contours will be dashed by default
                         )
        plt.clabel(CS, fontsize=9, inline=1)
        plt.title('Single color - negative contours dashed')
        
        
        # You can set negative contours to be solid instead of dashed:
        matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
        plt.figure()
        CS = plt.contour(X, Y, Z, 6,
                         colors='k', # negative contours will be dashed by default
                         )
        plt.clabel(CS, fontsize=9, inline=1)
        plt.title('Single color - negative contours solid')
        
        plt.savefig('/Users/smitamore/cyberweb/cyberweb/public/images/contour2.png')
        
        # And you can manually specify the colors of the contour
        plt.figure()
        CS = plt.contour(X, Y, Z, 6,
                         linewidths=np.arange(.5, 4, .5),
                         colors=('r', 'green', 'blue', (1,1,0), '#afeeee', '0.5')
                         )
        plt.clabel(CS, fontsize=9, inline=1)
        plt.title('Crazy lines')
        
        plt.savefig('/Users/smitamore/cyberweb/cyberweb/public/images/contour3.png')
        
        # Or you can use a colormap to specify the colors; the default
        # colormap will be used for the contour lines
        plt.figure()
        im = plt.imshow(Z, interpolation='bilinear', origin='lower',
                        cmap=cm.gray, extent=(-3,3,-2,2))
        levels = np.arange(-1.2, 1.6, 0.2)
        CS = plt.contour(Z, levels,
                         origin='lower',
                         linewidths=2,
                         extent=(-3,3,-2,2))
        
        #Thicken the zero contour.
        zc = CS.collections[6]
        plt.setp(zc, linewidth=4)
        
        plt.clabel(CS, levels[1::2],  # label every second level
                   inline=1,
                   fmt='%1.1f',
                   fontsize=14)
        
        # make a colorbar for the contour lines
        CB = plt.colorbar(CS, shrink=0.8, extend='both')
        
        plt.title('Lines with colorbar')
        #plt.hot()  # Now change the colormap for the contour lines and colorbar
        plt.flag()
        
        # We can still add a colorbar for the image, too.
        CBI = plt.colorbar(im, orientation='horizontal', shrink=0.8)
        
        # This makes the original colorbar look a bit out of place,
        # so let's improve its position.
        
        l,b,w,h = plt.gca().get_position().bounds
        ll,bb,ww,hh = CB.ax.get_position().bounds
        CB.ax.set_position([ll, b+0.1*h, ww, h*0.8])
        
        
        #plt.show()
        plt.savefig('/Users/smitamore/cyberweb/cyberweb/public/images/contour4.png')

        # Messages
        num_messages = 10
        messages = meta.Session.query(Message).filter(sa.or_(Message.recipient_group_id.in_(session['user_groups']),\
                                                             Message.recipient_user_id == session['user_id'],\
                                                             sa.and_(Message.recipient_group_id == sa.null(), Message.recipient_user_id == sa.null())))\
                                                             .order_by().limit(num_messages)
        c.messageheaders = ['Date','Message']
        c.messages = [ {'Date':i.date.strftime("%B %d,%Y"), 'Message':i.message} for i in messages ]


        # User Info
        user = meta.Session.query(User).filter(User.id == session.get('user_id')).one()
        c.info = dict()
        c.info['Last login'] = user.last_login_date
        c.info['from'] = user.last_login_ip
        c.myproxy_cmd=""
        meta.Session.close()
       
        return render('/graphs/graph1.mako')





    def graph2(self):
        user_id = session.get('user_id')
        if not user_id:
            raise Exception

        
        plt.subplot(221, projection="aitoff")
        plt.title("Aitoff")
        plt.grid(True)
        
        plt.subplot(222, projection="hammer")
        plt.title("Hammer")
        plt.grid(True)
        
        plt.subplot(223, projection="lambert")
        plt.title("Lambert")
        plt.grid(True)
        
        plt.subplot(224, projection="mollweide")
        plt.title("Mollweide")
        plt.grid(True)
        
        plt.savefig('/Users/smitamore/cyberweb/cyberweb/public/images/geodemo.png')



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
       
        return render('/graphs/graph2.mako')





    def graph3(self):
        user_id = session.get('user_id')
        if not user_id:
            raise Exception

        
        N = 5
        menMeans = (20, 35, 30, 35, 27)
        menStd =   (2, 3, 4, 1, 2)
        
        ind = np.arange(N)  # the x locations for the groups
        width = 0.35       # the width of the bars
        
        
        plt.subplot(111)
        rects1 = plt.bar(ind, menMeans, width,
                            color='r',
                            yerr=menStd,
                            error_kw=dict(elinewidth=6, ecolor='pink'))
        
        womenMeans = (25, 32, 34, 20, 25)
        womenStd =   (3, 5, 2, 3, 3)
        rects2 = plt.bar(ind+width, womenMeans, width,
                            color='y',
                            yerr=womenStd,
                            error_kw=dict(elinewidth=6, ecolor='yellow'))
        
        # add some
        plt.ylabel('Scores')
        plt.title('Scores by group and gender')
        plt.xticks(ind+width, ('G1', 'G2', 'G3', 'G4', 'G5') )
        
        plt.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        
        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                        ha='center', va='bottom')
        
        autolabel(rects1)
        autolabel(rects2)
        
        plt.savefig('/Users/smitamore/cyberweb/cyberweb/public/images/barchart.png')

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
       
        return render('/graphs/graph3.mako')






    def graph4(self):
        user_id = session.get('user_id')
        if not user_id:
            raise Exception

        # make a square figure and axes
        plt.clf()
        plt.figure(1, figsize=(6,6))
        plt.ax = axes([0.1, 0.1, 0.8, 0.8])
        
        labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        fracs = [15,30,45, 10]
        
        explode=(0, 0.05, 0, 0)
        plt.pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
        plt.title('Raining Hogs and Dogs', bbox={'facecolor':'0.8', 'pad':5})
        
        plt.savefig('/Users/smitamore/cyberweb/cyberweb/public/images/pie_demo.png')



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
       
        return render('/graphs/graph4.mako')
