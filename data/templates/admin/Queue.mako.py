# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1468813648.389106
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/admin/Queue.mako'
_template_uri = '/admin/Queue.mako'
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
        __M_writer(u'\n\t<script type="text/javascript" src="/js/admin/queue.js"></script>\n')
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
        __M_writer(u'\n\t<div id="maincontent">\n\t\t<div id="errorConsole" class="errorStyle"></div>\n\t\t<div id="menu">\n\t\t\t<ul id="menuList">\n\t\t\t\t<li id="queueTypeLi" class="selected" onclick="switchTabs(this);">Queue Type</li>\n\t\t\t\t<li id="queueInfoLi" onclick="switchTabs(this);">Queue Info</li>\n\t\t\t\t<li id="queueSystemLi" onclick="switchTabs(this);">Queue System</li>\n\t\t\t\t<li id="queueServiceLi" onclick="switchTabs(this);">Queue Service</li>\n\t\t\t</ul>\n\t\t</div>\n\t\t<div id="searchcontainer">\n\t\t\t<div id="queueTypeTab" class="classTab">\n\t\t\t\t<h2 class="header">Queue Types</h2>\n\t\t\t\t<div id="errorConsoleQueueType" class="errorStyle"></div>\n\t\t\t\t<div id="activity_pane_queueType">\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="queueTypeSearchContent" class="searchContent">\t\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t\t<div id="queueInfoTab" class="classTab">\n\t\t\t\t<h2 class="header">Queue Infos</h2>\n\t\t\t\t<div id="errorConsoleQueueInfo" class="errorStyle"></div>\n\t\t\t\t<div id="activity_pane_queueInfo">\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="queueInfoSearchContent" class="searchContent">\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t\t<div id="queueSystemTab" class="classTab">\n\t\t\t\t<h2 class="header">Queue Systems</h2>\n\t\t\t\t<div id="errorConsoleQueueSystem" class="errorStyle"></div>\n\t\t\t\t<div id="activity_pane_queueSystem">\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="queueSystemSearchContent" class="searchContent">\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t\t<div id="queueServiceTab" class="classTab">\n\t\t\t\t<h2 class="header">Queue Service</h2>\n\t\t\t\t<div id="errorConsoleQueueService" class="errorStyle"></div>\n\t\t\t\t<div id="activity_pane_queueService">\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="queueServiceSearchContent" class="searchContent">\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t</div>\n\t<script type="text/javascript">\n\t\tvar decodedResourceString = $("<div/>").html("')
        __M_writer(escape(c.resourceString))
        __M_writer(u'").text();\n\t\tvar decodedQueueTypeString = $("<div/>").html("')
        __M_writer(escape(c.queueTypeString))
        __M_writer(u'").text();\n\t\tvar decodedQueueInfoString = $("<div/>").html("')
        __M_writer(escape(c.queueInfoString))
        __M_writer(u'").text();\n\t\tvar decodedQueueSystemString = $("<div/>").html("')
        __M_writer(escape(c.queueSystemString))
        __M_writer(u'").text();\n\t\t\n\t\tresourceString = eval(\'(\' + decodedResourceString + \')\');\n\t\tqueueTypeString = eval(\'(\' + decodedQueueTypeString + \')\');\n\t\tqueueInfoString = eval(\'(\' + decodedQueueInfoString + \')\');\n\t\tqueueSystemString = eval(\'(\' + decodedQueueSystemString + \')\');\n\t\t\n\t\tinit();\n\t</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"64": 11, "33": 1, "34": 5, "35": 9, "69": 11, "70": 82, "71": 82, "72": 83, "41": 3, "74": 84, "75": 84, "76": 85, "45": 3, "77": 85, "51": 7, "73": 83, "56": 7, "57": 8, "58": 8, "28": 0, "83": 77}, "uri": "/admin/Queue.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/admin/Queue.mako"}
__M_END_METADATA
"""
