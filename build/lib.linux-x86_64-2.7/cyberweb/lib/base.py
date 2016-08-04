"""The base Controller API

Provides the BaseController class for subclassing.
"""
from datetime import datetime, timedelta

from pylons import app_globals, config, session, tmpl_context
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

from cyberweb.model.meta import Session


class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        tmpl_context.current_navtab = 'blah'
        tmpl_context.current_subnavtab = 'blakj'
        tmpl_context.status = 1
        tmpl_context.messagebar_text = ''
        tmpl_context.message = ''
        tmpl_context.username = ''

        beaker = environ.get('beaker.session') or {}
        try:
            timeout = int(config.get('cw.timeout'))
        except Exception:
            timeout = 0
        if timeout and beaker.get('user_id'):
            last_access = beaker.get('last_accessed') or False
            if last_access and datetime.now() - last_access > timedelta(minutes=timeout):
                try:
                    return "Your session has timed out. You have been logged out for security."
                finally:
                    Session.remove()
            beaker['last_accessed'] = datetime.now()
            beaker.save()

        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()

    def __init__(self):
        tmpl_context.general = ''
        if not session.get('available_resources'):
            session['available_resources'] = app_globals.user_resources(session.get('user_id'))
            session.save()