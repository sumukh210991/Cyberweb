# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1468782506.882564
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/news.mako'
_template_uri = '/account/news.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headtags', 'footer']


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
        c = context.get('c', UNDEFINED)
        endfor = context.get('endfor', UNDEFINED)
        endif = context.get('endif', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n\n<div class="col1-main">\n\n  <div id="newsandmessages">\n        <h3>News and Messages</h3>\n  ')

        cnt=0
        context.write('<table class="d0">')
        for m in c.messages:
           if ( (cnt % 2) == 0 ):
              context.write('<tr class="d0">')
              context.write('<td width=100><mfd0>' + m["date"] + ': </mfd1> </td><td> </mfd0><mf0>' + m["message"] + '</mf0</td>' )
              context.write('</tr>')
           else:
              context.write('<tr class="d1">')
              context.write('<td width=100><mfd1>' + m["date"] + ': </mfd1> </td><td> <mf1>' + m["message"] + '</mf1></td>' )
              context.write('</tr>')
           endif
           cnt=cnt+1
        endfor
        context.write("</table>")
          
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['cnt','m'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'  \n  </div>\n\n\n\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headtags(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n\t<script type="text/javascript" src="http://jqueryui.com/latest/jquery-1.3.2.js"></script>\n')
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


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"65": 3, "36": 1, "37": 5, "38": 8, "39": 15, "75": 7, "79": 7, "85": 79, "59": 31, "28": 0, "69": 3}, "uri": "/account/news.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/news.mako"}
__M_END_METADATA
"""
