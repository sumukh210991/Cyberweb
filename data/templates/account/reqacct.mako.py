# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467931842.90977
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/reqacct.mako'
_template_uri = '/account/reqacct.mako'
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
    return runtime._inherit_from(context, u'/account/account.layout.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
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
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        if c.status == 1:
            __M_writer(u'  <meta http-equiv="REFRESH" content="10;url=/signin">\n  <font color=green>')
            __M_writer(escape(h.html.literal(c.statusinfo)))
            __M_writer(u'</font><br>\n  <br>\n  <br>\n  Please login to use your account. You will be redirected to the signin page in 10 seconds.\n  You can also click <a href="/signin">here</a>.\n')
        else:
            __M_writer(u'  <h3>CyberWeb Account Request Form: </h3>\n  <br><font color=red>')
            __M_writer(escape(h.html.literal(c.statusinfo)))
            __M_writer(u'</font>\n  <p>\n  <form action="" method="post">\n  <table border=1>\n  <tr>\n     <td>Username:&nbsp;&nbsp;</td>\n     <td><input type="text" name="cw_username" value=')
            __M_writer(escape(c.username))
            __M_writer(u'> </td>\n  </tr>\n  <tr>\n     <td>Passphrase:</td>\n     <td><input type="password" name="password" value=')
            __M_writer(escape(c.password))
            __M_writer(u'></td>\n  </tr>\n  <tr>\n     <td>Verify Passphrase:</td>\n     <td><input type="password" name="password_verify" value=')
            __M_writer(escape(c.password_verify))
            __M_writer(u'></td>\n  </tr>\n  <tr>\n     <td>Firstname:</td>\n     <td><input type="text" name="firstname" value=')
            __M_writer(escape(c.firstname))
            __M_writer(u' ></td>\n  </tr>\n  <tr>\n     <td>Lastname:</td>\n     <td><input type="text" name="lastname" value=')
            __M_writer(escape(c.lastname))
            __M_writer(u'></td>\n  </tr>\n  <tr>\n     <td>Email:</td>\n     <td><input type="text" name="email" value=')
            __M_writer(escape(c.email))
            __M_writer(u'></td>\n  </tr>\n  <tr>\n     <td>Institution:</td>\n     <td><input type="text" name="institution" value=')
            __M_writer(escape(c.institution))
            __M_writer(u'></td>\n  </tr>\n  <tr>\n     <td>Reason:</td>\n     <td><input type="text" name="reason" value=')
            __M_writer(escape(c.reason))
            __M_writer(u'></td>\n  </tr>\n  </table>\n\n  <br>\n  <input type="submit" name="reqacct_form">\n  </form>\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 4, "35": 60, "41": 3, "45": 3, "51": 6, "57": 6, "58": 8, "59": 9, "60": 10, "61": 10, "62": 15, "63": 16, "64": 17, "65": 17, "66": 23, "67": 23, "68": 27, "69": 27, "70": 31, "71": 31, "72": 35, "73": 35, "74": 39, "75": 39, "76": 43, "77": 43, "78": 47, "79": 47, "80": 51, "81": 51, "82": 59, "88": 82}, "uri": "/account/reqacct.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/reqacct.mako"}
__M_END_METADATA
"""
