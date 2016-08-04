# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1468782365.131706
_enable_loop = True
_template_filename = u'/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/layout.mako'
_template_uri = u'/layout.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        app_globals = context.get('app_globals', UNDEFINED)
        request = context.get('request', UNDEFINED)
        tmpl_context = context.get('tmpl_context', UNDEFINED)
        next = context.get('next', UNDEFINED)
        __M_writer = context.writer()

        from authkit.authorize.pylons_adaptors import authorized
        from cyberweb.lib import auth
        
        session = request.environ['beaker.session']
        g = app_globals
        c = tmpl_context
        this_route = request.environ['pylons.routes_dict']
        
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['c','g','this_route','auth','session','authorized'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml" lang="en">\n\n  <head>\n    <title>')
        __M_writer(escape(g.title))
        __M_writer(u'</title>\n\t<meta name="Copyright" content="Copyright (c) 2009 Advanced Computing Environments Lab, SDSU">\n    <meta name="Author" content="Advanced Computing Environments Lab" >\n    <meta name="Keywords" content="cyberweb, python, pylons, grid computing, computational science, sdsu, ace, webservices">\n\n\t<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/combo?3.0.0/build/cssreset/reset-min.css&3.0.0/build/cssfonts/fonts-min.css&3.0.0/build/cssgrids/grids-min.css&3.0.0/build/cssbase/base-min.css">\n\t<link rel="stylesheet" type="text/css" href="/base.css">\n\n\t<script type="text/javascript" src="/jquery.js"></script>\n\t<script type="text/javascript" src="/js/jquery-1.6.2.js"></script>\n\t<script type="text/javascript" src="/js/jquery.ui.core.js"></script>\n\t<script type="text/javascript" src="/jquery.tablesorter.js"></script>\n\t<script type="text/javascript" src="/jquery.form.js"></script> \n\t\n\t<link rel="shortcut icon" href="/favicon.ico">\n\n\t<script type="text/javascript">\n\t  $(document).ready(function() {\n\t\t//Show dropdown bar\n\t\tsetTimeout("$(\'#messagebar\').fadeOut(\'slow\')",5000);\n\t\tif($("#myTable") && $("#myTable").tablesorter){\n\t\t\t$("#myTable").tablesorter();\n\t\t}\n\t  });\n\t</script>\n\n\t')
        __M_writer(escape(next.headtags()))
        __M_writer(u'\n  </head>\n\n  <body>\n\t<!--#Navigation bar-->\n\t<div id="navbar">\n\t  <ul id="tabs">\n')
        for k,v,admin in g.menu.get_menu():
            if k == 'CyberWeb':
                __M_writer(u'\t\t\t\t<li> <a href="/"> <h1><span class="dark">O</span>cean</h1> </a> </li> \n\t\t\t\t<li> <a href="/"> <h1><span class="dark">S</span>cience</h1> </a> </li>\n\t\t\t\t<li> <a href="/"> <h1><span class="dark">E</span>ducation</h1> </a> </li>\n\t\t\t\t<li> <a href="/"> <h1><span class="dark">P</span>ortal</h1> </a> </li>\n')
            elif admin and not authorized(auth.is_admin):
                __M_writer(u'\t\t\t\t<noop>\n')
            elif k == g.menu.find_title(this_route['controller'],this_route['action'],0):
                __M_writer(u'\t\t\t\t<li class=current><a href="')
                __M_writer(escape(v))
                __M_writer(u'">')
                __M_writer(escape(k))
                __M_writer(u'</a></li>\n')
            else:
                __M_writer(u'\t\t\t\t<li><a href="')
                __M_writer(escape(v))
                __M_writer(u'">')
                __M_writer(escape(k))
                __M_writer(u'</a></li>\n')
        __M_writer(u'\t  </ul>\n\t  <ul id="rightTabs">\n')
        if session.has_key('user'):
            __M_writer(u'                    <li><a href="/user">')
            __M_writer(escape(session['user']))
            __M_writer(u'</a><li>\n                    <li><a href="/signout">Logout</a></p></li>\n')
        else:
            __M_writer(u'                  <li><a href="/signin">Login</a></p></li>\n                  <li><a href="/signup">Signup</a></li>\n')
        __M_writer(u'\t  </ul>\n\t</div>\n\t<!--end navbar-->\n\t<div id="subnav">\n\t  <ul id="subnavTabs">\n')
        for k,v,admin in g.menu.find_menu(this_route['controller'],this_route['action'],1):
            if k == g.menu.find_title(this_route['controller'],this_route['action'],1):
                __M_writer(u'\t\t\t\t<li class=current><a href="')
                __M_writer(escape(v))
                __M_writer(u'">')
                __M_writer(escape(k))
                __M_writer(u'</a></li>\n')
            else:
                __M_writer(u'\t\t\t\t<li><a href="')
                __M_writer(escape(v))
                __M_writer(u'">')
                __M_writer(escape(k))
                __M_writer(u'</a></li>\n')
        __M_writer(u'\t  </ul>\n\t</div>\n\t<!--end subnavbar-->\n\t<!--#End Navigation Bar-->\n\n')
        if c.status == 1:
            __M_writer(u'\t  <div id="messagebar">')
            __M_writer(escape(c.messagebar_text))
            __M_writer(u'</div>\n')
        else:
            __M_writer(u'\t  <div id="messagebar" style="visibility:hidden"></div>\n')
        __M_writer(u'\n\t<!--#Body-->\n        <div id="content">\n\t  ')
        __M_writer(escape(next.body()))
        __M_writer(u'\n\t</div>\n\t<!--#End Body-->\n\n\t<!--#Footer-->\n\t<div id="footer">\n\n \t   <div class="footer-left">\n\t\tPowered by: <h1 style="color: black;">cyber<span class="dark">Web</span></h1>\n\t   </div>\n\t   <div class="footer-right">\n              <p>Brought to you by the faculty and students of the ACE Lab</p>\n              <p>&copy; 2011-2012 San Diego State University ACE Lab</p>\n              <p>Contact:  <a href="mailto:info at acel.sdsu.edu">info at acel.sdsu.edu</a></p>\n\t   </div>\n\t   <div class="footer-center"> </div>\n\n\t</div>\n\t<!--#End Footer-->\n\n  </body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"17": 0, "26": 1, "38": 9, "39": 15, "40": 15, "41": 41, "42": 41, "43": 48, "44": 49, "45": 50, "46": 54, "47": 55, "48": 56, "49": 57, "50": 57, "51": 57, "52": 57, "53": 57, "54": 58, "55": 59, "56": 59, "57": 59, "58": 59, "59": 59, "60": 62, "61": 64, "62": 65, "63": 65, "64": 65, "65": 67, "66": 68, "67": 71, "68": 76, "69": 77, "70": 78, "71": 78, "72": 78, "73": 78, "74": 78, "75": 79, "76": 80, "77": 80, "78": 80, "79": 80, "80": 80, "81": 83, "82": 88, "83": 89, "84": 89, "85": 89, "86": 90, "87": 91, "88": 93, "89": 96, "90": 96, "96": 90}, "uri": "/layout.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/layout.mako"}
__M_END_METADATA
"""
