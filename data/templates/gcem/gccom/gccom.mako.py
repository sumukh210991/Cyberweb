# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467227206.396088
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/gcem/gccom/gccom.mako'
_template_uri = '/gcem/gccom/gccom.mako'
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
        __M_writer(u'</h3>\n<p>\n<form action="/gccom/jobmonitor" method="post">\n<blockquote>\n<input type="submit" name="jobmonitor" value="Update My Jobs" />\n</blockquote>\n<blockquote>\n      <table >\n          <tr align=left valign=top>\n             <!--<th>ID</th>-->\n             <th>Job Name</th>\n             <th>Status</th>\n             <th>Resource</th>\n             <th>Submit Time</th>\n             <th>Start Time</th>\n             <th>End Time</th>\n          </tr>\n')
        if c.jobs:
            for job in c.jobs:
                __M_writer(u'          <tr align=left valign=top>\n             <td>')
                __M_writer(escape(job['Name']))
                __M_writer(u'</td>\n             <td>')
                __M_writer(escape(job['StatusKey']))
                __M_writer(u'</td>\n             <td>')
                __M_writer(escape(job['Resource']))
                __M_writer(u'</td>\n             <td>')
                __M_writer(escape(job['Submit Time']))
                __M_writer(u'</td>\n             <td>')
                __M_writer(escape(job['Start Time']))
                __M_writer(u'</td>\n             <th>Etime</th>\n          </tr>\n')
        else:
            __M_writer(u'          <tr align=left valign=top>\n             <th> </th> <th> </th> <th> </th> <th> </th> <th> </th> <th> </th> <th> </th>\n          </tr>\n')
        __M_writer(u'\n      </table>\n\t<pre><blockquote>\n      Status Keys:[ \n       for key, value in sorted(c.jobstateheaders.iteritems(), key=lambda (k,v): (v,k)):\n          {key}={value} ,\n       endfor\n      \n      ] </pre><br>\n   </blockquote>\n</blockquote>\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 50, "40": 3, "45": 3, "46": 4, "47": 4, "48": 21, "49": 22, "50": 23, "51": 24, "52": 24, "53": 25, "54": 25, "55": 26, "56": 26, "57": 27, "58": 27, "59": 28, "60": 28, "61": 32, "62": 33, "63": 37, "69": 63}, "uri": "/gcem/gccom/gccom.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/gcem/gccom/gccom.mako"}
__M_END_METADATA
"""
