# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467227142.009695
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/demos/demo_basicjob.mako'
_template_uri = '/demos/demo_basicjob.mako'
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
        __M_writer(u'\n<h3> Cyberweb Execution Services: \n<br>Testing Basic Job creation and management (non Jodis).</h3>\n<br>CyberWeb User: ')
        __M_writer(escape(c.cwuser))
        __M_writer(u'\n<br>CyberWeb Group:\n<br> \n<blockquote>\nstep 1: pick a command; pick a machine <br>\nstep 2: create the job <br>\nstep 3: start the job <br>\nstep 4: del the job <br>\nstep 5: view the job output <br>\n\n<form action="" method="post">\n<table border=0>\n    <tr>\n      <td><b>Select Test Script</b></td>\n      <td><b>Select Host:</b></td>\n    </tr>\n    <tr valign=top>\n      <td width=200 valign=top>\n')
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
        __M_writer(u'      </td>\n    </tr>\n    <tr>\n    <td colspan=2 align=left>\n\t<input type="radio" name="job" value="add">&nbsp;&nbsp;&nbsp;Add a new job\n        <input type="radio" name="job" value="add">&nbsp;&nbsp;&nbsp;Run Remote Command\n    </td>\n    </tr>\n\t<tr>\n    <td colspan=2 align=left><input type="submit" value="Run Remote Command" /></td>\n    </tr>\n</table>\n</form>\n\n')
        if c.state:
            __M_writer(u'  <table>\n  <tr><td colspan=2><h3>Output:</h3></td></tr>\n  <tr><td align=left><h4>Jobname:  </h4></td> <td> ')
            __M_writer(escape(c.jobname))
            __M_writer(u'</td></tr>\n  <tr><td align=left><h4>JobID:  </h4></td> <td> ')
            __M_writer(escape(c.jobid))
            __M_writer(u'</td></tr>\n  <tr><td align=left><h4>Hostname:  </h4></td> <td> ')
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
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 63, "40": 3, "45": 3, "46": 6, "47": 6, "48": 24, "49": 25, "50": 25, "52": 25, "53": 26, "54": 26, "55": 26, "56": 26, "57": 26, "58": 26, "59": 28, "60": 30, "61": 31, "62": 31, "64": 31, "65": 32, "66": 32, "67": 32, "68": 32, "69": 32, "70": 32, "71": 34, "72": 48, "73": 49, "74": 51, "75": 51, "76": 52, "77": 52, "78": 53, "79": 53, "80": 54, "81": 54, "82": 57, "83": 58, "84": 58, "85": 58, "86": 60, "92": 86}, "uri": "/demos/demo_basicjob.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/demos/demo_basicjob.mako"}
__M_END_METADATA
"""
