# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1468459161.624738
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/admin/ResourceServiceLink.mako'
_template_uri = '/admin/ResourceServiceLink.mako'
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
        __M_writer(u'\n\t<script type="text/javascript" src="/js/admin/resource_service.js"></script>\n\t<style>\n\t\t.header {\n\t\t\twidth: 95%;\n\t\t\tborder-spacing: 5px;\n\t\t\tborder-collapse:separate;\n\t\t\tmargin: 0px;\n\t\t}\n\t\t\n\t\t.header td {\n\t\t\tbackground-color: #CCCCCC !important;\n\t\t\tborder: 0px;\n\t\t\tpadding-top: .5em;\n    \t\tpadding-bottom: .5em;\n\t\t}\n\t\t\n\t\t.clear {\n\t\t\tclear: both;\n\t\t}\n\t\t\n\t\t.resourceList, .serviceList {\n\t\t\tmargin: 10px 3em;\n\t\t}\n\t\t\n\t\t.smallHeader {\n\t\t\twidth: 50px;\n\t\t\tmax-width: 50px;\n\t\t}\n\t\t\n\t\t/*.aviableSevice, .operation, .addedServices {\n\t\t\tfloat: left;\n\t\t}*/\n\t\t\n\t\t#addedServiceList, #availableServiceList {\n\t\t\tmax-width: 150px;\n\t\t\tmin-width: 150px;\n\t\t\tmin-height: 150px;\n\t\t\tmax-height: 150px;\n\t\t}\n\t\t\n\t\t/*.operation {\n\t\t\tvertical-align: middle;\n\t\t\tmargin: 30px 0;\n\t\t\tmin-height: 150px;\n\t\t\tmax-height: 150px;\n\t\t}*/\n\t\t\n\t\t.operation input {\n\t\t\twidth: 30px;\n\t\t\tmargin: 2px;\n\t\t\tfont-weight: bold;\n\t\t}\n\t\t\n\t\t.saveLinks {\n\t\t\ttext-align: center;\n\t\t}\n\t\t\n\t\t.saveLinks a {\n\t\t\ttext-decoration: underline;\n\t\t\tpadding-right: 10px;\n\t\t\tcolor: #0066CC;\n\t\t\tfont-size: 14px;\n\t\t}\n\t\t\n\t\t.textStyle{\n\t\t\tpadding: 10px;\n\t\t}\n\t</style>\n')
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
        __M_writer(u'\n\t<div id="maincontent">\n\t\t<h2>Configure Services to Resource</h2>\n\t\t<div id="step1">\n\t\t\t<table class="header">\n\t\t\t\t<tr>\n\t\t\t\t\t<td class="smallHeader">Step 1.</td>\n\t\t\t\t\t<td> Choose resource to add service </td>\n\t\t\t\t</tr>\n\t\t\t</table>\n\t\t\t<div class="clear resourceList">\n\t\t\t\t<span> Resources: </span>\n\t\t\t\t<select id="resourceList" name="resources">\n\t\t\t\t\t<option value="" selected>Select</option>\n')
        for resource in c.resource:
            __M_writer(u'\t\t\t\t\t<option value="')
            __M_writer(escape(resource.id))
            __M_writer(u'">')
            __M_writer(escape(resource.name))
            __M_writer(u'</option>\n')
        __M_writer(u'\t\t\t\t</select>\n\t\t\t\t<span class="textStyle"> If it is not here, Click <a href="/newadmin/resourceDetails" title="Add Resource">here</a> to add. </span>\n\t\t\t</div>\n\t\t</div>\n\t\t<div id="step2">\n\t\t\t<table class="header">\n\t\t\t\t<tr>\n\t\t\t\t\t<td class="smallHeader">Step 2.</td>\n\t\t\t\t\t<td> Add or Delete Service to Resource </td>\n\t\t\t\t</tr>\n\t\t\t</table>\n\t\t\t<div class="clear">\n\t\t\t\t<div id="resourceServiceLinkTab" class="classTab">\n\t\t\t\t\t<div id="errorConsoleResourceServiceLink" class="errorStyle"></div>\n\t\t\t\t\t<div id="activity_pane_resourceServiceLink">\n\t\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t\t<div id="resourceServiceLinkSearchContent" class="searchContent">\n\t\t\t\t\t\t</div>\n\t\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t</div>\n\t<script>\n\t\tvar decodedServiceString = $("<div/>").html("')
        __M_writer(escape(c.serviceString))
        __M_writer(u'").text();\n\t\tvar decodedProtocolString = $("<div/>").html("')
        __M_writer(escape(c.protocolString))
        __M_writer(u'").text();\n\t\t\n\t\tserviceList = eval(\'(\' + decodedServiceString + \')\');\n\t\tprotocolList = eval(\'(\' + decodedProtocolString + \')\');\n\t</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 72, "35": 76, "41": 3, "45": 3, "51": 74, "56": 74, "57": 75, "58": 75, "64": 78, "69": 78, "70": 92, "71": 93, "72": 93, "73": 93, "74": 93, "75": 93, "76": 95, "77": 124, "78": 124, "79": 125, "80": 125, "86": 80}, "uri": "/admin/ResourceServiceLink.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/admin/ResourceServiceLink.mako"}
__M_END_METADATA
"""
