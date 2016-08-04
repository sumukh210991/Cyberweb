# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467226954.679516
_enable_loop = True
_template_filename = u'/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/pkiproxy/pkiproxy.layout.mako'
_template_uri = u'/authentication/pkiproxy/./pkiproxy.layout.mako'
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
        __M_writer(u'\n\n\n<p>\n\n')
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
        __M_writer(u'\n\t<link rel="stylesheet" type="text/css" href="/css/ui-lightness/jquery-ui-1.8.17.custom.css" media="screen">\n\t<link rel="stylesheet" type="text/css" href="/css/showLoading.css" media="screen" />\n\t\n\t<script type="text/javascript" src="/js/jquery-1.6.2.js"></script>\n\t<script type="text/javascript" src="/js/jquery-ui-1.8.17.custom.min.js"></script>\n\t<script type="text/javascript" src="/js/jquery.showLoading.min.js"></script>\n\t<script type="text/javascript" src="/js/jquery.dateFormat-1.0.js"></script>\n\t\n\t')
        __M_writer(escape(next.headtags()))
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
        for k2,v2,admin in g.menu.find_menu('authentication','index',2):
            if k2 == g.menu.find_title('authentication','index',2):
                __M_writer(u'                 <li class=current><a href="')
                __M_writer(escape(v2))
                __M_writer(u'">')
                __M_writer(escape(k2))
                __M_writer(u'</a></li>\n')
            else:
                __M_writer(u'                 <li><a href="')
                __M_writer(escape(v2))
                __M_writer(u'">')
                __M_writer(escape(k2))
                __M_writer(u'</a></li>\n')
                if  'pkiproxy' in v2 :
                    for k3,v3,admin in g.menu.find_menu('pkiproxy','index',3):
                        if k3 == g.menu.find_title('pkiproxy','index',3):
                            __M_writer(u'                             <li class=current><a href="')
                            __M_writer(escape(v3))
                            __M_writer(u'">Q3')
                            __M_writer(escape(k3))
                            __M_writer(u'</a></li>\n')
                        else:
                            __M_writer(u'                             <li><a href="')
                            __M_writer(escape(v3))
                            __M_writer(u'">&nbsp;&nbsp;')
                            __M_writer(escape(k3))
                            __M_writer(u'</a></li>\n')
            __M_writer(u'            <p>\n')
        __M_writer(u'        </ul>\n   </div>\n<!--#End Left Menu Navigation Panel -->\n')
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
{"source_encoding": "utf-8", "line_map": {"133": 15, "137": 15, "143": 137, "28": 0, "34": 1, "35": 13, "36": 16, "37": 19, "38": 23, "39": 55, "40": 60, "41": 60, "47": 3, "52": 3, "53": 12, "54": 12, "60": 21, "65": 21, "66": 22, "67": 22, "73": 18, "77": 18, "83": 25, "90": 25, "91": 26, "98": 31, "99": 35, "100": 36, "101": 37, "102": 37, "103": 37, "104": 37, "105": 37, "106": 38, "107": 39, "108": 39, "109": 39, "110": 39, "111": 39, "112": 40, "113": 41, "114": 42, "115": 43, "116": 43, "117": 43, "118": 43, "119": 43, "120": 44, "121": 45, "122": 45, "123": 45, "124": 45, "125": 45, "126": 50, "127": 52}, "uri": "/authentication/pkiproxy/./pkiproxy.layout.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/pkiproxy/pkiproxy.layout.mako"}
__M_END_METADATA
"""
