# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1468440947.39433
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/exec/exec.mako'
_template_uri = '/exec/exec.mako'
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
        __M_writer(u'\n\n')
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
        __M_writer(u'</h3>\n<p>\n\n   <table>\n   <tr> <td>\n  <div class="infobar">MyJobs</div>\n  <table>\n     <tr align=left valign=top>\n        <th>ID</th>\n        <th>Job Name</th>\n        <th>Status</th>\n        <th>Resource</th>\n        <th>Submit</th>\n        <th>Start</th>\n        <th>End </th>\n      </tr>\n')
        for j in c.jobs:
            __M_writer(u'      <tr align=left valign=top>\n          <td>')
            __M_writer(escape(j['ID']))
            __M_writer(u'</td>\n          <td>')
            __M_writer(escape(j['Name']))
            __M_writer(u'</td>\n          <td>')
            __M_writer(escape(j['Resource']))
            __M_writer(u'</td>\n          <td>C</td>\n          <td>')
            __M_writer(escape(j['Submit Time']))
            __M_writer(u'</td>\n          <td>')
            __M_writer(escape(j['Start Time']))
            __M_writer(u'</td>\n          <td>')
            __M_writer(escape(j['End Time']))
            __M_writer(u'</td>\n      </tr>\n')
        __M_writer(u'  </table>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 33, "40": 3, "45": 3, "46": 4, "47": 4, "48": 20, "49": 21, "50": 22, "51": 22, "52": 23, "53": 23, "54": 24, "55": 24, "56": 26, "57": 26, "58": 27, "59": 27, "60": 28, "61": 28, "62": 31, "68": 62}, "uri": "/exec/exec.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/exec/exec.mako"}
__M_END_METADATA
"""
