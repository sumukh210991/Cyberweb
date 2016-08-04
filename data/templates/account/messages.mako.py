# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1468538758.846641
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/messages.mako'
_template_uri = '/account/messages.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headtags', 'col2main']


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
    return runtime._inherit_from(context, u'/account/account.layout.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n')
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


def render_col2main(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<script type="text/javascript">\n     function sendMessage(){\n         var recipient = document.MessageForm.recipient.value;\n         var message = document.MessageForm.message.value;\n\n         var dataString = "recipient=" + recipient + "&message=" + message;\n         $.ajax({\n               type: "POST",\n               url: "/user/send_message",\n               data: dataString,\n               error: function(msg){\n\t\t   var status = eval(\'(\' + msg + \')\');\n\t\t   if (status.error) {\n                       alert("Error: " + status.message);\n\t\t   }\n               },\n               success: function(msg){\n\t\t   var status = eval(\'(\' + msg + \')\');\n\t\t   if (!status.error) {\n                       alert(status.message);\n\t\t   }\n               }\n        });\n        return;\n     };\n</script>\n\n<h2>')
        __M_writer(escape(c.title))
        __M_writer(u'</h2>\n<h3>CyberWeb Information Services</h3>\n<br>\n<h3>Received Messages</h3>\n')
        if len(c.messages):
            __M_writer(u'  <table>\n    <tr>\n')
            for j in c.messageheaders:
                __M_writer(u'        <th>')
                __M_writer(escape(j))
                __M_writer(u'</th>\n')
            __M_writer(u'    </tr>\n')
            for i in c.messages:
                __M_writer(u'        <tr>\n')
                for j in c.messageheaders:
                    if i.has_key(j):
                        __M_writer(u'            <td>')
                        __M_writer(escape(i[j]))
                        __M_writer(u'</td>\n')
                    else:
                        __M_writer(u'            <td></td>\n')
                __M_writer(u'        </tr>\n')
            __M_writer(u'  </table>\n')
        else:
            __M_writer(u'      You have no messages at this time. <br>\n')
        __M_writer(u'<p>&nbsp;\n<p>&nbsp;\n<hr>\n  <form name="MessageForm" action="#" method="POST">\n    <div class="sendMessageBox">\n    Send\n    <select name="recipient">\n')
        for i in c.recipients:
            __M_writer(u'          <option value="')
            __M_writer(escape(i['value']))
            __M_writer(u'">')
            __M_writer(escape(i['name']))
            __M_writer(u'</option>\n')
        __M_writer(u'    </select>\n    a message.<p>\n    <textarea name="message" class="html-text-box">Enter your message here... </textarea>\n      <p><input type="button" value="Send Message" onClick="sendMessage()"/>\n      <p><a onClick="sendMessage()">Send Message</a>\n    </div>\n  </form>\n  <br>\n  <p>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 4, "35": 79, "41": 3, "45": 3, "51": 6, "57": 6, "58": 34, "59": 34, "60": 38, "61": 39, "62": 41, "63": 42, "64": 42, "65": 42, "66": 44, "67": 45, "68": 46, "69": 47, "70": 48, "71": 49, "72": 49, "73": 49, "74": 50, "75": 51, "76": 54, "77": 56, "78": 57, "79": 58, "80": 60, "81": 67, "82": 68, "83": 68, "84": 68, "85": 68, "86": 68, "87": 70, "93": 87}, "uri": "/account/messages.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/messages.mako"}
__M_END_METADATA
"""
