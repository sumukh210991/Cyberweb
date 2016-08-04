# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467226898.260309
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/admin/Resource.mako'
_template_uri = '/admin/Resource.mako'
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
        __M_writer(u'\n\t<script type="text/javascript" src="/js/admin/resource.js"></script>\n')
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
        __M_writer(u'\n\t<div id="maincontent">\n\t\t<div id="errorConsole" class="errorStyle"></div>\n\t\t<div id="menu">\n\t\t\t<ul id="menuList">\n\t\t\t\t<li id="resourceNameLi" class="selected" onclick="switchTabs(this);">Resource Name</li>\n\t\t\t\t<li id="resourceLi" onclick="switchTabs(this);">Resource</li>\n\t\t\t</ul>\n\t\t</div>\n\t\t<div id="searchcontainer">\n\t\t\t<div id="resourceNameTab" class="classTab">\n\t\t\t\t<h2 class="header">Resource Names</h2>\n\t\t\t\t<div id="errorConsoleResourceName" class="errorStyle"></div>\n\t\t\t\t<div id="activity_pane_resourceName">\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="resourceNameSearchContent" class="searchContent">\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t\t<div id="resourceTab" class="classTab">\n\t\t\t\t<table id="searchResource">\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td><label>Resources:</label></td>\n\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t<select id="resourceList" name="resources" MULTIPLE>\n\t\t\t\t\t\t\t\n')
        for resource in c.resource:
            __M_writer(u'\t\t\t\t\t\t\t\t<option value="')
            __M_writer(escape(resource.id))
            __M_writer(u'">')
            __M_writer(escape(resource.name))
            __M_writer(u'</option>\n')
        __M_writer(u'\t\t\t\t\t\t\t</select>\n\t\t\t\t\t\t</td>\n\t\t\t\t\t</tr>\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td></td>\n\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t<input type="button" class="buttonStyle" value="Show Services" onclick="searchResource();"/> <input type="button" class="buttonStyle" value="Refresh" onclick="refereshResource();"/>\n\t\t\t\t\t\t</td>\n\t\t\t\t\t</tr>\n\t\t\t\t</table>\n\t\t\t\t<div id="resoruceSearchContent" class="searchContent">\t\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t</div>\n\t<script>\n\t\tvar decodedQueueSystemString = $("<div/>").html("')
        __M_writer(escape(c.queueSystemString))
        __M_writer(u'").text();\n\t\tqueueSystemString = eval(\'(\' + decodedQueueSystemString + \')\');\n\t\t\n\t\tinitializeForm();\n\t</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 5, "35": 9, "41": 3, "45": 3, "51": 7, "56": 7, "57": 8, "58": 8, "64": 11, "69": 11, "70": 42, "71": 43, "72": 43, "73": 43, "74": 43, "75": 43, "76": 45, "77": 61, "78": 61, "84": 78}, "uri": "/admin/Resource.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/admin/Resource.mako"}
__M_END_METADATA
"""
