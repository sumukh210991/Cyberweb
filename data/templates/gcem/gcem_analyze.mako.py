# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1350123762.6458759
_enable_loop = True
_template_filename = '/home/smita/cyberweb/cyberweb/templates/gcem/gcem_analyze.mako'
_template_uri = '/gcem/gcem_analyze.mako'
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
        # SOURCE LINE 18
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
        __M_writer(u'</h3>\n<p>\n<blockquote>\n<h2>\nANALYZE: view perf and other data. Save/Del/Cancel (if running)/resub \n</h2>\n<ul>\n   <li> list items here\n   <li> list items here\n</li>\n</ul>\n</blockquote>\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


