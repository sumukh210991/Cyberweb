# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467227487.0436
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/data/jobmonitor.mako'
_template_uri = '/data/jobmonitor.mako'
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
        sorted = context.get('sorted', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n  <style type="text/css">\n    .infobar {\n      background:#cccccc;\n      padding-left:2px;\n      margin-bottom:2px;\n    }\n\n    table, td, th, thc,tdc {\n      border:0px solid black;\n    }\n    th {\n      vertical-align:top;\n      text-align:left; \n    }\n    td {\n      vertical-align:top;\n      text-align:left; \n    }\n    thc {\n      vertical-align:top;\n      text-align:center;\n    }\n    tdc {\n      vertical-align:top;\n      text-align:center;\n    }\n  </style>\n\n<h3>')
        __M_writer(escape(c.title))
        __M_writer(u'</h3>\n<form action="/data/jobmonitor" method="post">\n<blockquote>\n<input type="submit" name="jobmonitor" value="Update My Jobs" />\n</blockquote>\n<blockquote>\n      <table >\n          <tr align=left valign=top>\n             <th>ID</th>\n             <th>Job Name</th>\n             <th>Status</th>\n             <th>Resource</th>\n             <th>Submit Time</th>\n             <th>Start Time</th>\n             <th>End Time</th>\n          </tr>\n')
        if c.jobs:
            for job in c.jobs:
                __M_writer(u'          <tr align=left valign=top>\n\t     <td>')
                __M_writer(escape(job['ID']))
                __M_writer(u'</td>\n\t     <td>')
                __M_writer(escape(job['Name']))
                __M_writer(u'</td>\n             <td>')
                __M_writer(escape(job['StatusKey']))
                __M_writer(u'</td>\n             <td>')
                __M_writer(escape(job['Resource']))
                __M_writer(u'</td>\n\t     <td>')
                __M_writer(escape(job['Submit Time']))
                __M_writer(u'</td>\n\t     <td>')
                __M_writer(escape(job['Start Time']))
                __M_writer(u'</td>\n             <th>Etime</th>\n          </tr>\n')
        else:
            __M_writer(u'          <tr align=left valign=top>\n             <th> </th> <th> </th> <th> </th> <th> </th> <th> </th> <th> </th> <th> </th>\n          </tr>\n')
        __M_writer(u'\n      </table>\n   <blockquote>\n      Status Keys:[ \n')
        for key, value in sorted(c.jobstateheaders.iteritems(), key=lambda (k,v): (v,k)):
            __M_writer(u'          ')
            __M_writer(escape(key))
            __M_writer(u'=')
            __M_writer(escape(value))
            __M_writer(u' ,\n')
        __M_writer(u'      ] <br>\n   </blockquote>\n</blockquote>\n\n\n<input type="hidden" name="jobname" value="')
        __M_writer(escape(c.jobname))
        __M_writer(u'" />\n</form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 79, "40": 3, "46": 3, "47": 32, "48": 32, "49": 48, "50": 49, "51": 50, "52": 51, "53": 51, "54": 52, "55": 52, "56": 53, "57": 53, "58": 54, "59": 54, "60": 55, "61": 55, "62": 56, "63": 56, "64": 60, "65": 61, "66": 65, "67": 69, "68": 70, "69": 70, "70": 70, "71": 70, "72": 70, "73": 72, "74": 77, "75": 77, "81": 75}, "uri": "/data/jobmonitor.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/data/jobmonitor.mako"}
__M_END_METADATA
"""
