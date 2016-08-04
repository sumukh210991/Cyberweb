# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467226954.66912
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/pkiproxy/pkiproxy.mako'
_template_uri = '/authentication/pkiproxy/pkiproxy.mako'
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
        sorted = context.get('sorted', UNDEFINED)
        c = context.get('c', UNDEFINED)
        app_globals = context.get('app_globals', UNDEFINED)
        request = context.get('request', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n  <style type="text/css">\n    .pki_table, .pki_table tr, .pki_table td {\n        border: 1;\n        table-layout: fixed;\n    }\n\n    .pki_table td {\n        vertical-align:top;\n    }\n   .pki_tdh {\n        font-weight:bold;\n        vertical-align:top;\n    }\n\n    ul.s {list-style-type:square;list-style-position:inside; margin-left:10px;}\n\n</style>\n\n<h2>PKI Credential Management for CyberWeb User: ')
        __M_writer(escape(c.user))
        __M_writer(u'</h2>\n<p>\n<blockquote>\nCyberWeb uses passwordless authentication when performing tasks for CyberWeb Users on resources where they have permission/accounts. The system will create a public/private key pair associated with your CyberWeb account, and then install the public key into the authorized_keys files located on the remote resource under you account. In order for this to occur, you must have an active account, with a valid userID and password.\n</blockquote>\n<p>\n<h3>PKI Enabled Resources for CyberWeb User: ')
        __M_writer(escape(c.user))
        __M_writer(u' </h3>\n<table class=pki_table>\n   <tr> <td class=pki_tdh>HOSTNAME</td>\n        <td class=pki_tdh>KEY#</td> \n        <td class=pki_tdh>ACCOUNT</td> \n        <td class=pki_tdh>PUBKEY</td> \n   </tr>\n')
        for key in sorted(c.res_pki.iterkeys()):  ## for k in c.res_allata
            __M_writer(u'       <tr><td> ')
            __M_writer(escape(c.res_pki[key][0]))
            __M_writer(u' </td>\n           <td style="text-align:center;"> ')
            __M_writer(escape(c.res_pki[key][3]))
            __M_writer(u' </td>\n           <td> ')
            __M_writer(escape(c.res_pki[key][1]))
            __M_writer(u' </td>\n           <td style="overflow:hidden; vertical-align:top; width:700px;WORD-BREAK:BREAK-ALL">\n                ')
            __M_writer(escape(c.res_pki[key][4]))
            __M_writer(u' \n           </td>\n       </tr>\n')
        __M_writer(u'</table>\n<h3> NON PKI resources (c.res_nonpki)</h3>\n<table class=pki_table>\n')
        for key,v in c.res_nonpki.items():
            __M_writer(u'       <tr><td>')
            __M_writer(escape(key))
            __M_writer(u'</td><td> ')
            __M_writer(escape(v[0]))
            __M_writer(u' </td><td> ')
            __M_writer(escape(v[1]))
            __M_writer(u'  || ')
            __M_writer(escape(v[2]))
            __M_writer(u'   </td></tr>\n')
        __M_writer(u'</table>\n\n\n')
        if c.debug:
            __M_writer(u'   <h3> ALL resources (c.res_all) </h3>\n   <table>\n')
            for key,v in c.res_all.items():
                __M_writer(u'          <tr><td>')
                __M_writer(escape(key))
                __M_writer(u'</td><td> ')
                __M_writer(escape(v[0]))
                __M_writer(u' </td><td> ')
                __M_writer(escape(v[1]))
                __M_writer(u' </td></tr>\n')
            __M_writer(u'   </table>\n\n   <p>\n   <blockquote>\n   <br> c.err: ')
            __M_writer(escape(c.err))
            __M_writer(u'\n   <br> c.ssherr: ')
            __M_writer(escape(c.ssherr))
            __M_writer(u'\n   <br> c.cmd== ')
            __M_writer(escape(c.cmd))
            __M_writer(u'\n   ')

            session = request.environ['beaker.session']
            g = app_globals
               
            
            __M_writer(u'\n   <p> status: ')
            __M_writer(escape(c.status))
            __M_writer(u'\n')
            for k,v,admin in g.menu.find_menu('pkiproxy','index',1):
                __M_writer(u'       <li class=current>IDX1  V: "')
                __M_writer(escape(v))
                __M_writer(u', K=')
                __M_writer(escape(k))
                __M_writer(u'</li>\n')
            __M_writer(u'   <hr>\n')
            for k,v,admin in g.menu.find_menu('pkiproxy','index',2):
                __M_writer(u'       <li class=current>IDX2  V: "')
                __M_writer(escape(v))
                __M_writer(u', K=')
                __M_writer(escape(k))
                __M_writer(u'</li>\n')
            __M_writer(u'   <hr>\n')
            for k,v,admin in g.menu.find_menu('pkiproxy','index',3):
                __M_writer(u'       <li class=current>IDX3  V: "')
                __M_writer(escape(v))
                __M_writer(u', K=')
                __M_writer(escape(k))
                __M_writer(u'</li>\n')
            __M_writer(u'   <hr>\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"128": 85, "129": 85, "130": 85, "131": 87, "132": 89, "138": 132, "28": 0, "33": 1, "34": 4, "35": 90, "41": 3, "45": 3, "51": 7, "59": 7, "60": 27, "61": 27, "62": 33, "63": 33, "64": 40, "65": 41, "66": 41, "67": 41, "68": 42, "69": 42, "70": 43, "71": 43, "72": 45, "73": 45, "74": 49, "75": 52, "76": 53, "77": 53, "78": 53, "79": 53, "80": 53, "81": 53, "82": 53, "83": 53, "84": 53, "85": 55, "86": 58, "87": 59, "88": 61, "89": 62, "90": 62, "91": 62, "92": 62, "93": 62, "94": 62, "95": 62, "96": 64, "97": 68, "98": 68, "99": 69, "100": 69, "101": 70, "102": 70, "103": 71, "108": 74, "109": 75, "110": 75, "111": 76, "112": 77, "113": 77, "114": 77, "115": 77, "116": 77, "117": 79, "118": 80, "119": 81, "120": 81, "121": 81, "122": 81, "123": 81, "124": 83, "125": 84, "126": 85, "127": 85}, "uri": "/authentication/pkiproxy/pkiproxy.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/pkiproxy/pkiproxy.mako"}
__M_END_METADATA
"""
