# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1350123761.8453729
_enable_loop = True
_template_filename = '/home/smita/cyberweb/cyberweb/templates/gcem/gcem_sim_details.mako'
_template_uri = '/gcem/gcem_sim_details.mako'
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
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 54
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col1main(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 3
        __M_writer(u'\n<style type="text/css">\n    table, td, th\n    {\n    width:600px;\n    border:1px solid black;\n    }\n    td\n    {\n    height:400px;\n    vertical-align:top;\n    }\n\n    #jobs table, #jobs th, #jobs td\n    {\n    width:600px;\n    border:1px solid black;\n    }\n    #jobs th\n    {\n    height:200px;\n    vertical-align:top;\n    }\n    #jobs td\n    {\n    height:200px;\n    vertical-align:top;\n    }\n</style>\n\n<h3>')
        # SOURCE LINE 33
        __M_writer(escape(c.title))
        __M_writer(u'</h3>\n<p>\n\n\n<blockquote>\n   <table id="jobs">\n   <tr><td>\n   list all jobs in top panel job status/progress\n   </td></tr>\n   </table>\n</blockquote>\n<blockquote>\n   <table style="vertical:600px">\n   <tr><td>\n   <p> on selection of job in panel above, display job details\n   <p>interact with job (cancel)\n   <p>view interim results --> redirect to analyze \n   </td></tr>\n   </table>\n</blockquote>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


