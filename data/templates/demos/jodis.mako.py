# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1468535541.225274
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/demos/jodis.mako'
_template_uri = '/demos/jodis.mako'
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
        __M_writer(u'\n        <h3> Cyberweb Execution Services: Demo JODIS functionality.</h3>\n\t<br>\n\t<form action="" method="post">\n\t<table border=0>\n\t    <tr><th>Current Jobs</th></tr>\n')
        for i in c.current_jobs:
            __M_writer(u'\t    <tr><td>\n')
            if c.jobname == i:
                __M_writer(u'                \t<input type="radio" name="job" value="')
                __M_writer(escape(i))
                __M_writer(u'" checked>&nbsp;&nbsp;&nbsp;')
                __M_writer(escape(i))
                __M_writer(u'<br>\n')
            else:
                __M_writer(u'                \t<input type="radio" name="job" value="')
                __M_writer(escape(i))
                __M_writer(u'">&nbsp;&nbsp;&nbsp;')
                __M_writer(escape(i))
                __M_writer(u'<br>\n')
            __M_writer(u'\t    </td></tr>\n')
        __M_writer(u'            <tr><td>\n\t\t<input type="radio" name="job" value="add">&nbsp;&nbsp;&nbsp;Add a new job\n\t\t<select name="service">\n')
        for i in c.services:
            if c.service_id == i.id:
                __M_writer(u'\t\t\t\t<option value="')
                __M_writer(escape(i.id))
                __M_writer(u'" selected="selected">')
                __M_writer(escape(i.service_name.name))
                __M_writer(u' @ ')
                __M_writer(escape(i.resource.name))
                __M_writer(u'</option>\n')
            else:
                __M_writer(u'\t\t\t\t<option value="')
                __M_writer(escape(i.id))
                __M_writer(u'">')
                __M_writer(escape(i.service_name.name))
                __M_writer(u' @ ')
                __M_writer(escape(i.resource))
                __M_writer(u'</option>\n')
        __M_writer(u'\t\t</select>\n\t    </td></tr>\n\t</table>\n')
        if c.job:
            __M_writer(u'\t\t<table>\n\t\t<tr><th colspan="2">')
            __M_writer(escape(c.jobname))
            __M_writer(u'</th></tr>\n\t\t<tr><th>ID:</th><td>')
            __M_writer(escape(c.job.id))
            __M_writer(u'</td></tr>\n\t\t<tr><th>Name:</th><td>')
            __M_writer(escape(c.job.name))
            __M_writer(u'</td></tr>\n\t\t<tr><th>Service:</th><td>')
            __M_writer(escape(c.job.service.service_name.name))
            __M_writer(u' (')
            __M_writer(escape(c.job.service.id))
            __M_writer(u')</td></tr>\n\t\t<tr><th>Resource:</th><td>')
            __M_writer(escape(c.job.service.resource.name))
            __M_writer(u'</td></tr>\n\t\t<tr><th>State:</th><td>')
            __M_writer(escape(c.job.state))
            __M_writer(u'</td></tr>\n')
            if not len(c.job.listTasks()):
                __M_writer(u'\t\t\t<tr><th>Tasks:</th><td>No Tasks</tr></tr>\n')
            else:
                __M_writer(u'\t\t\t')
                tasklen = len(c.job.listTasks()) + 1 
                
                __M_writer(u'\n\t\t\t<tr><th rowspan="')
                __M_writer(escape(tasklen))
                __M_writer(u'">Tasks:</th></tr>\n')
                for i in c.job.listTasks():
                    __M_writer(u'\t\t\t\t<tr><td>')
                    __M_writer(escape(i))
                    __M_writer(u'</tr></td>\n')
            __M_writer(u'                <tr><td colspan="2">\n\t\t\t\t\t<input type="radio" name="task" value="add">&nbsp;&nbsp;&nbsp;Add a new task<br>\n                </td></tr>\n')
            if c.job.listTasks():
                __M_writer(u'                <tr><td colspan="2">\n\t\t\t\t\t<input type="radio" name="task" value="run">&nbsp;&nbsp;&nbsp;Run the job<br>\n                </td></tr>\n                <tr><td colspan="2">\n\t\t\t\t\t<input type="radio" name="task" value="monitor">&nbsp;&nbsp;&nbsp;Monitor the job<br>\n                </td></tr>\n')
            __M_writer(u'                <input type="hidden" name="jobname" value="')
            __M_writer(escape(c.jobname))
            __M_writer(u'"/>\n\t\t</table>\n')
        __M_writer(u'\t<input type="submit" value="Run Remote Command" />\n\t</form>\n\t\n')
        if c.monitor:
            __M_writer(u'\t\t<table>\n\t\t\t<tr>\n\t\t\t\t<th>Job</th>\n\t\t\t\t<th>Queue ID</th>\n\t\t\t\t<th>Status</th>\n\t\t\t</tr>\n')
            for job, i in c.monitor.items():
                __M_writer(u'\t\t\t<tr>\n\t\t\t\t<td>')
                __M_writer(escape(job))
                __M_writer(u'</td><td>')
                __M_writer(escape(i[0][0]))
                __M_writer(u'</td><td>')
                __M_writer(escape(i[0][1]))
                __M_writer(u'</td>\n\t\t\t</tr>\n')
            __M_writer(u'\t\t</table>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 79, "40": 3, "46": 3, "47": 9, "48": 10, "49": 11, "50": 12, "51": 12, "52": 12, "53": 12, "54": 12, "55": 13, "56": 14, "57": 14, "58": 14, "59": 14, "60": 14, "61": 16, "62": 18, "63": 21, "64": 22, "65": 23, "66": 23, "67": 23, "68": 23, "69": 23, "70": 23, "71": 23, "72": 24, "73": 25, "74": 25, "75": 25, "76": 25, "77": 25, "78": 25, "79": 25, "80": 28, "81": 31, "82": 32, "83": 33, "84": 33, "85": 34, "86": 34, "87": 35, "88": 35, "89": 36, "90": 36, "91": 36, "92": 36, "93": 37, "94": 37, "95": 38, "96": 38, "97": 39, "98": 40, "99": 41, "100": 42, "101": 42, "103": 42, "104": 43, "105": 43, "106": 44, "107": 45, "108": 45, "109": 45, "110": 48, "111": 51, "112": 52, "113": 59, "114": 59, "115": 59, "116": 62, "117": 65, "118": 66, "119": 72, "120": 73, "121": 74, "122": 74, "123": 74, "124": 74, "125": 74, "126": 74, "127": 77, "133": 127}, "uri": "/demos/jodis.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/demos/jodis.mako"}
__M_END_METADATA
"""
