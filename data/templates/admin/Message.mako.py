# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1468813642.546569
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/admin/Message.mako'
_template_uri = '/admin/Message.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headtags', 'col2left', 'col2main']


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
    return runtime._inherit_from(context, u'/admin/newAdmin.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headtags(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n\t<script type="text/javascript" src="/js/admin/message.js"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col2left(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\t')
        __M_writer(escape(self.col2left()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col2main(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\t<div id="maincontent">\n\t\t<div id="errorConsole" class="errorStyle"></div>\n\t\t<div id="menu">\n\t\t\t<ul id="menuList">\n\t\t\t\t<li id="messageTypeLi" class="selected" onclick="switchTabs(this);">Message Type</li>\n\t\t\t\t<li id="messageLi" onclick="switchTabs(this);">Message</li>\n\t\t\t</ul>\n\t\t</div>\n\t\t<div id="searchcontainer">\n\t\t\t<div id="messageTypeTab" class="classTab">\n\t\t\t\t<h2 class="header">Message Types</h2>\n\t\t\t\t<div id="errorConsoleMessageType" class="errorStyle"></div>\n\t\t\t\t<div id="activity_pane_messageType">\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="messageTypeSearchContent" class="searchContent">\t\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t\t<div id="messageTab" class="classTab">\n\t\t\t\t<h2 class="header">Messages</h2>\n\t\t\t\t<div id="errorConsoleMessage" class="errorStyle"></div>\n\t\t\t\t<div id="activity_pane_message">\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="messageSearchContent" class="searchContent">\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t</div>\n\t<script type="text/javascript">\n\t\tvar decodedUserString = $("<div/>").html("')
        __M_writer(escape(c.userString))
        __M_writer(u'").text();\n\t\tvar decodedGroupString = $("<div/>").html("')
        __M_writer(escape(c.groupString))
        __M_writer(u'").text();\n\t\tvar decodedMessageTypeString = $("<div/>").html("')
        __M_writer(escape(c.messageTypeString))
        __M_writer(u'").text();\n\t\t\n\t\tuserString = eval(\'(\' + decodedUserString + \')\');\n\t\tgroupString = eval(\'(\' + decodedGroupString + \')\');\n\t\tmessageTypeString = eval(\'(\' + decodedMessageTypeString + \')\');\n\t\tinit();\n\t</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"64": 11, "33": 1, "34": 5, "35": 9, "69": 11, "70": 52, "71": 52, "72": 53, "41": 3, "74": 54, "75": 54, "45": 3, "81": 75, "51": 7, "73": 53, "56": 7, "57": 8, "58": 8, "28": 0}, "uri": "/admin/Message.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/admin/Message.mako"}
__M_END_METADATA
"""
