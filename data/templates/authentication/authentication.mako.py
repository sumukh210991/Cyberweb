# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467226952.515133
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/authentication.mako'
_template_uri = '/authentication/authentication.mako'
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
    return runtime._inherit_from(context, u'/authentication/authentication.layout.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n\n')
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
        __M_writer = context.writer()
        __M_writer(u'\n\n<h2>Authentication Credential Summary for CyberWeb User: ')
        __M_writer(escape(c.user))
        __M_writer(u'</h2>\n<p>\n<h3>PKI Credentials</h3>\n<table>\n   <tr>\n      <td>Account</td><td>Hostname</td>Status</td><td>Date</td>\n   </tr>\n   <tr> <td>account1</td><td>hostname1</td>Status</td><td>date</td> </tr>\n   <tr> <td>account2</td><td>hostname2</td>Status</td><td>date</td> </tr>\n   <tr> <td>account3</td><td>hostname3</td>Status</td><td>date</td> </tr>\n</table>\n<p>\n<h3>GSI Credentials</h3>\n<table>\n   <tr> <td>Account</td><td>DN</td><td>MyProxy Server</td><td>Credential Info</td> </tr>\n   <tr> <td>account1</td><td>DN1</td><td>MyProxy Server</td><td>Credential1 Info</td> </tr>\n   <tr> <td>account2</td><td>DN2</td><td>MyProxy Server</td><td>Credential2 Info</td>\n   <tr> <td>account3</td><td>DN3</td><td>MyProxy Server</td><td>Credential3 Info</td>\n   <tr> <td>account4</td><td>DN4</td><td>MyProxy Server</td><td>Credential4 Info</td>\n   </tr>\n</table>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"64": 58, "33": 1, "34": 5, "35": 31, "41": 4, "45": 4, "51": 8, "56": 8, "57": 10, "58": 10, "28": 0}, "uri": "/authentication/authentication.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/authentication.mako"}
__M_END_METADATA
"""
