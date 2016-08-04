# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1468779400.582552
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/admin/Service.mako'
_template_uri = '/admin/Service.mako'
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
        __M_writer(u'\n\t<script type="text/javascript" src="/js/admin/service.js"></script>\n')
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
        __M_writer(u'\n\t<div id="maincontent">\n\t\t<div id="errorConsole" class="errorStyle"></div>\n\t\t<div id="menu">\n\t\t\t<ul id="menuList">\n\t\t\t\t<li id="serviceTypeLi" class="selected" onclick="switchTabs(this);">Service Type</li>\n\t\t\t\t<li id="serviceNameLi" onclick="switchTabs(this);">Service Name</li>\n\t\t\t\t<li id="serviceLi" onclick="switchTabs(this);">Services</li>\n\t\t\t</ul>\n\t\t</div>\n\t\t<div id="searchcontainer">\n\t\t\t<div id="serviceTypeTab" class="classTab">\n\t\t\t\t<h2 class="header">Service Types</h2>\n\t\t\t\t<div id="errorConsoleServiceType" class="errorStyle"></div>\n\t\t\t\t<div id="activity_pane_serviceType">\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="serviceTypeSearchContent" class="searchContent">\t\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t\t<div id="serviceNameTab" class="classTab">\n\t\t\t\t<h2 class="header">Service Names</h2>\n\t\t\t\t<div id="errorConsoleServiceName" class="errorStyle"></div>\n\t\t\t\t<div id="activity_pane_serviceName">\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="serviceNameSearchContent" class="searchContent">\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t\t<div id="servicesTab" class="classTab">\n\t\t\t\t<table id="searchService">\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td><label>Services</label></td>\n\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t<select id="serviceList" MULTIPLE>\n')
        for service in c.service:
            __M_writer(u'\t\t\t\t\t\t\t\t<option value="')
            __M_writer(escape(service.id))
            __M_writer(u'">')
            __M_writer(escape(service.name))
            __M_writer(u'</option>\n')
        __M_writer(u'\t\t\t\t\t\t\t</select>\n\t\t\t\t\t\t</td>\n\t\t\t\t\t</tr>\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td></td>\n\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t<input type="button" class="buttonStyle" value="Show Resources" onclick="searchServices();"/> <input type="button" class="buttonStyle" value="Refresh" onclick="refereshService();"/>\n\t\t\t\t\t\t</td>\n\t\t\t\t\t</tr>\n\t\t\t\t</table>\n\t\t\t\t<div id="serviceSearchContent" class="searchContent">\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t</div>\n\t<script type="text/javascript">\n\t\tvar decodedServiceTypeString = $("<div/>").html("')
        __M_writer(escape(c.serviceTypeString))
        __M_writer(u'").text();\n\t\tserviceTypeString = eval(\'(\' + decodedServiceTypeString + \')\');\n\t\t\n\t\tinit();\n\t</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 5, "35": 9, "41": 3, "45": 3, "51": 7, "56": 7, "57": 8, "58": 8, "64": 11, "69": 11, "70": 56, "71": 57, "72": 57, "73": 57, "74": 57, "75": 57, "76": 59, "77": 75, "78": 75, "84": 78}, "uri": "/admin/Service.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/admin/Service.mako"}
__M_END_METADATA
"""
