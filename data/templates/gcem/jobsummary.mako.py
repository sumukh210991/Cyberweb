# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1465687765.363064
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/gcem/jobsummary.mako'
_template_uri = '/gcem/jobsummary.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['col1main']


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
    return runtime._inherit_from(context, u'/1col.mako', _template_uri)
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


def render_col1main(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<h3>')
        __M_writer(escape(c.title))
        __M_writer(u'</h3>\n<form action="/gccom/jobsummary" method="post">\n<blockquote>\n<!--- _states = [\'setup\',\'queued\', \'running\', \'idle\', \'paused\', \'finished\', \'error\', \'cancelled\', \'timeout\', \'unknown\'] --->\n<blockquote>\n     <input type="submit" name="jobsummary" value="MyJobs" />\n<p>\n  <table>\n     <tr align=left valign=top>\n        <th>ID</th>\n        <th>Job Name</th>\n        <th>Status</th>\n        <th>Resource</th>\n        <th>Submit Time</th>\n        <th>Start Time</th>\n        <th>End Time</th>\n      </tr>\n')
        for job in c.jobs:
            __M_writer(u'      <tr align=center valign=top>\n          <td>')
            __M_writer(escape(job['ID']))
            __M_writer(u'</td>\n          <td>')
            __M_writer(escape(job['Name']))
            __M_writer(u'</td>\n          <td>')
            __M_writer(escape(job['StatusKey']))
            __M_writer(u' </td>\n          <td>')
            __M_writer(escape(job['Resource']))
            __M_writer(u'</td>\n\t  <td>')
            __M_writer(escape(job['Submit Time']))
            __M_writer(u'</td>\n\t  <td>')
            __M_writer(escape(job['Start Time']))
            __M_writer(u'</td>\n\t  <td>')
            __M_writer(escape(job['End Time']))
            __M_writer(u'</td>\n      </tr>\n')
        __M_writer(u'  </table>\n</blockquote>\n\n<blockquote>\n   </blockquote>\n         <input type="hidden" name="jobname" value="')
        __M_writer(escape(c.jobname))
        __M_writer(u'" />\n</form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 39, "40": 3, "45": 3, "46": 4, "47": 4, "48": 21, "49": 22, "50": 23, "51": 23, "52": 24, "53": 24, "54": 25, "55": 25, "56": 26, "57": 26, "58": 27, "59": 27, "60": 28, "61": 28, "62": 29, "63": 29, "64": 32, "65": 37, "66": 37, "72": 66}, "uri": "/gcem/jobsummary.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/gcem/jobsummary.mako"}
__M_END_METADATA
"""
