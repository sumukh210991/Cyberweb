# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467226906.483343
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/services.mako'
_template_uri = '/account/services.mako'
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
        __M_writer(u'\n\t<link rel="stylesheet" type="text/css" href="/css/admin.css" media="screen">\n\t<link rel="stylesheet" type="text/css" href="/css/services.css" media="screen">\n\t\n\t<script type="text/javascript" src="/js/account/service.js"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col2main(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<script type="text/javascript">\n    function connect(service){\n        dataString = "service="+service;\n\n        $.ajax({\n            type: "POST",\n            url: "/user/jodis_connect",\n            data: dataString,\n            error: function(){\n                window.location.reload()\n            },\n            success: function(){\n                window.location.reload()\n            }\n        });\n\n        return;\n    };\n</script>\n\n<div class="mainContent">\n\t<h2 class="mainHeading">CyberWeb Information Services</h2> &nbsp;&nbsp;\n\t\n\t<h3>Filter Result:</h3>\n\t<table class="noBorder">\n\t\t<tr>\n\t\t\t<td>Resources:</td>\n\t\t\t<td><select id="filterResources">\n\t\t\t\t\t<option value="Available">Available</option>\n\t\t\t\t\t<option value="All">All</option>\n\t\t\t\t</select>\n\t\t\t</td>\n\t\t</tr>\n\t</table>\n\t<br>\n\t<div id="resoruceList">\n\t</div>\n\t<div style="margin-bottom:40px"></div>\n\t<script>\n\t\tvar decodedResourceString = $("<div/>").html(\'')
        __M_writer(escape(c.resourceServiceJson))
        __M_writer(u"').text();\n\t\tvar resourceService = eval('(' + decodedResourceString + ')');\n\t</script>\n</div>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"64": 58, "33": 1, "34": 8, "35": 54, "41": 3, "45": 3, "51": 10, "56": 10, "57": 50, "58": 50, "28": 0}, "uri": "/account/services.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/services.mako"}
__M_END_METADATA
"""
