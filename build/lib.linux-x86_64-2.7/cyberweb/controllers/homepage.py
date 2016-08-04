import logging
import os

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from authkit.authorize.pylons_adaptors import authorize,authorized
import sqlalchemy as sa

from cyberweb.lib.base import BaseController, render
from cyberweb.lib import auth
from cyberweb.model import meta, Message, Resource, ServiceName

log = logging.getLogger(__name__)

class HomepageController(BaseController):

    #@authorize(auth.is_valid_user)
    def __before__(self):
        pass
    
    def index(self):
        basedir = 'cyberweb/public'
        gallerydir = 'gcem-gallery'

        # Gather the messages to be displayed
        num_messages = 5
        c.messages = []


#        # select user/group specific  and generic messages
        if session.has_key('user_id') and session.has_key('user_groups'):
            messages = meta.Session.query(Message).filter(sa.or_(Message.recipient_group_id.in_(session['user_groups']), Message.recipient_user_id == session['user_id'], \
                                                                 sa.and_(Message.recipient_group_id == sa.null(), Message.recipient_user_id == sa.null()))).limit(num_messages)
#        # select generic messages (user not logged in)
        else:
            messages = meta.Session.query(Message).filter(sa.and_(Message.recipient_group_id == sa.null(), Message.recipient_user_id == sa.null())).limit(num_messages)

        c.messages =  [ ({'date':i.date.strftime("%b %d,%y %H:%M %p"), 'message':i.message}) for i in messages ]
        c.resources = meta.Session.query(Resource).filter(Resource.active == 1).distinct()
        c.service_names = meta.Session.query(ServiceName).distinct()

        # Gather images for the slideshow on the homepage
        # Pickup captions from a text file and match it to the filename
        c.images = []
        c.captions = dict()
        key = '/' + gallerydir + '/'
        try:
            fh = open(basedir + '/' + gallerydir + '.captions')
            for line in fh:
                arr = line.split('|')
                c.captions[key + arr[0]] = '|'.join(arr[1:]).strip()
            fh.close()
        except:
            log.error('Failed reading opening captions')
        for i in os.listdir(basedir + '/' + gallerydir):
            if i[0] != '.':
                c.images.append(key + i)
            if not c.captions.has_key(key + i):
                c.captions[key + i] = 'No caption'

        meta.Session.close()
        return render('/gallery.mako')

    def aboutpage(self):
        return render('/about.mako')

    def contact(self):
        cstr = ['name','cwuser','email','comments']
        c.info = {}
        errflag = False
        c.errmessag = ''
        c.istr = ''
        
        for i in cstr:
            c.info[i] = ''

        c.info['cwuser'] = session.get('user') or 'Guest'
        c.state = request.params.get('state') or 'start'

        if  c.state == 'process':
            # get parameters
            for i in cstr:
                c.info[i] = request.params.get(i) or ''
                if not request.params.has_key(i):
                    errstr = 'Contact Form Problem: ' + i
                    c.errmessage =  c.errmessage + errstr
                    log.debug(errstr)
                    return render('/contact.mako')
            
            c.state = 'finish'
            cwusersdir  = config.get('cw.user_dir','.')
            ff = cwusersdir + '/contactFormData.txt'
            f= open( ff, 'a')
            f.write(str(c.info) + 'end.\n')
            f.close()
            log.info('CONTACT INPUT: FILE: %s, CONTENT: %s' % (ff, str(c.info)))
        elif c.state == 'finish':
            for i in cstr:
                c.info[i] = request.params.get(i) or ''
                c.istr = i + '=' + c.info[i] + '|'
                c.state = ''
            log.info('Contact Input: %s ' % c.istr )
        else:
            pass
            # start state

        return render('/contact.mako')

    def news(self):
        # Gather the messages to be displayed
        num_messages = 50
        c.messages = []

        # select user messages AND generic messages
        if session.has_key('user_id') and session.has_key('user_groups'):
            messages = meta.Session.query(Message).filter(sa.or_(Message.recipient_group_id.in_(session['user_groups']), Message.recipient_user_id == session['user_id'], sa.and_(Message.recipient_group_id == sa.null(), Message.recipient_user_id == sa.null()))).limit(num_messages)
        # select generic messages (user not logged in)
        else:
            messages = meta.Session.query(Message).filter(sa.and_(Message.recipient_group_id == sa.null(), Message.recipient_user_id == sa.null())).limit(num_messages)
        for i in messages:
            c.messages.append({'date':i.date.strftime("%b %d,%y %H:%M %p"), 'message':i.message})

        meta.Session.close()
        return render('/account/news.mako')    
