# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1468441324.403918
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/gcem/gccom/app_demo.mako'
_template_uri = '/gcem/gccom/app_demo.mako'
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
            __M_writer(u"</h3>\n   <form action='/gccom/app_jobs_action' method='post'>\n   <input type='submit' name='app_jobs_action' value='Exec GCEM Job' >\n   <table width=100% border=0 bordercolor='white'>\n     <tr width=100% align=left  valign=top>\n               <td width=250 valign=top align=left bgcolor='#9999cc' >\n                 <h3>Job Information:</h3>\n               </td>\n               <td valign=top align=left bgcolor='#9999cc'>\n                     Note: Parameters can only be modified for Test cases, and requires a GCEM account.\n               </td> \n            </tr>\n            <tr align=left valign=top>\n               <td width=250 valign=top align=left >\n                   <h3>Job Name: </h3>\n                   You can create a unique name\n               </td>\n               <td valign=top align=left >\n                   DATE_TIME_CyberWebJobID_<input type='text' name='jobname' value='")
            __M_writer(escape(c.jobname))
            __M_writer(u'\'>\n                   <br>The system will include the DATE+TIME+JobID to the jobname after submission.\n               </td>\n            </tr>\n            <tr align=left valign=top>\n               <td width=200 valign=top align=left >\n                   <h3>Job Decription:</h3> Include custom description or comments: </h3>\n               </td>\n               <td valign=top align=left >\n                   <textarea name="jobdescription" class="html-text-box">GCEM ')
            __M_writer(escape(c.model_key))
            __M_writer(u' ')
            __M_writer(escape(c.mode))
            __M_writer(u'  Case: fixed parameters.  </textarea>\n               </td>\n            </tr>\n            <tr>\n               <td valign=top align=left >\n                   <h3>Select Host:<h3>\n               </td>\n               ')

            cnt=0
            
            
            __M_writer(u'\n               <td valign=top align=left >\n')
            if  len(c.resources.items()) == 0: 
                __M_writer(u' \t\t \tYou currently have SSH connected resources.<br>\n         \t\tTo add compute resource accounts, see MyCyberWeb-->Authentication.\n')
            else:
                for r_id, r in c.resources.items():
                    __M_writer(u'                          ')
                    checked = "checked" if cnt == 0 else "" 
                    
                    __M_writer(u"\n                          <input type='radio' name='hostname' value='")
                    __M_writer(escape(r_id))
                    __M_writer(u"' ")
                    __M_writer(escape(checked))
                    __M_writer(u'>&nbsp;&nbsp;&nbsp;')
                    __M_writer(escape(r['hostname']))
                    __M_writer(u'<br>\n\t\t\t  ')

                    cnt=cnt+1
                                              
                    
                    __M_writer(u'\n')
            __M_writer(u'      </td>\n   </tr>\n            <tr align=left valign=top>\n               <td width=200 valign=top align=left >\n                   <h3>Job Details: </h3>\n               </td>\n               <td valign=top align=left >\n                  <b>Grid Name: </b> ')
            __M_writer(escape(c.grid_name))
            __M_writer(u' <br>\n                  <b>Grid Dimensions:</b> [IMax,JMax,KMax] = [')
            __M_writer(escape(c.grid_imax))
            __M_writer(u', ')
            __M_writer(escape(c.grid_jmax))
            __M_writer(u',')
            __M_writer(escape(c.grid_kmax))
            __M_writer(u"] \n               </td>\n            </tr>\n   <tr> \n      <td colspan=2 align=left valign=top >\n         <table width=100% align=center>\n           <tr bgcolor='#9999cc'>\n               <td colspan=3 >\n                   <h3>Parameter List:</h3> Note: All parameters can be modified for the Test cases.\n               </td> \n            </tr>\n            ")

            p = c.model_params
                         
            
            __M_writer(u'\n')
            if len(p):
                __M_writer(u"           <tr bgcolor='#ffffcc'>\n")
                for i in c.model_param_hdrs:
                    __M_writer(u'               <th>')
                    __M_writer(escape(i))
                    __M_writer(u'</th>\n')
                for r in p:
                    __M_writer(u'               <tr>\n                 <th>')
                    __M_writer(escape(r[0]))
                    __M_writer(u'</th>\n                 <td>')
                    __M_writer(escape(r[1]))
                    __M_writer(u'</td>\n                 <td> <input type="text" readonly="readonly" name="')
                    __M_writer(escape(r[0]))
                    __M_writer(u'.paramval" value="')
                    __M_writer(escape(r[2]))
                    __M_writer(u'"></td>\n               </tr>\n')
                __M_writer(u'            </td>\n            </tr>\n          </table>\n       <tr>\n       <td colspan=3  align=center><p>\n            <input type="submit" name="app_jobs_action" value="Exec GCEM Job" />\n       </td>\n       </tr>\n   </table>\n       <input type="hidden" name="mode"         value="')
                __M_writer(escape(c.mode))
                __M_writer(u'" >\n       <input type="hidden" name="model_key"    value="')
                __M_writer(escape(c.model_key))
                __M_writer(u'" >\n       <input type="hidden" name="model_params" value="')
                __M_writer(escape(c.model_params))
                __M_writer(u'" >\n       <input type="hidden" name="model_desc"   value="')
                __M_writer(escape(c.model_desc))
                __M_writer(u'" >\n       <input type="hidden" name="jobstate"     value="submit" >\n   </form>\n')
            else:
                __M_writer(u'           No Application Available.<br>\n')
        elif c.jobstate == 'submitted' :
            __M_writer(u'<h3>jobstate: ')
            __M_writer(escape(c.jobstate))
            __M_writer(u'</h3>\n   <h3>GCEM Job Submission Successful for ')
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
            __M_writer(u'   </table>\n   <form action="/gccom/jobmonitor" method="post">\n       <input type="hidden" name="mode"        value="')
            __M_writer(escape(c.mode))
            __M_writer(u'" >\n       <input type="hidden" name="jobid"        value="')
            __M_writer(escape(c.jobid))
            __M_writer(u'" >\n       <input type="hidden" name="jobname"      value="')
            __M_writer(escape(c.jobname))
            __M_writer(u'" >\n       <input type="hidden" name="model_key"    value="')
            __M_writer(escape(c.model_key))
            __M_writer(u'" >\n       <input type="hidden" name="model_params" value="')
            __M_writer(escape(c.model_params))
            __M_writer(u'" >\n       <input type="hidden" name="jobstate"     value="monitor" >\n       <input type="submit" name="app_jobs_action" value="Monitor Jobs" />\n   </form>\n\n')
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
{"source_encoding": "utf-8", "line_map": {"28": 0, "33": 1, "34": 162, "40": 3, "46": 3, "47": 4, "48": 5, "49": 5, "50": 5, "51": 6, "52": 6, "53": 7, "54": 7, "55": 8, "56": 8, "57": 9, "58": 9, "59": 10, "60": 11, "61": 11, "62": 11, "63": 12, "64": 12, "65": 30, "66": 30, "67": 39, "68": 39, "69": 39, "70": 39, "71": 46, "75": 48, "76": 50, "77": 51, "78": 53, "79": 54, "80": 55, "81": 55, "83": 55, "84": 56, "85": 56, "86": 56, "87": 56, "88": 56, "89": 56, "90": 57, "94": 59, "95": 62, "96": 69, "97": 69, "98": 70, "99": 70, "100": 70, "101": 70, "102": 70, "103": 70, "104": 81, "108": 83, "109": 84, "110": 85, "111": 86, "112": 87, "113": 87, "114": 87, "115": 89, "116": 90, "117": 91, "118": 91, "119": 92, "120": 92, "121": 93, "122": 93, "123": 93, "124": 93, "125": 96, "126": 105, "127": 105, "128": 106, "129": 106, "130": 107, "131": 107, "132": 108, "133": 108, "134": 111, "135": 112, "136": 114, "137": 115, "138": 115, "139": 115, "140": 116, "141": 116, "142": 116, "143": 116, "144": 118, "145": 118, "146": 119, "147": 119, "148": 120, "149": 120, "150": 121, "151": 121, "152": 122, "153": 122, "154": 124, "155": 124, "156": 124, "157": 124, "158": 124, "159": 124, "160": 125, "161": 125, "162": 126, "163": 126, "164": 127, "165": 127, "166": 132, "167": 133, "168": 133, "169": 133, "170": 135, "171": 136, "172": 137, "173": 138, "174": 139, "175": 139, "176": 139, "177": 141, "178": 143, "179": 145, "180": 145, "181": 146, "182": 146, "183": 147, "184": 147, "185": 148, "186": 148, "187": 149, "188": 149, "189": 154, "190": 155, "191": 156, "192": 156, "193": 157, "194": 157, "195": 158, "196": 158, "197": 159, "198": 159, "199": 161, "205": 199}, "uri": "/gcem/gccom/app_demo.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/gcem/gccom/app_demo.mako"}
__M_END_METADATA
"""
