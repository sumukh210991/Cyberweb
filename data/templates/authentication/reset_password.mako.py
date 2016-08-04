# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1465687803.470334
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/reset_password.mako'
_template_uri = '/authentication/reset_password.mako'
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
    return runtime._inherit_from(context, u'/authentication/authentication.layout.mako', _template_uri)
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
        __M_writer = context.writer()
        __M_writer(u'\n\n\t<script type="text/javascript">\n\t\tfunction changePassword() {\n\t\t\tvar messageCenter = document.getElementById("messageCenter");\n\t\t\tvar newpassword = document.getElementById("newpassword");\n\t\t\tvar newconfirmpassword = document.getElementById("newconfirmpassword");\n\t\t\t\n\t\t\tif(newpassword.value == newconfirmpassword.value) {\n\t\t\t\t$.post(\'/authentication/changePassword\',$(\'#prefbar\').serialize(),getResult);\n\t\t\t} else {\n\t\t\t\tmessageCenter.innerHTML = "New Password and Confirmation Password do not match.";\n\t\t\t\tmessageCenter.className = \'errorConsole\';\n\t\t\t\tsetTimeout("$(\'#messageCenter\').hide(\'slow\');",10000);\n\t\t\t}\n\t\t}\n\t\t\n\t\tfunction getResult(data) {\n\t\t\t$(\'#messageCenter\').show(\'slow\');\n\t\t\tvar messageCenter = document.getElementById("messageCenter");\n\t\t\tmyData = eval("(" + data + ")");\n\t\t\tvar isError = myData[\'Error\'];\n\t\t\tvar message = myData[\'Message\'];\n\t\t\tmessageCenter.innerHTML = message;\n\t\t\tif(isError.toUpperCase() == \'TRUE\') {\n\t\t\t\tmessageCenter.className = \'errorConsole\';\n\t\t\t} else {\n\t\t\t\tmessageCenter.className = \'messageConsole\';\n\t\t\t}\n\t\t\tsetTimeout("$(\'#messageCenter\').hide(\'slow\');",10000);\n\t\t}\n\t</script>\n\t\n  <style type="text/css">\n  \t.errorConsole {\n  \t\tmargin: 0.5em;\n  \t\tcolor: red;\n  \t\tfont-weight: bold;\n  \t}\n  \t.messageConsole {\n  \t\tmargin: 0.5em;\n  \t\tcolor: green;\n  \t\tfont-weight: bold;\n  \t}\n    .prefbutton {\n      margin:0 10px 0 10px;\n      display:inline;\n    }\n    .prefbuttons {\n      width: 190px;\n      margin: 0 auto;\n      text-align: center;\n    }\n    .prefheader {\n      float:left;\n      width: 130px;\n      text-align: right;\n      color: grey;\n      font-weight: bold;\n      margin: 5px 0 5px 0;\n    }\n    .prefvalue {\n      float:left;\n      padding-left:15px;\n      width: 323px;\n      margin: 5px 0 5px 0;\n    }\n    .prefbar {\n      background:#cccccc;\n      padding-left:15px;\n      margin-bottom:7px;\n    }\n  </style>\n\n  <div style="width:500px">\n\n  <div class="prefbar">Change Password for CyberWeb User:   ')
        __M_writer(escape(c.account['username']))
        __M_writer(u'</div>\n  \t<div id="messageCenter"></div>\n  \t<form id="prefbar" name="prefbar" mathod="POST" action="">\n  \t\t<div id="oldpasswordDiv" class="prefrow">\n\t\t\t<div class="prefheader">Old Password:</div><div class="prefvalue"><input type="password" \n                             id="oldpassword" name="oldpassword" value=""/></div>\n\t\t</div>\n\t\t<div id="newpasswordDiv" class="prefrow">\n\t\t\t<div class="prefheader">New Password:</div><div class="prefvalue"><input type="password" \n                             id="newpassword" name="newpassword" value=""/></div>\n\t\t</div>\n\t\t<div id="newconfirmpasswordDiv" class="prefrow">\n\t\t\t<div class="prefheader">Confirm Password:</div><div class="prefvalue"><input type="password" \n                             id="newconfirmpassword" name="newconfirmpassword" value=""/></div>\n\t\t</div>\n\t\t\n\t\t<br>\n\t\t<div class="prefbuttons">\n    \t\t<div id="savebutton" class="prefbutton"><a href="#" onClick="changePassword();">Save Password</a></div>\n    \t\t<div id="cancelbutton" class="prefbutton"><a href="#" onClick="document.prefbar.clear();">Cancel</a></div>\n  \t\t</div>\n\t</form>\n  </div>\n  <br><br>\n\n  </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"64": 58, "33": 1, "34": 4, "35": 108, "41": 3, "45": 3, "51": 6, "56": 6, "57": 82, "58": 82, "28": 0}, "uri": "/authentication/reset_password.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/reset_password.mako"}
__M_END_METADATA
"""
