# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1468538751.104963
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/settings.mako'
_template_uri = '/account/settings.mako'
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
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col2main(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n        <script type="text/javascript">\n\t\tfunction getResult(data) {\n\t\t\t$(\'#messageCenter\').show(\'slow\');\n\t\t\tvar messageCenter = document.getElementById("messageCenter");\n\t\t\tmyData = eval("(" + data + ")");\n\t\t\tvar isError = myData[\'Error\'];\n\t\t\tvar message = myData[\'Message\'];\n\t\t\tmessageCenter.innerHTML = message;\n\t\t\tif(isError.toUpperCase() == \'TRUE\') {\n\t\t\t\tmessageCenter.className = \'errorConsole\';\n\t\t\t} else {\n\t\t\t\tmessageCenter.className = \'messageConsole\';\n\t\t\t}\n\t\t\tsetTimeout("$(\'#messageCenter\').hide(\'slow\');",10000);\n\t\t}\n\t</script>\n\t\n  <style type="text/css">\n  \t.errorConsole {\n  \t\tmargin: 0.5em;\n  \t\tcolor: red;\n  \t\tfont-weight: bold;\n  \t}\n  \t.messageConsole {\n  \t\tmargin: 0.5em;\n  \t\tcolor: green;\n  \t\tfont-weight: bold;\n  \t}\n    .prefbutton {\n      margin:0 10px 0 10px;\n      display:inline;\n    }\n    .prefbuttons {\n      width: 190px;\n      margin: 0 auto;\n      text-align: center;\n    }\n    .prefheader {\n      float:left;\n      width: 130px;\n      text-align: right;\n      color: grey;\n      font-weight: bold;\n      margin: 5px 0 5px 0;\n    }\n    .prefvalue {\n      float:left;\n      padding-left:15px;\n      width: 323px;\n      margin: 5px 0 5px 0;\n    }\n    .prefbar {\n      background:#cccccc;\n      padding-left:15px;\n      margin-bottom:7px;\n    }\n  </style>\n\n  <div style="width:500px">\n  <h2>Change your personal information.</h2>\n  <br>\n  <p>\n  <form name="dataForm" method="POST" action="">\n  <div class="prefbar">User Information</div>\n  <div id="accounttable">\n')
        for k,v in c.account.items():
            __M_writer(u'        <div id="')
            __M_writer(escape(k))
            __M_writer(u'" class="prefrow">\n          <div class="prefheader">')
            __M_writer(escape(k))
            __M_writer(u':</div>\n')
            if k == 'password':
                __M_writer(u'            <div class="prefvalue"><input type="password" name="')
                __M_writer(escape(k))
                __M_writer(u'" value="')
                __M_writer(escape(v))
                __M_writer(u'"/></div>\n')
            else:
                __M_writer(u'            <div class="prefvalue"><input type="text" name="')
                __M_writer(escape(k))
                __M_writer(u'" value="')
                __M_writer(escape(v))
                __M_writer(u'"/></div>\n')
            __M_writer(u'        </div>\n        <div class="clear"></div>\n')
        __M_writer(u'  </div>\n')
        if c.message:
            __M_writer(u'    <div id="status" class="prefrow">\n    <div class="prefbuttons">\n')
            if c.error:
                __M_writer(u'      <font color="red">')
                __M_writer(escape(c.message))
                __M_writer(u'</font>\n')
            else:
                __M_writer(u'      <font color="green">')
                __M_writer(escape(c.message))
                __M_writer(u'</font>\n')
            __M_writer(u'    </div>\n    </div>\n')
        __M_writer(u'\n  <br>\n  <div class="prefbuttons">\n    <div id="savebutton" class="prefbutton"><a href="#" onClick="document.dataForm.submit()">Save User Information</a></div>\n    <div id="cancelbutton" class="prefbutton"><a href="#" onClick="document.dataForm.clear()">Cancel</a></div>\n  </div>\n  <div class="clear"></div>\n  </form>\n\n  <!-- <br><br>\n  <form name="prefForm" method="POST" action="">\n  <div class="prefbar">CyberWeb Preferences</div>\n')
        if c.devmessage:
            __M_writer(u'     &nbsp;&nbsp;&nbsp;(')
            __M_writer(escape(c.devmessage))
            __M_writer(u')\n')
        __M_writer(u'  <div id="preftable">\n')
        for k,v in c.pref.items():
            __M_writer(u'        <div id="')
            __M_writer(escape(k))
            __M_writer(u'" class="prefrow">\n          <div class="prefheader">')
            __M_writer(escape(k))
            __M_writer(u':</div>\n')
            if k == 'password':
                __M_writer(u'            <div class="prefvalue"><input type="password" name="')
                __M_writer(escape(k))
                __M_writer(u'" value="')
                __M_writer(escape(v))
                __M_writer(u'"/></div>\n')
            else:
                __M_writer(u'            <div class="prefvalue"><input type="text" name="')
                __M_writer(escape(k))
                __M_writer(u'" value="')
                __M_writer(escape(v))
                __M_writer(u'"/></div>\n')
            __M_writer(u'        </div>\n        <div class="clear"></div>\n')
        __M_writer(u'  </div>\n')
        if c.message:
            __M_writer(u'    <div id="status" class="prefrow">\n    <div class="prefbuttons">\n')
            if c.error:
                __M_writer(u'      <font color="red">')
                __M_writer(escape(c.message))
                __M_writer(u'</font>\n')
            else:
                __M_writer(u'      <font color="green">')
                __M_writer(escape(c.message))
                __M_writer(u'</font>\n')
            __M_writer(u'    </div>\n    </div>\n')
        __M_writer(u'\n  <br>\n  <div class="prefbuttons">\n    <div id="savebutton" class="prefbutton"><a href="#" onClick="document.prefForm.submit()">Save Preferences</a></div>\n    <div id="cancelbutton" class="prefbutton"><a href="#" onClick="document.prefForm.clear()">Cancel</a></div>\n  </div>\n  <div class="clear"></div>\n  </form> -->\n\n  </div>\n  <br><br>\n  <div class="prefbar">Login Statistics</div>\n  <div id="infotable">\n')
        for k,v in c.info.items():
            __M_writer(u'        <div class="prefrow">\n          <div class="prefheader">')
            __M_writer(escape(k))
            __M_writer(u'</div>\n          <div class="prefvalue">')
            __M_writer(escape(v))
            __M_writer(u'</div>\n        </div>\n        <div class="clear"></div>\n')
        __M_writer(u'  </div>\n\n  </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"128": 150, "129": 150, "130": 151, "131": 151, "132": 155, "138": 132, "28": 0, "33": 1, "34": 4, "35": 158, "41": 3, "45": 3, "51": 6, "56": 6, "57": 73, "58": 74, "59": 74, "60": 74, "61": 75, "62": 75, "63": 76, "64": 77, "65": 77, "66": 77, "67": 77, "68": 77, "69": 78, "70": 79, "71": 79, "72": 79, "73": 79, "74": 79, "75": 81, "76": 84, "77": 85, "78": 86, "79": 88, "80": 89, "81": 89, "82": 89, "83": 90, "84": 91, "85": 91, "86": 91, "87": 93, "88": 96, "89": 108, "90": 109, "91": 109, "92": 109, "93": 111, "94": 112, "95": 113, "96": 113, "97": 113, "98": 114, "99": 114, "100": 115, "101": 116, "102": 116, "103": 116, "104": 116, "105": 116, "106": 117, "107": 118, "108": 118, "109": 118, "110": 118, "111": 118, "112": 120, "113": 123, "114": 124, "115": 125, "116": 127, "117": 128, "118": 128, "119": 128, "120": 129, "121": 130, "122": 130, "123": 130, "124": 132, "125": 135, "126": 148, "127": 149}, "uri": "/account/settings.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/settings.mako"}
__M_END_METADATA
"""
