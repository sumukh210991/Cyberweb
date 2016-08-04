# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467227219.283865
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/postjob/index.mako'
_template_uri = '/postjob/index.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headtags', 'footer', 'header']


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
    return runtime._inherit_from(context, u'/layout.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        dict = context.get('dict', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n\n\n')

        # Python code to manipulate file/directory names for javascript var names
        import re
        varre = re.compile("\.|\(|\)| ")
        
        listing = {'left': dict(), 'right': dict()}
        listarr = {'left': [], 'right': []}
        listvar = {'left': dict(), 'right': dict()}
        dirvar = {'left': dict(), 'right': dict()}
        host = {'left': '', 'right': ''}
        path = {'left': '', 'right': ''}
        
        for box in ['left','right']:
            if len(c.data.get(box)):
                    host[box] = c.data.get(box).get('host')
                    path[box] = c.data.get(box).get('path')
                    for a in c.data.get(box).get('listing'):
                            name = a[1]
                            listarr[box].append(name)
                            listing[box][name] = a
                            listvar[box][name] = varre.subn('',name)[0]
                            dirvar[box][name] = 1 if a[0] == 'directory' else 0
                    listarr[box].sort()
        if len(session['available_resources'].keys()):
                selecthostStr = 'Choose a Host...'
        else:
                selecthostStr = 'No Resources Available'
        
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['box','a','selecthostStr','name','varre','host','re','dirvar','listvar','listing','path','listarr'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n\n\n<div id="loading">\n\t<p><img src="/images/loading2.gif" class="loading_img"></p>\n</div>\n<div id="graphbrowser">\n<!-- For Loop Browser Box -->\n\t<div>\n  \t\t<div class="machine-browser">\n')
        __M_writer(u'\t\t\t<div class="file-box">\n')
        __M_writer(u'\t\t\t<form name="browserLocation" method="post" action="">\n\t\t\t\t<input type="hidden" name="box" value="')
        __M_writer(escape(box))
        __M_writer(u'" />\n\t\t\t\t<div class="header-text">Host:</div>\n\t\t\t\t<div class="header-input">\n\t\t\t\t<!--<select name="host" onchange="this.form.submit();" >-->\n\t\t\t\t<select name="host" id="host" onchange="select_Host();" >\n\t\t\t\t    <option VALUE="">')
        __M_writer(escape(selecthostStr))
        __M_writer(u'...</option>\n')
        for account_id, resource in session['available_resources'].items():
            __M_writer(u'\t\t\t\t\t\t')

            if  'longboard' in resource['name']:
                            name = 'CyberWeb Home'
                                                            
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['name'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\n')
            if host[box] == account_id:
                __M_writer(u'\t\t\t\t\t\t\t<option VALUE="')
                __M_writer(escape(account_id))
                __M_writer(u'" selected="selected">')
                __M_writer(escape(resource['name']))
                __M_writer(u'</option>\n')
            else:
                __M_writer(u'\t\t\t\t\t\t\t<option VALUE="')
                __M_writer(escape(account_id))
                __M_writer(u'">')
                __M_writer(escape(resource['name']))
                __M_writer(u'</option>\n')
        __M_writer(u'\t\t\t\t</select>\n\t\t\t\t</div>\n\t\t\t\t<br class="clear"/>\n\t\t\t\t<div class="header-text">Directory:</div>\n\t\t\t\t<div class="header-input">\n\t\t\t\t\t<input type="text" size="20" name="path" id="host_path" value="')
        __M_writer(escape(path[box]))
        __M_writer(u'" />\n\t\t\t\t</div>\n\t\t\t\t<div class="header-input">\n\t\t\t\t\t<input id="get_listing_button" type="submit" class="button" value="Go" />\n\t\t\t\t</div>\n\t\t\t\t<br class="clear"/>\n\t\t\t\t<div class="header-text"></div>\n\t\t\t\t\n\t\t\t\t<div id=\'\' class="header-icon" onClick="changedir(\'')
        __M_writer(escape(box))
        __M_writer(u'\',\'..Parent Directory\')"><img src="/images/uponedir.jpg" alt="Go to Parent Directory" /></div>\n\t\t\t\t<div id=\'\' class="header-icon" onClick="changedir(\'')
        __M_writer(escape(box))
        __M_writer(u'\',\'..Home Directory\')"><img src="/images/home.jpg" alt="Go to Home Directory" /></div>\n\t\t\t\t<div id=\'\' class="header-icon" onClick="changedir(\'')
        __M_writer(escape(box))
        __M_writer(u'\',\'..Refresh Listing\')"><img src="/images/refresh2.jpg" alt="Refresh listing" /></div>\t\t\t\t\n\t\t\t\t<!--\n\t\t\t\t<div id=\'\' class="header-icon" onClick="selectItems(\'')
        __M_writer(escape(box))
        __M_writer(u"','")
        __M_writer(escape(box))
        __M_writer(u'sortable\')"><img src="/images/rename.gif"/></div>\t\t\t\t\n\t\t\t\t<div id=\'\' class="header-icon" onClick="download(\'')
        __M_writer(escape(box))
        __M_writer(u"','")
        __M_writer(escape(box))
        __M_writer(u'sortable\')"><img src="/images/move.gif"/></div>\n\t\t\t\t<div id=\'\' class="header-icon" onClick="deletefiles(\'')
        __M_writer(escape(box))
        __M_writer(u"','")
        __M_writer(escape(box))
        __M_writer(u"sortable', '")
        __M_writer(escape(path[box]))
        __M_writer(u'\')"><img src="/images/trash.gif"/></div>\n\t\t\t\t-->\n\t\t\t\t<br class="clear"/>\n\t\t\t</form>\n\t\n\t\t\t<div id="')
        __M_writer(escape(box))
        __M_writer(u'databox" class="dataarea">\n')
        if host[box] != '' and path[box] != '':
            __M_writer(u'\t\t\t\t\t<!--<div style="position: relative;padding: 3px 0 5px 0;border-bottom:dotted 1px grey">\n\t\t\t\t\t\t<div class="detail-check">\n\t\t\t\t\t\t\t<input type="checkbox" id="')
            __M_writer(escape(box))
            __M_writer(u'checkall" onClick="checkAll(this.id, \'')
            __M_writer(escape(box))
            __M_writer(u'sortable\')"/>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t\t<div style="margin-left:7px;width:7px;border:solid white;float:left"></div>\n\t\t\t\t\t\t<div class="detail-name"><h3>Name</h3></div>\n\t\t\t\t\t\t<div class="detail-size"><h3>Size</h3></div>\n\t\t\t\t\t\t<div class="detail-modified"><h3>Modified</h3></div>\n\t\t\t\t\t\t<br class="clear"/>\n\t\t\t\t\t</div>-->\n\t\t\t\t\t<li>\n\t\t\t\t\t\t<div id=\'\'>\n\t\t\t\t\t\t\t<div style="position: relative;">\n\t\t\t\t\t\t\t\t<div style="width:12px;border:solid white;float:left"></div>\n\t\t\t\t\t\t\t\t<div class="detail-icon"><img class="filesprite" src="/images/uparrow.gif"/></div>\n\t\t\t\t\t\t\t\t<div class="detail-name"><a href="#" onClick="changedir(\'')
            __M_writer(escape(box))
            __M_writer(u"','..Parent Directory', '")
            __M_writer(escape(path[box]))
            __M_writer(u'\')">Parent Directory..</a></div>\n\t\t\t\t\t\t\t\t<br class="clear"/>\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</li>\n\t\n')
            __M_writer(u'\t\t\t\t\t<div id="')
            __M_writer(escape(box))
            __M_writer(u'sortable" class="sortable" host="')
            __M_writer(escape(host[box]))
            __M_writer(u'" path="')
            __M_writer(escape(path[box]))
            __M_writer(u'">\n\t\t\t\t\t\t<ul class="fileList">\n')
            for a in listarr[box]:
                if dirvar[box][a] == 1:
                    __M_writer(u'\t\t\t\t\t\t\t\t<li var="')
                    __M_writer(escape(listvar[box][a]))
                    __M_writer(u'" file="')
                    __M_writer(escape(a))
                    __M_writer(u'" host="')
                    __M_writer(escape(host[box]))
                    __M_writer(u'" type="directory">\n\t\t\t\t\t\t\t\t\t<div class="')
                    __M_writer(escape(box))
                    __M_writer(u'drag">\n\t\t\t\t\t\t\t\t\t\t<div style="position: relative;">\n\t\t\t\t\t\t\t\t\t\t\t<div class="detail-check"><!--<input type="checkbox" name="')
                    __M_writer(escape(listvar[box][a]))
                    __M_writer(u'" />--></div>\n\t\t\t\t\t\t\t\t\t\t\t<div class="detail-icon"><img class="filesprite" src="/images/folder.gif"/></div>\n\t\t\t\t\t\t\t\t\t\t\t<div class="detail-name"><a href="#" onClick="changedir(\'')
                    __M_writer(escape(box))
                    __M_writer(u"','")
                    __M_writer(escape(a))
                    __M_writer(u'\')">')
                    __M_writer(escape(a))
                    __M_writer(u'</a></div>\n\t\t\t\t\t\t\t\t\t\t\t<br class="clear"/>\n\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t</li>\n')
                else:
                    __M_writer(u'\t\t\t\t\t\t\t\t<li var="')
                    __M_writer(escape(listvar[box][a]))
                    __M_writer(u'" file="')
                    __M_writer(escape(listing[box][a][1]))
                    __M_writer(u'" host="')
                    __M_writer(escape(host[box]))
                    __M_writer(u'" type="file">\n\t\t\t\t\t\t\t\t\t<div class="')
                    __M_writer(escape(box))
                    __M_writer(u'drag">\n\t\t\t\t\t\t\t\t\t\t<div style="position: relative;">\n\t\t\t\t\t\t\t\t\t\t\t<div class="detail-check"><!--<input type="checkbox" name="')
                    __M_writer(escape(listing[box][a][1]))
                    __M_writer(u'" />--></div>\n\t\t\t\t\t\t\t\t\t\t\t<div class="detail-icon"><img class="filesprite" src="/images/text.gif"/></div>\n\t\t\t\t\t\t\t\t\t\t\t<div class="detail-name" onClick="javascript: return setFileName(this)">')
                    __M_writer(escape(listing[box][a][1]))
                    __M_writer(u'</div>\n\t\t\t\t\t\t\t\t\t\t\t<!--<div class="detail-size">')
                    __M_writer(escape(listing[box][a][3]))
                    __M_writer(u'</div>\n\t\t\t\t\t\t\t\t\t\t\t<div class="detail-modified">')
                    __M_writer(escape(listing[box][a][2]))
                    __M_writer(u'</div>-->\n\t\t\t\t\t\t\t\t\t\t\t<br class="clear"/>\n\t\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t</li>\n')
            __M_writer(u'\t\t\t\t\t\t</ul>\n\t\t\t\t\t</div>\n')
        else:
            __M_writer(u'\t\t\t\t\t<div style="padding:90px;text-align:center;color:grey;">')
            __M_writer(escape(selecthostStr))
            __M_writer(u'</div>\n')
        __M_writer(u'\t\t\t\t<ul>\n\t\t\t</div>\n\t\t\t<div id="select_job_div">\n\t\t\t\t<form class="select_job_form">\n\t\t\t\t\t<input type="hidden" name="job_path" id="job_path" value="')
        __M_writer(escape(path[box]))
        __M_writer(u'" />\n\t\t\t\t\t<input type="hidden" name="script" value="read.job.summary.ssh"/>\n\t\t\t\t\t<input type="hidden" name="file_name" id= "file_name" value=""/>\n')
        for resource,name in session['available_resources'].items():
            __M_writer(u'\t\t\t\t\t\t')

                                                        #if name == 'longboard':
            if  'longboard' in name:
                    name = 'CyberWeb Home'
                                                            
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['name'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\n\t\t\t\t\t\t<input type="hidden" name="host" value="')
            __M_writer(escape(resource))
            __M_writer(u'" />\n')
        __M_writer(u'\t\t\t\t\t<!--<input class="select_job" type="button" name="submit" value="Analyze Job" />-->\n\t\t\t\t\t<!--<input class="image_submit" type="button" name="image_submit" value="Display Image" />-->\n\t\t\t\t\t<!--<input class="create_remote_script" type="button" name="create_remote_script" value="Create Remote Script" />-->\n\t\t\t\t</form>\n\t\t\t</div>\n\t\t\t\n\t\t\t<div id="job_summary">\n\t \t\t\t<!--<img src="images/open.png" alt="open job summary">-->\n\t \t\t\t<h4>Job Summary</h4>\n\t\t\t\t<div id=\'summary\'></div>\n\t\t\t</div>\n\t\t\t\n\t\t\t<div style=\'clear:both\'><br /></div>\n\t\t</div>\n\t \t<div class=\'plot_options\'>\n\t \t\t<form name=\'get_plot_form\' id=\'get_plot_form\' onsubmit="javascript: return false;">\n\t\t\t\t<table class="options_table">\n\t\t\t\t\t<tr id=\'options_table_tr1\'>\n\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t<div id="analysis_types_div">\n\t\t\t\t\t\t\t\t<h3>Analysis Type</h3>\n\t\t\t\t\t\t\t\t<select id="analysisTypes" name="analysisTypes" >\n\t\t\t\t\t\t\t\t\t<option value="" selected>--Select--</option>\n')
        for item in c.plots['analysisTypes']: 
            __M_writer(u'\t\t\t\t\t\t\t\t\t\t<option name="')
            __M_writer(escape(item['label']))
            __M_writer(u'" value="')
            __M_writer(escape(item['name']))
            __M_writer(u'">')
            __M_writer(escape(item['label']))
            __M_writer(u'</option>\n')
        __M_writer(u'\t\t\t\t\t\t\t\t</select>\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t<input type=\'hidden\' id=\'plot_file\' name=\'plot_file\' value=\'\'/>\n\t\t\t\t\t\t\t\t<input type=\'hidden\' id=\'check_selected_job\' name=\'check_selected_job\' value=\'\'/>\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</td>\n\t\t\t\t\t</tr>\n\t\t\t\t</table>\n\t\t\t\t<label id="job_selected"></label>\n\t\t\t\t<label id=\'plot_filename\'></label>\n\t \t\t</form>\n\t \t\t\n\t\t\t<div id="plot_table_wrapper">\n\t\t\t\t<table id="plot_table">\n\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t</table>\n\t\t\t\t<div id=\'movie_holder\'>\n\t\t\t\t\t<!--<embed id="myVideoTag" width="670" height="377" name="plugin" \n\t\t\t\t\t\t\tsrc="" \n\t\t\t\t\t\t\ttype="video" play="false">\n\t\t\t\t\t</embed>\n\t\t\t\t\t-->\n\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t</div>\n\t\t\t</div>\n\t \t</div>\t\n  \t</div>\n </div>\n\n<br>\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headtags(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n\n\t<link rel="stylesheet" type="text/css" href="/css/highslide.css" />\n\n\t<script type="text/javascript" src="/stopwatch.js"></script>\n\t<script type="text/javascript" src="/js/runonload.js"></script>\n\t<script type="text/javascript" src="/js/jquery-ui.js"></script>\n\t<script type="text/javascript" src="/js/jquery.ui.sortable.js"></script>\n    <script type="text/javascript" src="/js/jquery.ui.progressbar.js"></script>\n\t<script type="text/javascript" src="/js/jquery.base64.js"></script>\n\t<script type="text/javascript" src="/js/jquery.base64.min.js"></script>\n\t<script type="text/javascript" src="/js/postjob.js"></script>\n\t<script type="text/javascript" src="/js/highslide.js"></script>\n\t<script type="text/javascript" src="/js/jwplayer.js" ></script>\n\t<script type="text/javascript" src="/js/jwplayer.html5.js" ></script>\n\t<style type=\'text/css\'>\n\t\t.form_table tr, .form_table td{\n\t\t\tborder: none;\n\t\t}\n\t\t\n\t\t#content, #graphbrowser{\n\t\t\tmargin: 0px;\n\t\t}\n\t\n\t\t.dark{\n\t\t\tbackground: none;\n\t\t}\n\t\t\n\t\t.alternate {\n    \t\tbackground-color: none;\n\t\t}\n\t</style>\n\n\t<script type="text/javascript">\n//<![CDATA[\nhs.registerOverlay({\n\thtml: \'<div class="closebutton" onclick="return hs.close(this)" title="Close"></div>\',\n\tposition: \'top right\',\n\tfade: 2 // fading the semi-transparent overlay looks bad in IE\n});\n\n\nhs.graphicsDir = \'../images/\';\nhs.outlinesDir = \'../images/\'\nhs.outlineType = \'rounded-black\';\n//hs.wrapperClassName = \'borderless\';\n//]]>\n</script>\n\t\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footer(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_header(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "37": 2, "38": 3, "39": 55, "40": 58, "41": 61, "42": 66, "73": 93, "74": 105, "75": 107, "76": 108, "77": 108, "78": 113, "79": 113, "80": 114, "81": 115, "82": 115, "89": 118, "90": 119, "91": 120, "92": 120, "93": 120, "94": 120, "95": 120, "96": 121, "97": 122, "98": 122, "99": 122, "100": 122, "101": 122, "102": 125, "103": 130, "104": 130, "105": 138, "106": 138, "107": 139, "108": 139, "109": 140, "110": 140, "111": 142, "112": 142, "113": 142, "114": 142, "115": 143, "116": 143, "117": 143, "118": 143, "119": 144, "120": 144, "121": 144, "122": 144, "123": 144, "124": 144, "125": 149, "126": 149, "127": 150, "128": 151, "129": 153, "130": 153, "131": 153, "132": 153, "133": 166, "134": 166, "135": 166, "136": 166, "137": 173, "138": 173, "139": 173, "140": 173, "141": 173, "142": 173, "143": 173, "144": 175, "145": 176, "146": 177, "147": 177, "148": 177, "149": 177, "150": 177, "151": 177, "152": 177, "153": 178, "154": 178, "155": 180, "156": 180, "157": 182, "158": 182, "159": 182, "160": 182, "161": 182, "162": 182, "163": 187, "164": 188, "165": 188, "166": 188, "167": 188, "168": 188, "169": 188, "170": 188, "171": 189, "172": 189, "173": 191, "174": 191, "175": 193, "176": 193, "177": 194, "178": 194, "179": 195, "180": 195, "181": 202, "182": 204, "183": 205, "184": 205, "185": 205, "186": 207, "187": 211, "188": 211, "189": 214, "190": 215, "191": 215, "199": 219, "200": 220, "201": 220, "202": 222, "203": 245, "204": 246, "205": 246, "206": 246, "207": 246, "208": 246, "209": 246, "210": 246, "211": 248, "217": 5, "221": 5, "227": 60, "231": 60, "237": 57, "241": 57, "247": 241}, "uri": "/postjob/index.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/postjob/index.mako"}
__M_END_METADATA
"""
