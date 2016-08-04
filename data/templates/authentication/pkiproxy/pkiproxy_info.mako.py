# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1465693132.695516
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/pkiproxy/pkiproxy_info.mako'
_template_uri = '/authentication/pkiproxy/pkiproxy_info.mako'
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
        __M_writer(u'\n\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headtags(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n\t<style>\n\t\t.errorStyle{\n\t\t\tmargin: 0;\n\t\t\tpadding: 1em;\n\t\t\tcolor: red;\n\t\t\tfont-weight: bold;\n\t\t}\n\t\t\n\t\t.formStyle th, .formStyle td{\n\t\t\tborder: 0;\n\t\t}\n\t\t\n\t\t.label {\n\t\t\ttext-align: right;\n\t\t}\n\t</style>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col2main(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n  <style type="text/css">\n    .prefbutton {\n      margin:0 10px 0 10px;\n      display:inline;\n    }\n    .prefbuttons {\n      width: 190px;\n      margin: 0 auto;\n      text-align: center;\n    }\n    .prefheader {\n      float:left;\n      width: 130px;\n      text-align: right;\n      color: grey;\n      font-weight: bold;\n      margin: 5px 0 5px 0;\n    }\n    .prefvalue {\n      float:left;\n      padding-left:15px;\n      width: 323px;\n      margin: 5px 0 5px 0;\n    }\n    .prefbar {\n      background:#cccccc;\n      padding-left:15px;\n      margin-bottom:7px;\n    }\n\n    .pki_table, .pki_table tr, .pki_table td {\n        border: 1;\n        table-layout: fixed;\n    }\n\t\n    .pki_table td {\n        vertical-align:top;\n    }\n\n    ul.b {list-style-type:square;list-style-position:inside; margin-left:10px;}\n\n  </style>\n\n  <div style="width:700px;">\n\t    <div class="prefbar">PKI Credential Information</div>\n            <table class="pki_table">\n               <tr><td style="width:100px;"> Resources</td>  <td style="vertical-align:top;">Key</td> </tr>\n')
        for k in c.current_keys:
            __M_writer(u'                  <tr>\n                     <td>\n                        <ul class="b"> \n')
            for r in c.pkires:
                __M_writer(u'                             <li> ')
                __M_writer(escape(c.pkires[r]))
                __M_writer(u'</li> \n')
            __M_writer(u'                        </ul> \n                     </td>\n                     <td style="overflow:hidden; vertical-align:top; width:500px;WORD-BREAK:BREAK-ALL">\n                         ')
            __M_writer(escape(k.public_key))
            __M_writer(u'\n                     </td>\n                  </tr>\n')
        __M_writer(u'            </table>\n\n\n\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"64": 80, "33": 1, "34": 20, "35": 89, "66": 84, "65": 80, "72": 66, "41": 3, "45": 3, "60": 75, "51": 22, "56": 22, "57": 70, "58": 71, "59": 74, "28": 0, "61": 75, "62": 75, "63": 77}, "uri": "/authentication/pkiproxy/pkiproxy_info.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/pkiproxy/pkiproxy_info.mako"}
__M_END_METADATA
"""
