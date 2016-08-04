# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467226821.335095
_enable_loop = True
_template_filename = u'/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/2col-left.mako'
_template_uri = u'/2col-left.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['footer', 'headtags', 'subnavtabs', 'header']


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
        app_globals = context.get('app_globals', UNDEFINED)
        request = context.get('request', UNDEFINED)
        tmpl_context = context.get('tmpl_context', UNDEFINED)
        next = context.get('next', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n')

        from authkit.authorize.pylons_adaptors import authorized
        from cyberweb.lib import auth
        
        session = request.environ['beaker.session']
        g = app_globals
        c = tmpl_context
        
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['g','c','session','authorized','auth'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n<div class="col2-left">\n    ')
        __M_writer(escape(next.col2left()))
        __M_writer(u'\n</div>\n<div class="col2-main">\n    ')
        __M_writer(escape(next.col2main()))
        __M_writer(u'\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footer(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(escape(self.footer()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headtags(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        next = context.get('next', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\t')
        __M_writer(escape(next.headtags()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_subnavtabs(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(escape(self.subnavtabs()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_header(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(escape(self.header()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "37": 1, "38": 3, "49": 10, "50": 14, "51": 18, "52": 22, "53": 26, "54": 29, "55": 29, "56": 32, "57": 32, "63": 24, "68": 24, "69": 25, "70": 25, "76": 12, "81": 12, "82": 13, "83": 13, "89": 20, "94": 20, "95": 21, "96": 21, "102": 16, "107": 16, "108": 17, "109": 17, "115": 109}, "uri": "/2col-left.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/2col-left.mako"}
__M_END_METADATA
"""
