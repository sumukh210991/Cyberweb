# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467227488.105134
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/data/upload.mako'
_template_uri = '/data/upload.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headtags', 'footer', 'header']


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
    return runtime._inherit_from(context, u'/layout.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n\n\n')
        __M_writer(u'<form action="" enctype="multipart/form-data" method="post">\n<p>\nPlease specify a file to upload:<br>\n<input type="file" name="datafile" size="40">\n</p>\n<div>\n<input type="submit" value="Send">\n</div>\n</form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headtags(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footer(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_header(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"64": 8, "33": 2, "34": 3, "35": 6, "36": 9, "37": 12, "38": 17, "74": 68, "44": 5, "48": 5, "54": 11, "68": 8, "58": 11, "28": 0}, "uri": "/data/upload.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/data/upload.mako"}
__M_END_METADATA
"""
