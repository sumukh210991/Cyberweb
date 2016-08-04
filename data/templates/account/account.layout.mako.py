# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467226821.329765
_enable_loop = True
_template_filename = u'/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/account.layout.mako'
_template_uri = u'/account/account.layout.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headtags', 'col2left', 'header', 'col2main', 'footer']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/2col-left.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        next = context.get('next', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n<p>\n\n')
        __M_writer(escape(next.body()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headtags(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        next = context.get('next', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\t<link rel="stylesheet" type="text/css" href="/css/ui-lightness/jquery-ui-1.8.17.custom.css" media="screen">\n\t<link rel="stylesheet" type="text/css" href="/css/showLoading.css" media="screen" />\n\t<link rel="stylesheet" type="text/css" href="/css/admin.css" media="screen">\n\t\n\t<script type="text/javascript" src="/js/jquery-1.6.2.js"></script>\n\t<script type="text/javascript" src="/js/jquery-ui-1.8.17.custom.min.js"></script>\n\t<script type="text/javascript" src="/js/jquery.showLoading.min.js"></script>\n\t<script type="text/javascript" src="/js/jquery.dateFormat-1.0.js"></script>\n\t<script type="text/javascript" src="/js/ajax_post_lib.js"></script>\n\t<script type="text/javascript" src="/js/newAdmin.js"></script>\n\t\n\t<style>\n\t\t.col2-left {\n\t\t\tfloat: left;\n\t\t\tmargin-top:3em;\n\t\t\twidth: 150px;\n\t\t\tmax-width: 200px;\n\t\t\toverflow-x: auto;\n\t\t}\n\t\t\n\t\t.col2-main {\n\t\t\tmargin:1em;\n\t\t\tmax-width:80%;\n  \t\t\tmin-width:200px;\n\t\t}\n\t\t\n\t\t#leftmenuList li {\n\t\t\tfont-family: Verdana, Arial, Helvetica, sans-serif;\n\t\t\tfont-size: 11px;\n\t\t\tline-height: 2em;\n\t\t\tlist-style: disc outside none;\n\t\t\tdisplay: list-item;\n\t\t\tmargin-left: 20px;\n\t\t}\n\t</style>\n\t\n\t')
        __M_writer(escape(next.headtags()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col2left(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        app_globals = context.get('app_globals', UNDEFINED)
        request = context.get('request', UNDEFINED)
        tmpl_context = context.get('tmpl_context', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')

        session = request.environ['beaker.session']
        g = app_globals
        c = tmpl_context
        this_route = request.environ['pylons.routes_dict']
        
        
        __M_writer(u'\n<!--#Implement sub_menu as a Left Menu Navigation Panel -->\n    <div id="leftmenu">\n\t\t<ul id="leftmenuList">\n')
        for k,v,admin in g.menu.find_menu(this_route['controller'],this_route['action'],2):
            if k == g.menu.find_title(this_route['controller'],this_route['action'],2):
                __M_writer(u'                 <li class=current><a href="')
                __M_writer(escape(v))
                __M_writer(u'">')
                __M_writer(escape(k))
                __M_writer(u'</a></li>\n')
            else:
                __M_writer(u'                 <li><a href="')
                __M_writer(escape(v))
                __M_writer(u'">')
                __M_writer(escape(k))
                __M_writer(u'</a></li>\n')
        __M_writer(u'        </ul>\n\t</div>\n<!--#End Left Menu Navigation Panel -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_header(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col2main(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(escape(self.col2main()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footer(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"129": 123, "28": 0, "34": 1, "35": 41, "36": 44, "37": 47, "38": 50, "39": 72, "40": 76, "41": 80, "42": 80, "48": 3, "53": 3, "54": 40, "55": 40, "61": 52, "68": 52, "69": 53, "76": 58, "77": 62, "78": 63, "79": 64, "80": 64, "81": 64, "82": 64, "83": 64, "84": 65, "85": 66, "86": 66, "87": 66, "88": 66, "89": 66, "90": 69, "96": 46, "100": 46, "106": 74, "111": 74, "112": 75, "113": 75, "119": 49, "123": 49}, "uri": "/account/account.layout.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/account.layout.mako"}
__M_END_METADATA
"""
