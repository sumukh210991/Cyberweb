# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1350123182.4849229
_enable_loop = True
_template_filename = '/home/smita/cyberweb/cyberweb/templates/gcem/gcem.mako'
_template_uri = '/gcem/gcem.mako'
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
        # SOURCE LINE 14
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
        __M_writer(u'\n<h3>')
        # SOURCE LINE 4
        __M_writer(escape(c.title))
        __M_writer(u'</h3>\n<p>\n\n<h2>GCEM Simulation Manager: A Workflow for building and running GCEM Ocean Models</h2>\n<ul>\n<li>CREATE:  build a new Simulation, and save (can be reused/copied for next job) </li>\n<li>EXECUTE:  select [existing simulation  OR create new (redirect)], set params for running and submit job to queue </li>\n<li>MONITOR: job monitor/interactive/view interim results/cancel </li>\n<li>ANALYZE: view perf and other data. Save/Del/Cancel (if running)/resub </li>\n</ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


