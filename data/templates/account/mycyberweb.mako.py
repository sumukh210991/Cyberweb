# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467226902.691616
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/mycyberweb.mako'
_template_uri = '/account/mycyberweb.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['col1main']


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
    return runtime._inherit_from(context, u'/1col.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_col1main(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        reversed = context.get('reversed', UNDEFINED)
        len = context.get('len', UNDEFINED)
        enumerate = context.get('enumerate', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n  <style type="text/css">\n    .infobar {\n      background:#cccccc;\n      padding-left:2px;\n      margin-bottom:2px;\n    }\n\n    table, td, th {\n      border:1px solid black;\n    }\n    th {\n      vertical-align:top;\n    }\n    td {\n      vertical-align:top;\n    }\n  </style>\n\n<h3>MyCyberWeb:  ')
        __M_writer(escape(c.title))
        __M_writer(u' </h3>\n<hr>\n\n<table width=90%>\n   <tr>\n   <!----------------  LEFT COL  ------------------->\n   <td>\n      <table style="width:350px">\n         <tr style="text-align:top;"> <td>\n            <div class="infobar">My Information</div>\n            <br>Last login: ')
        __M_writer(escape(c.info['Last login']))
        __M_writer(u' &nbsp;&nbsp;\n            <br>from ip address:  ')
        __M_writer(escape(c.info['from']))
        __M_writer(u'\n         </td> </tr>\n         <tr> <td>\n             <div class="infobar">My Groups & Projects</div>\n             No group information available at this time.\n         </td> </tr>\n         <tr> <td>\n            <div class="infobar">My Remote Accounts </div>\n              ')
        l = len(c.user_resources ) 
        
        __M_writer(u'\n              [length(c.user_resources)] = [- ')
        __M_writer(escape(l))
        __M_writer(u' -]  <br>\n              <hr>\n')
        if l == 0 :
            __M_writer(u'                  You currently have no SSH connected resources.<br>\n                  To add compute resource accounts, see MyCyberWeb-->Authentication. \n')
        else:
            for index, item in enumerate(c.user_resources):
                __M_writer(u'                      &nbsp;&nbsp;')
                __M_writer(escape(item['account_name']))
                __M_writer(u'  @ ')
                __M_writer(escape(item['hostname']))
                __M_writer(u' <br>\n')
        __M_writer(u'         </td> </tr>\n         <tr> <td>\n            <div class="infobar">Recent Messages </div>\n')
        if len(c.messages):
            __M_writer(u'               <table>\n                  <tr>\n')
            for j in c.messageheaders:
                __M_writer(u'                        <th>')
                __M_writer(escape(j))
                __M_writer(u'</th>\n')
            __M_writer(u'                  </tr>\n')
            for i in c.messages:
                __M_writer(u'                     <tr>\n')
                for j in c.messageheaders:
                    if i.has_key(j):
                        __M_writer(u'                              <td>')
                        __M_writer(escape(i[j]))
                        __M_writer(u'</td>\n')
                    else:
                        __M_writer(u'                              <td></td>\n')
                __M_writer(u'                     </tr>\n')
            __M_writer(u'               </table>\n')
        else:
            __M_writer(u'                 &nbsp;&nbsp;No messages. \n')
        __M_writer(u'            [More >]\n         </td> </tr>\n      </table>\n   </td>\n\n   <!----------------  RIGHT COL  ------------------->\n   <td>\n      <table>\n      <tr align=left valign=top> <td>\n         <div class="infobar">MyJobs</div>\n      </td></tr>\n      <tr align=left valign=top> <td>\n         <form action="/user" method="post">\n         <input type="submit" name="jobsummary" value="Update Jobs" />\n         </form>\n      </td></tr>\n      <tr align=left valign=top><td>\n            <table>\n               <tr align=left valign=top>\n                  <th>ID</th>\n                  <th>Job Name</th>\n                  <th>Status</th>\n                  <th>Resource</th>\n                  <th>Submit Time</th>\n                  <th>Start Time</th>\n                  <th>End Time</th>\n               </tr>\n')

        sort_on = "Name"
        jsort = [(dict_[sort_on], dict_) for dict_ in c.jobs]
        jsort.sort()
        sorted_jobs = [dict_ for (key, dict_) in jsort]
               ##% for job in c.jobs:
        
        
        __M_writer(u'\n')
        for job in reversed(sorted_jobs):
            __M_writer(u'                  <tr align=center valign=top>\n                  <td>')
            __M_writer(escape(job['ID']))
            __M_writer(u'</td>\n                  <td>')
            __M_writer(escape(job['Name']))
            __M_writer(u'</td>\n                  <td>')
            __M_writer(escape(job['StatusKey']))
            __M_writer(u' </td>\n                  <td>')
            __M_writer(escape(job['Resource']))
            __M_writer(u'</td>\n                  <td>')
            __M_writer(escape(job['Submit Time']))
            __M_writer(u'</td>\n                  <td>')
            __M_writer(escape(job['Start Time']))
            __M_writer(u'</td>\n                  <td>')
            __M_writer(escape(job['End Time']))
            __M_writer(u'</td>\n               </tr>\n')
        __M_writer(u'            </table>\n\n         </td> </tr>\n         <tr align=left valign=top>\n            <td>\n            <div class="infobar">My Resources & Services</div>\n\n      </td> </tr>\n      </table>\n\n\n   <!------- end right column -->\n   </td> </tr>\n   <!------- end main table  ----->\n</table>\n\n')

        sort_on = "Name"
        jsort = [(dict_[sort_on], dict_) for dict_ in c.jobs]
        jsort.sort()
        sorted_jobs = [dict_ for (key, dict_) in jsort]
        
        
        __M_writer(u'\n<hr>\n===========================================================<br>\n')
        for j in reversed(sorted_jobs):
            __M_writer(u'JOB: ')
            __M_writer(escape(j['Name']))
            __M_writer(u' <br>\n')
        __M_writer(u'<hr>\n===========================================================<br>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"128": 148, "129": 150, "135": 129, "28": 0, "33": 2, "34": 152, "40": 4, "48": 4, "49": 23, "50": 23, "51": 33, "52": 33, "53": 34, "54": 34, "55": 42, "57": 42, "58": 43, "59": 43, "60": 45, "61": 46, "62": 48, "63": 49, "64": 50, "65": 50, "66": 50, "67": 50, "68": 50, "69": 53, "70": 56, "71": 57, "72": 59, "73": 60, "74": 60, "75": 60, "76": 62, "77": 63, "78": 64, "79": 65, "80": 66, "81": 67, "82": 67, "83": 67, "84": 68, "85": 69, "86": 72, "87": 74, "88": 75, "89": 76, "90": 78, "91": 105, "99": 111, "100": 112, "101": 113, "102": 114, "103": 114, "104": 115, "105": 115, "106": 116, "107": 116, "108": 117, "109": 117, "110": 118, "111": 118, "112": 119, "113": 119, "114": 120, "115": 120, "116": 123, "117": 139, "124": 144, "125": 147, "126": 148, "127": 148}, "uri": "/account/mycyberweb.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/account/mycyberweb.mako"}
__M_END_METADATA
"""
