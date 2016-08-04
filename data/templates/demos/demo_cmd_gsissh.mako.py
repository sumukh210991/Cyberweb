# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1468532389.722097
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/demos/demo_cmd_gsissh.mako'
_template_uri = '/demos/demo_cmd_gsissh.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['col2main']


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
    return runtime._inherit_from(context, u'/exec/exec.layout.2col.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col2main(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<h3> Cyberweb Execution Services: Testing  Unix commands with GSISSH authentication.</h3>\n<br>\n<form action="" method="post">\n<table border=0>\n    <tr>\n      <td><b>Select Test Script</b></td>\n      <td><b>Select Host:</b></td>\n    </tr>\n    <tr valign=top>\n      <td width=200 valign=top>\n')
        for i in c.command_options:
            __M_writer(u'           ')
            checked = "checked" if i[0] == c.command else "" 
            
            __M_writer(u'\n          <input type="radio" name="command" value="')
            __M_writer(escape(i[0]))
            __M_writer(u'" ')
            __M_writer(escape(checked))
            __M_writer(u'>&nbsp;&nbsp;&nbsp;')
            __M_writer(escape(i[1]))
            __M_writer(u'<br>\n')
        __M_writer(u'      </td>\n      <td>\n')
        for i in c.resources:
            __M_writer(u'           ')
            checked = "checked" if i == c.hostname else "" 
            
            __M_writer(u'\n          <input type="radio" name="hostname" value="')
            __M_writer(escape(i))
            __M_writer(u'" ')
            __M_writer(escape(checked))
            __M_writer(u'>&nbsp;&nbsp;&nbsp;')
            __M_writer(escape(i))
            __M_writer(u'<br>\n')
        __M_writer(u'      </td>\n    </tr>\n    <tr>\n    <td colspan=2 align=left><input type="submit" value="Run Remote Command" /></td>\n    </tr>\n</table>\n</form>\n\n')
        if c.state:
            __M_writer(u'  <table>\n  <tr><td colspan=2><h3>Output:</h3></td></tr>\n  <tr><td align=left><h4>Hostname:  </h4></td> <td> ')
            __M_writer(escape(c.hostname))
            __M_writer(u'</td></tr>\n  <tr><td align=left><h4>Command:  </h4></td> <td> ')
            __M_writer(escape(c.command))
            __M_writer(u'</td></tr>\n  <tr><td align=left valign=top><h4>Results: </h4></td> \n  <td>\n')
            for i in c.results :
                __M_writer(u'    <br>')
                __M_writer(escape(i))
                __M_writer(u'\n')
            __M_writer(u'  </td> </tr>\n  </table>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 45, "40": 3, "45": 3, "46": 14, "47": 15, "48": 15, "50": 15, "51": 16, "52": 16, "53": 16, "54": 16, "55": 16, "56": 16, "57": 18, "58": 20, "59": 21, "60": 21, "62": 21, "63": 22, "64": 22, "65": 22, "66": 22, "67": 22, "68": 22, "69": 24, "70": 32, "71": 33, "72": 35, "73": 35, "74": 36, "75": 36, "76": 39, "77": 40, "78": 40, "79": 40, "80": 42, "86": 80}, "uri": "/demos/demo_cmd_gsissh.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/demos/demo_cmd_gsissh.mako"}
__M_END_METADATA
"""
