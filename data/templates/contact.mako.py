# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1463973655.761125
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/contact.mako'
_template_uri = '/contact.mako'
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
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col1main(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n<h3> CyberWeb Project Contact Form</h3>\n\n')
        if c.state == 'finish' :
            __M_writer(u'  <blockquote>\n  <h2>Thanks for your feedback.\n      <br>Your input will be sent to the CyberWeb development team::</h2>\n  <blockquote>')
            __M_writer(escape(c.istr))
            __M_writer(u"</blockquote>\n  <form action='' method='post'>\n  <input type='hidden' name='state' value='' >\n  <blockquote>\n      <input type='submit' value='Sumbit More Feedback' name='form' >\n  </blockquote>\n   <p>In the event of problems with this form,  <a href='mailto:mthomas@sciences.sdsu.edu'>Mary Thomas</a>\n\n  </form>\n  </blockquote>\n")
        else:
            __M_writer(u'\n<blockquote>\n   <h2>Use this form to report things you like or problems, issues you encounter.<br>\n       Please Provide copies of error messages if possible.\n  </h2>\n  <p>\n  <form action=\'\' method=\'post\'>\n   <table size="500">\n      <tr >\n         <td size="150">Name:</td>\n         <td><input type="text" size="200" name="name" value="')
            __M_writer(escape(c.info['name']))
            __M_writer(u'" /></td>\n      </tr>\n      <tr>\n         <td>CW Account Name<br>(if you have one):</td>\n        <td><input type="text" name="cwuser" value="')
            __M_writer(escape(c.info['cwuser']))
            __M_writer(u'" /></td>\n      </tr>\n      <tr>\n         <td>Email:</td>\n         <td><input type="text" name="email" value="')
            __M_writer(escape(c.info['email']))
            __M_writer(u'" /></td>\n      </tr>\n      <tr>\n         <td>Comments:</td>\n         <td>\n           <textarea class="html-text-box" name="comments">')
            __M_writer(escape(c.info['comments']))
            __M_writer(u'</textarea>\n           </td>\n      </tr>\n     <tr>\n       <td align=center colspan=2>\n       <input type="submit" value="Submit Information/Request" name="form" />\n       </td>\n     <tr>\n       <td align=center colspan=2>\n       In the event of problems with this form,  <a href="mailto:mthomas@sciences.sdsu.edu">Mary Thomas</a>\n       </td>\n     </tr>\n\n   </table>\n</blockquote>\n<input type="hidden" name="state" value="process" />\n</form>\n')
        __M_writer(u'\n<hr>\n<h3>Output:</h3>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"33": 1, "65": 59, "39": 3, "44": 3, "45": 7, "46": 8, "47": 11, "48": 11, "49": 21, "50": 22, "51": 32, "52": 32, "53": 36, "54": 36, "55": 40, "56": 40, "57": 45, "58": 45, "59": 63, "28": 0}, "uri": "/contact.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/contact.mako"}
__M_END_METADATA
"""
