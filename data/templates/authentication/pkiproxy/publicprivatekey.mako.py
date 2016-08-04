# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1468779267.995774
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/pkiproxy/publicprivatekey.mako'
_template_uri = '/authentication/pkiproxy/publicprivatekey.mako'
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
        __M_writer(u'\n\t<style>\n\t\t.errorStyle{\n\t\t\tmargin: 0;\n\t\t\tpadding: 1em;\n\t\t\tcolor: red;\n\t\t\tfont-weight: bold;\n\t\t}\n\t\t\n\t\t.formStyle th, .formStyle td{\n\t\t\tborder: 0;\n\t\t}\n\t\t\n\t\t.label {\n\t\t\ttext-align: right;\n\t\t}\n\t</style>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col2main(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n  <style type="text/css">\n    .prefbutton {\n      margin:0 10px 0 10px;\n      display:inline;\n    }\n    .prefbuttons {\n      width: 190px;\n      margin: 0 auto;\n      text-align: center;\n    }\n    .prefheader {\n      float:left;\n      width: 130px;\n      text-align: right;\n      color: grey;\n      font-weight: bold;\n      margin: 5px 0 5px 0;\n    }\n    .prefvalue {\n      float:left;\n      padding-left:15px;\n      width: 323px;\n      margin: 5px 0 5px 0;\n    }\n    .prefbar {\n      background:#cccccc;\n      padding-left:15px;\n      margin-bottom:7px;\n    }\n  </style>\n\n  <div style="width:500px;">\n  \t<h2>Private/Public Key Authentication.</h2>\n')
        if not c.current_keys:
            __M_writer(u'\t    <br>The public private/key combination allows CyberWeb to SSH to a particular SSH enabled resource\n\t    <p> on behalf of a user. You must already have access to the resource in order to use this feature.\n\t    <p> To get started click the button below and CyberWeb will create a key pair for you.\n\t    <div class="prefbar">Create a new key</div>\n\t    <form name="dataForm" method="POST" action="">\n\t    <div class="prefbuttons">\n\t      <input type="hidden" name="CreateKey" value="True">\n\t      <div id="savebutton" class="prefbutton"><a href="#" onClick="document.dataForm.submit()">Create key pair</a></div>\n\t      <div id="cancelbutton" class="prefbutton"><a href="#" onClick="document.dataForm.clear()">Cancel</a></div>\n\t    </div>\n\t    <div class="clear"></div>\n\t    </form>\n')
        else:
            if c.keymade:
                __M_writer(u'\t      <br><font color="green">You have successfully created a public/private key pair.<p></font>\n')
            __M_writer(u'\t    <p>\n\t    <div class="prefbar">Instructions to add a resource.</div>\n\t    <p>1. Highlight and copy the key below.</p>\n\t    <form name="pubkey" method="post" action="">  \n            <table border=1 style="table-layout:fixed; width:100px">\n')
            for i in c.current_keys:
                __M_writer(u'                    <tr><td style="overflow:hidden; width:500px;WORD-BREAK:BREAK-ALL">\n                        ')
                __M_writer(escape(i.public_key))
                __M_writer(u'\n                    </td></tr>\n')
            __M_writer(u'            </table>\n\t  </form>\n\t    <p>2. Using your current username and password, login to the resource you wish to add.</p>\n\t    <p>3. Paste the key string you copied in Step 1 into the file ~/.ssh/authorized_keys. If this file does not exist, create it.</p>\nC.USERID=  [  ')
            __M_writer(escape(c.user_id))
            __M_writer(u'  ]<br>\n\t    <div id="accounttable">\n\t    </div>\n\t    <br>\n')
        __M_writer(u'\t  <h2>Add your key</h2>\n\t  <form name="addResource" method="post" action="">  \n')
        if c.message:
            __M_writer(u'\t\t\t<div class="errorStyle">\n\t\t\tMessage:\t')
            __M_writer(escape(c.message))
            __M_writer(u'<br/>\n\t\t\t</div>\n')
        __M_writer(u'\t\t<table class="formStyle">\n\t\t\t<tr>\n\t\t\t\t<td class="label"><label>Host: </label></td>\n\t\t\t\t<td><select name="host">\n\t\t\t\t\t    <OPTION VALUE=""></option>\n')
        for resource in c.resources:
            __M_writer(u'\t\t\t\t\t\t\t')

            name = resource.name
            if 'longboard' in resource.name:
                            name = 'CyberWeb Home'
                                                                    
            
            __M_writer(u'\n')
            if c.resource_id == resource.id:
                __M_writer(u'\t\t\t\t\t\t\t\t<OPTION VALUE="')
                __M_writer(escape(resource.id))
                __M_writer(u'" selected="selected">')
                __M_writer(escape(name))
                __M_writer(u'</option>\n')
            else:
                __M_writer(u'\t\t\t\t\t\t\t\t<OPTION VALUE="')
                __M_writer(escape(resource.id))
                __M_writer(u'">')
                __M_writer(escape(name))
                __M_writer(u'</option>\n')
        __M_writer(u'\t\t\t\t\t</select>\n\t\t\t\t</td>\n\t\t\t</tr>\n\t\t\t<tr>\n\t\t\t\t<td class="label"><label>Username: </label></td>\n\t\t\t\t<td><input type="text" name="user" value="')
        __M_writer(escape(c.user))
        __M_writer(u'"/></td>\n\t\t\t</tr>\n\t\t\t<tr>\n\t\t\t\t<td class="label"><label>Password: </label></td>\n\t\t\t\t<td><input type="password" name="password"/></td>\n\t\t\t</tr>\n\t\t\t<tr>\n\t\t\t\t<td></td>\n\t\t\t\t<td><input type="submit" name="submit" /></td>\n\t\t\t</tr>\n\t\t</table>\n\t  </form>\n\t</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 20, "35": 134, "41": 3, "45": 3, "51": 22, "56": 22, "57": 56, "58": 57, "59": 69, "60": 70, "61": 71, "62": 73, "63": 78, "64": 79, "65": 80, "66": 80, "67": 83, "68": 87, "69": 87, "70": 92, "71": 94, "72": 95, "73": 96, "74": 96, "75": 99, "76": 104, "77": 105, "78": 105, "84": 109, "85": 110, "86": 111, "87": 111, "88": 111, "89": 111, "90": 111, "91": 112, "92": 113, "93": 113, "94": 113, "95": 113, "96": 113, "97": 116, "98": 121, "99": 121, "105": 99}, "uri": "/authentication/pkiproxy/publicprivatekey.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/authentication/pkiproxy/publicprivatekey.mako"}
__M_END_METADATA
"""
