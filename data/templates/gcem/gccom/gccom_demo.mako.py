# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467227211.688736
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/gcem/gccom/gccom_demo.mako'
_template_uri = '/gcem/gccom/gccom_demo.mako'
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
    return runtime._inherit_from(context, u'/gcem/gcem.layout.2col.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col2main(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n<h3> ')
        __M_writer(escape(c.title))
        __M_writer(u'</h3>\n<blockquote>\nChoose one of the pre-configured demonstration models listed on tde menu.\n<table>\n  <tr>\n     <td><b>Lid Driven Cavity Test Case</b></td>\n     <td>\n        <img src="/images/ldc.jpg" style="width:150px;height:100px"> \n      </td>\n  </tr>\n  <tr>\n     <td><b>Temperature Test Cases (I and II)</b> </td>\n     <td>\n        <img src="/images/temperature.jpg" style="width:150px;height:100px"> \n      </td>\n  </tr>\n  <tr>\n     <td><b>Seamount Test Case </b> </td>\n     <td>\n        <img src="/images/seamount.jpg" style="width:150px;height:100px"> \n      </td>\n  </tr>\n</table>\n</blockquote>\n<br>\n<br>\n<br>\n<br>\n<br>\n<br>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"33": 1, "34": 36, "40": 3, "45": 3, "46": 5, "47": 5, "53": 47, "28": 0}, "uri": "/gcem/gccom/gccom_demo.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/gcem/gccom/gccom_demo.mako"}
__M_END_METADATA
"""
