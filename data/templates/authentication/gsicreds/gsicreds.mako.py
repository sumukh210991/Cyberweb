# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1465693106.681428
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/gsicreds/gsicreds.mako'
_template_uri = '/authentication/gsicreds/gsicreds.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headtags', 'col2main']


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
    return runtime._inherit_from(context, u'./gsicreds.layout.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n\n\n')
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
        c = context.get('c', UNDEFINED)
        app_globals = context.get('app_globals', UNDEFINED)
        request = context.get('request', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n<h2>GSI Credential Management for CyberWeb User: ')
        __M_writer(escape(c.user))
        __M_writer(u'</h2>\n<p>\n<p> c.gsidir: ')
        __M_writer(escape(c.gsidir))
        __M_writer(u'\n<p> c.status: ')
        __M_writer(escape(c.status))
        __M_writer(u'\n<table>\n   <tr>\n      <td>account</td><td>DN</td><td>MyProxy Server</td><td>Credential Info</td>\n   </tr>\n   <tr>\n      <td>account</td><td>DN</td><td>MyProxy Server</td><td>Credential Info</td>\n   </tr>\n   <tr>\n      <td>account</td><td>DN</td><td>MyProxy Server</td><td>Credential Info</td>\n   </tr>\n   <tr>\n      <td>account</td><td>DN</td><td>MyProxy Server</td><td>Credential Info</td>\n   </tr>\n</table>\n<p>\n<p> Note: several of the functions on left menu might be put into one page for  credential management\n(add/del/modify).\n\n<hr>\n')

        session = request.environ['beaker.session']
        g = app_globals
        
        
        __M_writer(u'\n')
        for k,v,admin in g.menu.find_menu('gsicreds','index',1):
            __M_writer(u'    <li class=current>IDX1  V: "')
            __M_writer(escape(v))
            __M_writer(u', K=')
            __M_writer(escape(k))
            __M_writer(u'</li>\n')
        __M_writer(u'<hr>\n')
        for k,v,admin in g.menu.find_menu('gsicreds','index',2):
            __M_writer(u'    <li class=current>IDX2  V: "')
            __M_writer(escape(v))
            __M_writer(u', K=')
            __M_writer(escape(k))
            __M_writer(u'</li>\n')
        __M_writer(u'<hr>\n')
        for k,v,admin in g.menu.find_menu('gsicreds','index',3):
            __M_writer(u'    <li class=current>IDX3  V: "')
            __M_writer(escape(v))
            __M_writer(u', K=')
            __M_writer(escape(k))
            __M_writer(u'</li>\n')
        __M_writer(u'<hr>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 4, "35": 49, "41": 3, "45": 3, "51": 7, "58": 7, "59": 9, "60": 9, "61": 11, "62": 11, "63": 12, "64": 12, "65": 32, "70": 35, "71": 36, "72": 37, "73": 37, "74": 37, "75": 37, "76": 37, "77": 39, "78": 40, "79": 41, "80": 41, "81": 41, "82": 41, "83": 41, "84": 43, "85": 44, "86": 45, "87": 45, "88": 45, "89": 45, "90": 45, "91": 47, "97": 91}, "uri": "/authentication/gsicreds/gsicreds.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/gsicreds/gsicreds.mako"}
__M_END_METADATA
"""
