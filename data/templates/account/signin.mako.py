# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467226821.321253
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/signin.mako'
_template_uri = '/account/signin.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['header', 'footer', 'col2right', 'col2main', 'headtags']


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
    return runtime._inherit_from(context, u'/account/account.layout.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
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


def render_footer(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col2right(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n<h3> </h3>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col2main(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        config = context.get('config', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<blockquote>\n<h3> Sign into ')
        __M_writer(escape(config.get('project.fullname','CyberWeb')))
        __M_writer(u'</h3> <p>\n<form action="/signin" method="post">\n<blockquote>\n   <table width=200>\n')
        if c.message:
            __M_writer(u'     <tr>\n         <font color=red>')
            __M_writer(escape(c.message))
            __M_writer(u'</font>\n         <p>\n     </tr>\n')
        __M_writer(u'     <tr>\n       <td align=right>\n           Username: &nbsp;&nbsp;\n       </td>\n       <td align=right>\n         <input type="text" name="username" value="')
        __M_writer(escape(c.username))
        __M_writer(u'">\n       </td>\n     </tr>\n     <tr>\n       <td align=right>\n         Password: &nbsp;&nbsp;\n       </td>\n       <td align=right>\n         <input type="password" name="password">\n       </td>\n     </tr>\n     <tr>\n       <td align=center colspan=2>\n       <input type="submit" value="Signin" name="authform" />\n       </td>\n     </tr>\n   </table>\n   <blockquote>\n      <b><a href="/signup">Request New Account.</a></b>\n      <br><b>Forgot your password?</b>  [request password here]\n      <br><b>Having problems?</b>  [contact us here]\n   </blockquote>\n</blockquote>\n</form>\n\n\t\n</blockquote>\n\n')
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


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 4, "35": 7, "36": 10, "37": 57, "38": 61, "44": 3, "48": 3, "54": 9, "58": 9, "64": 59, "68": 59, "74": 12, "80": 12, "81": 14, "82": 14, "83": 18, "84": 19, "85": 20, "86": 20, "87": 24, "88": 29, "89": 29, "95": 6, "99": 6, "105": 99}, "uri": "/account/signin.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/signin.mako"}
__M_END_METADATA
"""
