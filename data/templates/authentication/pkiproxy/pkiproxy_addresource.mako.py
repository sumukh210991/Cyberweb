# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1465693123.428626
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/pkiproxy/pkiproxy_addresource.mako'
_template_uri = '/authentication/pkiproxy/pkiproxy_addresource.mako'
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
    return runtime._inherit_from(context, u'./pkiproxy.layout.mako', _template_uri)
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
        __M_writer(u'\n\n<h2>ADD Resource:  PKI Credential Management for CyberWeb User: ')
        __M_writer(escape(c.user))
        __M_writer(u'</h2>\n<p>\n<p> status: ')
        __M_writer(escape(c.status))
        __M_writer(u'\n<table>\n<h3>PKI Credentials</h3>\n<table>\n   <tr>\n      <td>Account</td><td>Hostname</td>Status</td><td>Date</td>\n   </tr>\n   <tr> <td>account1</td><td>hostname1</td>Status</td><td>date</td> </tr>\n   <tr> <td>account2</td><td>hostname2</td>Status</td><td>date</td> </tr>\n   <tr> <td>account3</td><td>hostname3</td>Status</td><td>date</td> </tr>\n</table>\n\n<hr>\n')

        session = request.environ['beaker.session']
        g = app_globals
        
        
        __M_writer(u'\n')
        for k,v,admin in g.menu.find_menu('pkiproxy','index',1):
            __M_writer(u'    <li class=current>IDX1  V: "')
            __M_writer(escape(v))
            __M_writer(u', K=')
            __M_writer(escape(k))
            __M_writer(u'</li>\n')
        __M_writer(u'<hr>\n')
        for k,v,admin in g.menu.find_menu('pkiproxy','index',2):
            __M_writer(u'    <li class=current>IDX2  V: "')
            __M_writer(escape(v))
            __M_writer(u', K=')
            __M_writer(escape(k))
            __M_writer(u'</li>\n')
        __M_writer(u'<hr>\n')
        for k,v,admin in g.menu.find_menu('pkiproxy','index',3):
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
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 4, "35": 41, "41": 3, "45": 3, "51": 7, "58": 7, "59": 9, "60": 9, "61": 11, "62": 11, "63": 24, "68": 27, "69": 28, "70": 29, "71": 29, "72": 29, "73": 29, "74": 29, "75": 31, "76": 32, "77": 33, "78": 33, "79": 33, "80": 33, "81": 33, "82": 35, "83": 36, "84": 37, "85": 37, "86": 37, "87": 37, "88": 37, "89": 39, "95": 89}, "uri": "/authentication/pkiproxy/pkiproxy_addresource.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/pkiproxy/pkiproxy_addresource.mako"}
__M_END_METADATA
"""
