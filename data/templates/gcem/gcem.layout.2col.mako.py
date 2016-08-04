# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467227211.694233
_enable_loop = True
_template_filename = u'/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/gcem/gcem.layout.2col.mako'
_template_uri = u'/gcem/gcem.layout.2col.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headtags', 'col2main', 'header', 'col2left', 'footer']


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
        __M_writer(u'\n\n\n<p>\n\n')
        __M_writer(escape(next.body()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headtags(context):
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


def render_header(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
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
{"source_encoding": "utf-8", "line_map": {"28": 0, "34": 1, "35": 4, "36": 7, "37": 10, "38": 13, "39": 17, "40": 39, "41": 44, "42": 44, "48": 3, "52": 3, "58": 15, "63": 15, "64": 16, "65": 16, "71": 9, "75": 9, "81": 19, "88": 19, "89": 20, "96": 25, "97": 29, "98": 30, "99": 31, "100": 31, "101": 31, "102": 31, "103": 31, "104": 32, "105": 33, "106": 33, "107": 33, "108": 33, "109": 33, "110": 36, "116": 12, "120": 12, "126": 120}, "uri": "/gcem/gcem.layout.2col.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/gcem/gcem.layout.2col.mako"}
__M_END_METADATA
"""
