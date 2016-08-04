# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1465693280.857689
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/gcem/gccom/app_test.mako'
_template_uri = '/gcem/gccom/app_test.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['col2main']


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
    return runtime._inherit_from(context, u'/gcem/gcem.layout.2col.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col2main(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if "error" in c.jobstate  :
            __M_writer(u'   MSG: ')
            __M_writer(escape(c.jobmsg))
            __M_writer(u'<p>\n   model_key: ')
            __M_writer(escape(c.model_key))
            __M_writer(u'<p>\n   mode: ')
            __M_writer(escape(c.mode))
            __M_writer(u'<p>\n   jobstate: ')
            __M_writer(escape(c.jobstate))
            __M_writer(u'<p>\n   jobname: ')
            __M_writer(escape(c.jobname))
            __M_writer(u'<p>\n')
        elif c.jobstate == 'build' :
            __M_writer(u'   <h3> ')
            __M_writer(escape(c.title))
            __M_writer(u'</h3>\n   <h3 style="color:red">')
            __M_writer(escape(c.error_flash))
            __M_writer(u'</h3>\n   <form action=\'/gccom/app_jobs_action\' method=\'post\'>\n   <input type=\'submit\' name=\'app_jobs_action\' value=\'Exec GCEM Job\' >\n   <table width=100% border=0 bordercolor=\'white\'>\n     <tr width=100% align=left  valign=top>\n               <td  colspan=2 valign=top align=left bgcolor=\'#9999cc\'>\n                 <h3>Job Information:</h3>\n                     Note: Parameters can <em>only</em> be modified for the <b>Test</b> cases.\n               </td> \n            </tr>\n            <tr align=left valign=top>\n               <td width=200 valign=top align=left >\n                   <h3>Job Name: </h3>\n               </td>\n               <td valign=top align=left >\n                   <input type=\'text\' readonly="readonly"  name=\'jobname\' value=\'')
            __M_writer(escape(c.jobname))
            __M_writer(u'\'>\n                   <br>Note: The Job Name is automatically created for you, but you can edit/change this.\n                         The system will include the DATE+TIME+JobID to the jobname.\n               </td>\n            </tr>\n            <tr align=left valign=top>\n               <td valign=top align=left >\n                   <h3>Job Decription/Comments: </h3>\n               </td>\n               <td valign=top align=left >\n                   <textarea name="jobdescription" class="html-text-box">GCEM ')
            __M_writer(escape(c.model_key))
            __M_writer(u' ')
            __M_writer(escape(c.mode))
            __M_writer(u' Case. </textarea>\n               </td>\n            </tr>\n            <tr>\n               <td valign=top align=left >\n                   <h3>Select Host:</h3>\n               </td>\n               <td valign=top align=left >\n')
            for r, v in c.resources.items():
                __M_writer(u"                       <input type='radio' name='hostname' value='")
                __M_writer(escape(r))
                __M_writer(u"'>&nbsp;&nbsp;&nbsp;")
                __M_writer(escape(v['name']))
                __M_writer(u'<br>\n')
            __M_writer(u'               </td>\n            </tr>\n            <tr align=left valign=top>\n               <td width=200 valign=top align=left >\n                   <h3>Job Details: </h3>\n               </td>\n               <td valign=top align=left >\n                  <b>Grid Name: </b> ')
            __M_writer(escape(c.grid_name))
            __M_writer(u' <br>\n                  <b>Grid Dimensions:</b> [IMax,JMax,KMax] = [')
            __M_writer(escape(c.grid_imax))
            __M_writer(u', ')
            __M_writer(escape(c.grid_jmax))
            __M_writer(u',')
            __M_writer(escape(c.grid_kmax))
            __M_writer(u"] \n               </td>\n            </tr>\n   <tr> \n      <td colspan=2 align=left valign=top >\n         <table width=100% align=center>\n           <tr bgcolor='#9999cc'>\n               <td colspan=3 >\n                   <h3>Parameter List:</h3> Note: All parameters can be modified for the Test cases.\n               </td> \n            </tr>\n\n            ")

            p = c.model_params
                         
            
            __M_writer(u'\n')
            if len(p):
                __M_writer(u"\n           <tr bgcolor='#ffffcc'>\n")
                for i in c.model_param_hdrs:
                    __M_writer(u'               <th>')
                    __M_writer(escape(i))
                    __M_writer(u'</th>\n')
                for r in p:
                    __M_writer(u'               <tr>\n                 <th>')
                    __M_writer(escape(r[0]))
                    __M_writer(u'</th>\n                 <td>')
                    __M_writer(escape(r[1]))
                    __M_writer(u'</td>\n                 <td> <input type="text" name="')
                    __M_writer(escape(r[0]))
                    __M_writer(u'.paramval" value="')
                    __M_writer(escape(r[2]))
                    __M_writer(u'"></td>\n               </tr>\n')
                __M_writer(u'            </td>\n            </tr>\n          </table>\n       <tr>\n       <td colspan=3  align=center><p>\n            <input type="submit" name="app_jobs_action" value="Exec GCOM Job" />\n       </td>\n       </tr>\n   </table>\n       <input type="hidden" name="model_desc"   value="')
                __M_writer(escape(c.model_desc))
                __M_writer(u'" >\n       <input type="hidden" name="mode"         value="')
                __M_writer(escape(c.mode))
                __M_writer(u'" >\n       <input type="hidden" name="model_key"    value="')
                __M_writer(escape(c.model_key))
                __M_writer(u'" >\n       <input type="hidden" name="model_params" value="')
                __M_writer(escape(c.model_params))
                __M_writer(u'" >\n       <input type="hidden" name="jobstate"     value="submit" >\n   </form>\n')
            else:
                __M_writer(u'           No Application Available.<br>\n')
        elif c.jobstate == 'submitted' :
            __M_writer(u'<h3>jobstate: ')
            __M_writer(escape(c.jobstate))
            __M_writer(u'</h3>\n   <h3>GCOM Job Submission Successful for ')
            __M_writer(escape(c.model_desc))
            __M_writer(u' ')
            __M_writer(escape(c.mode))
            __M_writer(u' Case:</h3>\n   <table>\n     <tr align="left" valign="top" ><td width="100"><b>GCEM User:</b> </td><td> ')
            __M_writer(escape(c.cwuser))
            __M_writer(u' </td></tr>\n     <tr><td> <b>GCEM Job Title</b>   </td><td> ')
            __M_writer(escape(c.title))
            __M_writer(u'  </td></tr>\n     <tr><td> <b>GCEM User: </b>      </td><td> ')
            __M_writer(escape(c.cwuser))
            __M_writer(u'  </td></tr>\n     <tr><td> <b>GCEM Job Name: </b>  </td><td> ')
            __M_writer(escape(c.jobname))
            __M_writer(u'  </td></tr>\n     <tr><td> <b>Grid Name: </b>      </td><td> ')
            __M_writer(escape(c.grid_name))
            __M_writer(u' </td></tr>\n     <tr><td> <b>Grid Dimensions:</b> </td>\n         <td> [IMax,JMax,KMax] = [')
            __M_writer(escape(c.grid_imax))
            __M_writer(u', ')
            __M_writer(escape(c.grid_jmax))
            __M_writer(u',')
            __M_writer(escape(c.grid_kmax))
            __M_writer(u'] </td></tr>\n     <tr><td> <b>Remote Host:</b>     </td><td> ')
            __M_writer(escape(c.hostname))
            __M_writer(u'  </td></tr>\n     <tr><td><b>JobId:</b>   </td><td>')
            __M_writer(escape(c.jobid))
            __M_writer(u' </td></tr>\n     <tr><td><b>Mode:</b>  </td><td> ')
            __M_writer(escape(c.mode))
            __M_writer(u' </td></tr>\n   </table>\n    </td></tr>\n    <table>\n        <tr>\n')
            for i in c.model_param_hdrs:
                __M_writer(u'               <th>')
                __M_writer(escape(i))
                __M_writer(u'</th>\n')
            __M_writer(u'         </tr>\n')
            for r in c.model_params:
                __M_writer(u'         <tr>\n')
                for k in r:
                    __M_writer(u'                       <td>')
                    __M_writer(escape(k))
                    __M_writer(u'</td>\n')
                __M_writer(u'         </tr>\n')
            __M_writer(u'   </table>\n   <form action="/gccom/jobmonitor" method="post">\n       <input type="hidden" name="jobid"        value="')
            __M_writer(escape(c.jobid))
            __M_writer(u'" >\n       <input type="hidden" name="jobname"      value="')
            __M_writer(escape(c.jobname))
            __M_writer(u'" >\n       <input type="hidden" name="model_key"    value="')
            __M_writer(escape(c.model_key))
            __M_writer(u'" >\n       <input type="hidden" name="model_params" value="')
            __M_writer(escape(c.model_params))
            __M_writer(u'" >\n       <input type="hidden" name="jobstate"     value="monitor" >\n       <input type="submit" name="app_jobs_action" value="Exec GCOM Job" />\n   </form>\n\n')
        else:
            __M_writer(u'   <h3>Problem with Run: %{c.title}</h3>\n   model_key: ')
            __M_writer(escape(c.model_key))
            __M_writer(u'<p>\n   mode: ')
            __M_writer(escape(c.mode))
            __M_writer(u'<p>\n   jobstate: ')
            __M_writer(escape(c.jobstate))
            __M_writer(u'<p>\n   jobname: ')
            __M_writer(escape(c.jobname))
            __M_writer(u'<p>\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 149, "40": 3, "46": 3, "47": 4, "48": 5, "49": 5, "50": 5, "51": 6, "52": 6, "53": 7, "54": 7, "55": 8, "56": 8, "57": 9, "58": 9, "59": 10, "60": 11, "61": 11, "62": 11, "63": 12, "64": 12, "65": 27, "66": 27, "67": 37, "68": 37, "69": 37, "70": 37, "71": 45, "72": 46, "73": 46, "74": 46, "75": 46, "76": 46, "77": 48, "78": 55, "79": 55, "80": 56, "81": 56, "82": 56, "83": 56, "84": 56, "85": 56, "86": 68, "90": 70, "91": 71, "92": 72, "93": 74, "94": 75, "95": 75, "96": 75, "97": 77, "98": 78, "99": 79, "100": 79, "101": 80, "102": 80, "103": 81, "104": 81, "105": 81, "106": 81, "107": 84, "108": 93, "109": 93, "110": 94, "111": 94, "112": 95, "113": 95, "114": 96, "115": 96, "116": 99, "117": 100, "118": 102, "119": 103, "120": 103, "121": 103, "122": 104, "123": 104, "124": 104, "125": 104, "126": 106, "127": 106, "128": 107, "129": 107, "130": 108, "131": 108, "132": 109, "133": 109, "134": 110, "135": 110, "136": 112, "137": 112, "138": 112, "139": 112, "140": 112, "141": 112, "142": 113, "143": 113, "144": 114, "145": 114, "146": 115, "147": 115, "148": 120, "149": 121, "150": 121, "151": 121, "152": 123, "153": 124, "154": 125, "155": 126, "156": 127, "157": 127, "158": 127, "159": 129, "160": 131, "161": 133, "162": 133, "163": 134, "164": 134, "165": 135, "166": 135, "167": 136, "168": 136, "169": 141, "170": 142, "171": 143, "172": 143, "173": 144, "174": 144, "175": 145, "176": 145, "177": 146, "178": 146, "179": 148, "185": 179}, "uri": "/gcem/gccom/app_test.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/gcem/gccom/app_test.mako"}
__M_END_METADATA
"""
