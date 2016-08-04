# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467227107.310403
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/demos/demo_cmd_ssh.mako'
_template_uri = '/demos/demo_cmd_ssh.mako'
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
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<h3> Cyberweb Execution Services: \n<br>Testing simple Unix commands with passwordless SSH authentication.</h3>\n<br>CyberWeb User: ')
        __M_writer(escape(c.cwuser))
        __M_writer(u'\n<br>CyberWeb Group:\n<br> \n<form action="" method="post">\n<table border=0>\n    <tr>\n      <td><b>Select Test Script</b></td>\n      <td><b>Select Host:</b></td>\n    </tr>\n    <tr valign=top>\n      <td width=200 valign=top>\n       ')
        cnt=0 
        
        __M_writer(u'\n')
        for i in c.command_options:
            __M_writer(u'          ')
            checked = "checked" if cnt == 0 else "" 
            
            __M_writer(u'\n          <input type="radio" name="command" value="')
            __M_writer(escape(i[0]))
            __M_writer(u'" ')
            __M_writer(escape(checked))
            __M_writer(u'>&nbsp;&nbsp;&nbsp;')
            __M_writer(escape(i[1]))
            __M_writer(u'<br>\n          ')
            cnt=cnt+1 
            
            __M_writer(u'\n')
        __M_writer(u'      </td>\n      <td>\n          ')
        cnt=0 
        
        __M_writer(u'\n')
        if  len(c.resources.items()) == 0:
            __M_writer(u'              You currently have SSH connected resources.<br>\n              To add compute resource accounts, see MyCyberWeb-->Authentication.\n')
        else:
            for r_id, r in c.resources.items():
                __M_writer(u'                   ')
                checked = "checked" if cnt == 0 else "" 
                
                __M_writer(u"\n                   <input type='radio' name='hostname' value='")
                __M_writer(escape(r_id))
                __M_writer(u"' ")
                __M_writer(escape(checked))
                __M_writer(u'>&nbsp;&nbsp;&nbsp;')
                __M_writer(escape(r['hostname']))
                __M_writer(u'<br>\n             ')
                cnt=cnt+1 
                
                __M_writer(u'\n')
        __M_writer(u'      </td>\n    </tr>\n    <tr>\n    <td colspan=2 align=left><input type="submit" value="Run Remote Command" /></td>\n    </tr>\n</table>\n</form>\n\n')
        if c.state:
            __M_writer(u'  <table>\n  <tr><td colspan=2><h3>Output:</h3></td></tr>\n  <tr><td align=left><h4>Host:  </h4></td> <td> ')
            __M_writer(escape(c.hostname))
            __M_writer(u'</td></tr>\n  <tr><td align=left><h4>Host_name:  </h4></td> <td> ')
            __M_writer(escape(c.hostname_name))
            __M_writer(u'</td></tr>\n  <tr><td align=left><h4>Command:  </h4></td> <td> ')
            __M_writer(escape(c.command))
            __M_writer(u'</td></tr>\n  <tr><td align=left valign=top><h4>Results: </h4></td> \n  <td>\n')
            for res in c.results:
                __M_writer(u'     ')
                __M_writer(escape(res))
                __M_writer(u' <br>\n')
            __M_writer(u'  </td> </tr>\n  </table>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 58, "40": 3, "46": 3, "47": 6, "48": 6, "49": 17, "51": 17, "52": 18, "53": 19, "54": 19, "56": 19, "57": 20, "58": 20, "59": 20, "60": 20, "61": 20, "62": 20, "63": 21, "65": 21, "66": 23, "67": 25, "69": 25, "70": 26, "71": 27, "72": 29, "73": 30, "74": 31, "75": 31, "77": 31, "78": 32, "79": 32, "80": 32, "81": 32, "82": 32, "83": 32, "84": 33, "86": 33, "87": 36, "88": 44, "89": 45, "90": 47, "91": 47, "92": 48, "93": 48, "94": 49, "95": 49, "96": 52, "97": 53, "98": 53, "99": 53, "100": 55, "106": 100}, "uri": "/demos/demo_cmd_ssh.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/demos/demo_cmd_ssh.mako"}
__M_END_METADATA
"""
