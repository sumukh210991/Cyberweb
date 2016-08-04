# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1468813685.14519
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/admin/Account.mako'
_template_uri = '/admin/Account.mako'
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
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headtags(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n\t<script type="text/javascript" src="/js/admin/account.js"></script>\n')
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
        __M_writer(u'\n\t\n\t<div id="maincontent">\n\t\t<div id="menu">\n\t\t\t<ul id="menuList">\n\t\t\t\t<li id="accountLi" onclick="switchTabs(this);">Accounts</li>\n\t\t\t\t<li id="authkeyLi" class="selected" onclick="switchTabs(this);">Pki Credential</li>\n\t\t\t</ul>\n\t\t</div>\n\t\t<div id="searchcontainer">\n\t\t\t<div id="authKeyTab" class="classTab">\n\t\t\t\t<h2 class="header">Auth Key</h2>\n\t\t\t\t<div id="errorConsoleAuthKey" class="errorStyle"></div>\n\t\t\t\t<div id="activity_pane_authKey">\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="authKeySearchContent" class="searchContent">\t\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t\t<div id="accountTab" class="classTab">\n\t\t\t\t<div id="dialog-modal" title="Configure PKI/SSH Passwordless connection to">\n\t\t\t\t\t<h2>Add your key</h2>\n\t\t\t\t\t<br><p>CyberWeb generates a PKI public/private key pair for your CyberWeb user account. To enable access to a CyberWeb resource, you must have a valid user account and password on that resource. CyberWeb will use the username and password for authentication and installation of the PKI credential onto the remote host. The password is not stored or saved by CyberWeb.</p>\n\t\t\t\t\t<p>Note: If your account on the remote resource is not ready, this step can be done at a later time - just click on the cancel button.</p>\n\t\t\t\t\t<form name="addResource" method="post" action="">\n\t\t\t\t\t  \t<label>Username: </label>\n\t\t\t\t\t  \t<input type="text" name="user" id="sshUserName" value=""/>\n\t\t\t\t\t\t<br/>\n\t\t\t\t\t\t\n\t\t\t\t\t  \t<label>Password: </label>\n\t\t\t\t\t  \t<input type="password" name="password" id="sshPassword" />\n\t\t\t\t\t\t<br/>\n\t\t\t\t\t</form>\n\t\t\t\t</div>\n\t\t\t\t<h2 class="header">Account</h2>\n\t\t\t\t<div id="errorConsoleAccount" class="errorStyle"></div>\n\t\t\t\t<div id="activity_pane_account">\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="accountSearchContent" class="searchContent">\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t</div>\n\t<script type="text/javascript">\n\t\ttabOperationObj.tabList = new Array(document.getElementById(\'accountLi\'),document.getElementById(\'authkeyLi\'));\n\t\ttabOperationObj.tabDivList = new Array(document.getElementById(\'accountTab\'),document.getElementById(\'authKeyTab\'));\n\t\ttabOperationObj.init();\n\t\ttabOperationObj.switchTab(tabOperationObj.tabList[0]);\n\t\t\n\t\taccountAdminObj.setData(accountsData);\n\t\taccountAdminObj.setPopulateData(populateAccountLists);\n\t\taccountAdminObj.setParseResponse(parseAccountResponse);\n\t\taccountAdminObj.activityPane = \'activity_pane_account\';\n\t\t\n\t\tauthKeyAdminObj.setData(authKeyData);\n\t\tauthKeyAdminObj.setPopulateData(populateAuthKeyLists);\n\t\tauthKeyAdminObj.setParseResponse(parseAuthKeyResponse);\n\t\tauthKeyAdminObj.activityPane = \'activity_pane_authKey\';\n\t\t\n\t\taccountAdminObj.getData(\'/newadmin/forwardRequest\',\'method=view&type=account\');\n\t\t\n\t\tvar decodedResourceString = $("<div/>").html("')
        __M_writer(escape(c.resourceString))
        __M_writer(u'").text();\n\t\tvar decodedUserString = $("<div/>").html("')
        __M_writer(escape(c.userString))
        __M_writer(u'").text();\n\t\t\n\t\tresourceString = eval(\'(\' + decodedResourceString + \')\');\n\t\tuserString = eval(\'(\' + decodedUserString + \')\');\n\t\tuserName = \'')
        __M_writer(escape(c.user))
        __M_writer(u"';\n\t</script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"33": 1, "34": 5, "35": 9, "36": 90, "70": 11, "65": 11, "72": 83, "73": 84, "42": 3, "71": 83, "76": 88, "82": 76, "46": 3, "75": 88, "52": 7, "57": 7, "58": 8, "59": 8, "28": 0, "74": 84}, "uri": "/admin/Account.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/admin/Account.mako"}
__M_END_METADATA
"""
