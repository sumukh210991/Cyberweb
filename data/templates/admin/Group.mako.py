# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467226839.601848
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/admin/Group.mako'
_template_uri = '/admin/Group.mako'
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
        __M_writer(u'\n\t<script type="text/javascript" src="/js/admin/group.js"></script>\n\t<style>\n\t\t.passwordTable {\n\t\t\twidth: 100%;\n\t\t}\n\t\t\n\t\t.passwordTable td{\n\t\t\tborder: 0px;\n\t\t\ttext-align: left;\n\t\t}\n\t\t\n\t\t.rightLable {\n\t\t\ttext-align: right !important;\n\t\t}\n\t</style>\n')
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
        __M_writer(u'\n\t<div id="maincontent">\n\t\t<div id="menu">\n\t\t\t<ul id="menuList">\n\t\t\t\t<li id="userLi" class="selected" onclick="switchTabs(this);">User</li>\n\t\t\t\t<li id="groupLi" onclick="switchTabs(this);">Group</li>\n\t\t\t\t<li id="userGroupLi" onclick="switchTabs(this);">User group</li>\n\t\t\t</ul>\n\t\t</div>\n\t\t<div id="searchcontainer">\n\t\t\t<div id="userTab" class="classTab">\n\t\t\t\t<div id="dialog-modal" title="Set Password">\n\t\t\t\t\t<h2>Set or Change Password</h2>\n\t\t\t\t\t<br>Please set or change password. if you do not wish to modify it, please click cancel.\n\t\t\t\t\t<form name="changePassword" method="post" action="">\n\t\t\t\t\t\t<table class="passwordTable">\n\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t<td class="rightLable"><label>Password: </label>\n\t\t\t\t\t\t\t\t<td><input type="password" name="pass" id="password" value=""/></td>\n\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t<td class="rightLable"><label>Confirm Password: </label>\n\t\t\t\t\t\t\t\t<td><input type="password" name="confPass" id="confirmPassword" value=""/></td>\n\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t</table>\n\t\t\t\t\t</form>\n\t\t\t\t\t<input type="hidden" id="passwordField" />\n\t\t\t\t</div>\n\t\t\t\t<h2 class="header">Users</h2>\n\t\t\t\t<div id="errorConsoleUsers" class="errorStyle"></div>\n\t\t\t\t<div id="activity_pane_users">\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="userSearchContent" class="searchContent">\t\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t\t<div id="groupTab" class="classTab">\n\t\t\t\t<h2 class="header">Groups</h2>\n\t\t\t\t<div id="errorConsoleGroups" class="errorStyle"></div>\n\t\t\t\t<div id="activity_pane_groups">\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="groupSearchContent" class="searchContent">\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t\t<div id="userGroupTab" class="classTab">\n\t\t\t\t<h2 class="header">User Group Association</h2>\n\t\t\t\t<div id="errorConsoleUsersGroups" class="errorStyle"></div>\n\t\t\t\t<div id="activity_pane_users_groups">\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="userGroupSearchContent" class="searchContent">\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t</div>\n\t<script type="text/javascript">\n\t\tvar decodedUserString = $("<div/>").html("')
        __M_writer(escape(c.userString))
        __M_writer(u'").text();\n\t\tvar decodedGroupString = $("<div/>").html("')
        __M_writer(escape(c.groupString))
        __M_writer(u'").text();\n\t\t\n\t\tuserString = eval(\'(\' + decodedUserString + \')\');\n\t\tgroupString = eval(\'(\' + decodedGroupString + \')\');\n\t\t\n\t\tinit();\n\t</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"64": 25, "33": 1, "34": 19, "35": 23, "69": 25, "70": 97, "71": 97, "72": 98, "41": 3, "45": 3, "79": 73, "51": 21, "73": 98, "56": 21, "57": 22, "58": 22, "28": 0}, "uri": "/admin/Group.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/admin/Group.mako"}
__M_END_METADATA
"""
