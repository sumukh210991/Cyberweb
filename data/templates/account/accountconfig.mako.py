# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467226908.100224
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/accountconfig.mako'
_template_uri = '/account/accountconfig.mako'
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
    return runtime._inherit_from(context, u'/account/account.layout.mako', _template_uri)
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
        __M_writer(u'\n\t<script type="text/javascript" src="/js/account/account.js"></script>\n\t\n\t<style>\n\t\t.confirmationStyle {\n\t\t\tcolor: #064F08;\n\t\t\tmargin: 0;\n\t\t\tpadding: 1em;\n\t\t\tfont-weight: bold;\n\t\t}\n\t</style>\n')
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
        __M_writer(u'\n\t<div id="maincontent">\n\t\t<div id="menu">\n\t\t</div>\n\t\t<div id="searchcontainer">\n\t\t\t<div id="accountTab" class="classTab">\n\t\t\t\t<div id="dialog-modal" title="Configure PKI/SSH Passwordless connection to">\n\t\t\t\t\t<h2>Add your key</h2>\n\t\t\t\t\t<br><p>CyberWeb generates a PKI public/private key pair for your CyberWeb user account. To enable access to a CyberWeb resource, you must have a valid user account and password on that resource. CyberWeb will use the username and password for authentication and installation of the PKI credential onto the remote host. The password is not stored or saved by CyberWeb.</p>\n\t\t\t\t\t<p>Note: If your account on the remote resource is not ready, this step can be done at a later time - just click on the cancel button.</p>\n\t\t\t\t\t<form name="addResource" method="post" action="">\n\t\t\t\t\t  \t<label>Username: </label>\n\t\t\t\t\t  \t<input type="text" name="user" id="sshUserName" value=""/>\n\t\t\t\t\t\t<br/>\n\t\t\t\t\t\t\n\t\t\t\t\t  \t<label>Password: </label>\n\t\t\t\t\t  \t<input type="password" name="password" id="sshPassword" />\n\t\t\t\t\t\t<br/>\n\t\t\t\t\t</form>\n\t\t\t\t</div>\n\t\t\t\t<h2 class="header">Account</h2>\n\t\t\t\t<div id="errorConsoleAccount" class="confirmationStyle"></div>\n\t\t\t\t<div id="activity_pane_account">\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="accountSearchContent" class="searchContent">\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id="opertaionDiv" class="operation">\n\t\t\t\t\t\t<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t</div>\n\t<input type="hidden" id="userCredential" />\n\t<script type="text/javascript">\n\t\tvar decodedResourceString = $("<div/>").html("')
        __M_writer(escape(c.resourceString))
        __M_writer(u'").text();\n\t\t\n\t\tresourceString = eval(\'(\' + decodedResourceString + \')\');\n\t\tuserName = \'')
        __M_writer(escape(c.user))
        __M_writer(u"';\n\t\tuserId = '")
        __M_writer(escape(c.userId))
        __M_writer(u"';\n\t\t\n\t\tinit();\n\t</script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"64": 20, "33": 1, "34": 14, "35": 18, "69": 20, "70": 57, "71": 57, "72": 60, "41": 3, "74": 61, "75": 61, "45": 3, "81": 75, "51": 16, "73": 60, "56": 16, "57": 17, "58": 17, "28": 0}, "uri": "/account/accountconfig.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/accountconfig.mako"}
__M_END_METADATA
"""
