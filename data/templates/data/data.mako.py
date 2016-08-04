# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1467227214.548655
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/data/data.mako'
_template_uri = '/data/data.mako'
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
        app_globals = context.get('app_globals', UNDEFINED)
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
        __M_writer(u'\n\n\n\n<div id="browser">\n<!-- For Loop Browser Box -->\n')
        for box in ['left','right']:
            __M_writer(u'    <div class="file-box">\n')
            __M_writer(u'\t\t<form name="browserLocation" method="post" action="">\n\t\t    <input type="hidden" name="box" value="')
            __M_writer(escape(box))
            __M_writer(u'" />\n\t\t    <div class="header-text">Host:</div>\n\t\t    <div class="header-input">\n\t\t\t\t<select name="host" onchange="this.form.submit();">\n\t\t\t\t    <OPTION VALUE="">')
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
                    __M_writer(u'\t\t\t\t\t\t\t<OPTION VALUE="')
                    __M_writer(escape(account_id))
                    __M_writer(u'" selected="selected">')
                    __M_writer(escape(resource['name']))
                    __M_writer(u'</option>\n')
                else:
                    __M_writer(u'\t\t\t\t\t\t\t<OPTION VALUE="')
                    __M_writer(escape(account_id))
                    __M_writer(u'">')
                    __M_writer(escape(resource['name']))
                    __M_writer(u'</option>\n')
            __M_writer(u'\t\t\t\t</select>\n\t\t    </div>\n\t\t    <br class="clear"/>\n')
            if not app_globals.is_community_model:
                __M_writer(u'\t\t    <div class="header-text">Directory:</div>\n\t\t    <div class="header-input">\n\t\t\t\t<input type="text" size="100" name="path" value="')
                __M_writer(escape(path[box]))
                __M_writer(u'" />\n\t\t    </div>\n\t\t    <div class="header-input">\n\t\t\t\t<input type="submit" class="button" value="Go" />\n\t\t    </div>\n')
            __M_writer(u'\t\t    <br class="clear"/>\n\t\t    <div class="header-text"></div>\n\t\t    <div id=\'\' class="header-icon" onClick="changedir(\'')
            __M_writer(escape(box))
            __M_writer(u'\',\'..Parent Directory\')"><img src="/images/uponedir.jpg" alt="Go to Parent Directory" /></div>\n')
            if not app_globals.is_community_model:
                __M_writer(u'\t\t    <div id=\'\' class="header-icon" onClick="changedir(\'')
                __M_writer(escape(box))
                __M_writer(u'\',\'..User Home Directory\')">~</div>\n')
            __M_writer(u'\t\t    <div id=\'\' class="header-icon" onClick="changedir(\'')
            __M_writer(escape(box))
            __M_writer(u'\',\'..Home Directory\')"><img src="/images/home.jpg" alt="Go to Home Directory" /></div>\n\t\t    <div id=\'\' class="header-icon" onClick="changedir(\'')
            __M_writer(escape(box))
            __M_writer(u'\',\'..Refresh Listing\')"><img src="/images/refresh2.jpg" alt="Refresh listing" /></div>\n\t\t\t<!--\n\t\t    <div id=\'\' class="header-icon" onClick="selectItems(\'')
            __M_writer(escape(box))
            __M_writer(u"','")
            __M_writer(escape(box))
            __M_writer(u'sortable\')"><img src="/images/rename.gif"/></div>\n\t\t\t-->\n\t\t    <div id=\'\' class="header-icon" onClick="download(\'')
            __M_writer(escape(box))
            __M_writer(u"','")
            __M_writer(escape(box))
            __M_writer(u'sortable\')"><img src="/images/move.gif"/></div>\n\t\t    <div id=\'\' class="header-icon" onClick="deletefiles(\'')
            __M_writer(escape(box))
            __M_writer(u"','")
            __M_writer(escape(box))
            __M_writer(u"sortable', '")
            __M_writer(escape(path[box]))
            __M_writer(u'\')"><img src="/images/trash.gif"/></div>\n\t\t    <br class="clear"/>\n\t\t</form>\n\n\t\t<div id="')
            __M_writer(escape(box))
            __M_writer(u'databox" class="dataarea">\n')
            if host[box] != '' and path[box] != '':
                __M_writer(u'\t\t\t\t<div style="position: relative;padding: 3px 0 5px 0;border-bottom:dotted 1px grey">\n\t\t\t\t\t<div class="detail-check"><input type="checkbox" id="')
                __M_writer(escape(box))
                __M_writer(u'checkall" onClick="checkAll(this.id, \'')
                __M_writer(escape(box))
                __M_writer(u'sortable\')"/></div>\n\t\t\t        <div style="margin-left:7px;width:7px;border:solid white;float:left"></div>\n\t\t\t\t\t<div class="detail-name"><h3>Name</h3></div>\n\t\t\t\t\t<div class="detail-size"><h3>Size</h3></div>\n\t\t\t\t\t<div class="detail-modified"><h3>Modified</h3></div>\n\t\t\t\t    <br class="clear"/>\n\t\t\t\t</div>\n\t\t\t\t<li>\n\t\t\t\t\t<div id=\'\'>\n\t\t\t\t\t\t<div style="position: relative;">\n\t\t\t\t\t\t\t<div style="width:12px;border:solid white;float:left"></div>\n\t\t\t\t\t\t\t<div class="detail-icon"><img class="filesprite" src="/images/uparrow.gif"/></div>\n\t\t\t\t\t\t\t<div class="detail-name"><a href="#" onClick="changedir(\'')
                __M_writer(escape(box))
                __M_writer(u"','..Parent Directory', '")
                __M_writer(escape(path[box]))
                __M_writer(u'\')">Parent Directory..</a></div>\n\t\t\t\t\t\t\t<br class="clear"/>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t</li>\n\n')
                __M_writer(u'\t\t\t\t<div id="')
                __M_writer(escape(box))
                __M_writer(u'sortable" class="sortable" host="')
                __M_writer(escape(host[box]))
                __M_writer(u'" path="')
                __M_writer(escape(path[box]))
                __M_writer(u'">\n\t\t\t\t\t<ul class="fileList">\n')
                for a in listarr[box]:
                    if dirvar[box][a] == 1:
                        __M_writer(u'\t\t\t\t\t\t\t<li var="')
                        __M_writer(escape(listvar[box][a]))
                        __M_writer(u'" file="')
                        __M_writer(escape(a))
                        __M_writer(u'" host="')
                        __M_writer(escape(host[box]))
                        __M_writer(u'" type="directory">\n\t\t\t\t\t\t\t\t<div class="')
                        __M_writer(escape(box))
                        __M_writer(u'drag">\n\t\t\t\t\t\t\t\t\t<div style="position: relative;">\n\t\t\t\t\t\t\t\t\t\t<div class="detail-check"><input type="checkbox" name="')
                        __M_writer(escape(listvar[box][a]))
                        __M_writer(u'" /></div>\n\t\t\t\t\t\t\t\t\t\t<div class="detail-icon"><img class="filesprite" src="/images/folder.gif"/></div>\n\t\t\t\t\t\t\t\t\t\t<div class="detail-name"><a href="#" onClick="changedir(\'')
                        __M_writer(escape(box))
                        __M_writer(u"','")
                        __M_writer(escape(a))
                        __M_writer(u'\')">')
                        __M_writer(escape(a))
                        __M_writer(u'</a></div>\n\t\t\t\t\t\t\t\t\t\t<br class="clear"/>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t</li>\n')
                    else:
                        __M_writer(u'\t\t\t\t\t\t\t<li var="')
                        __M_writer(escape(listvar[box][a]))
                        __M_writer(u'" file="')
                        __M_writer(escape(listing[box][a][1]))
                        __M_writer(u'" host="')
                        __M_writer(escape(host[box]))
                        __M_writer(u'" type="file">\n\t\t\t\t\t\t\t\t<div class="')
                        __M_writer(escape(box))
                        __M_writer(u'drag">\n\t\t\t\t\t\t\t\t\t<div style="position: relative;">\n\t\t\t\t\t\t\t\t\t\t<div class="detail-check"><input type="checkbox" name="')
                        __M_writer(escape(listing[box][a][1]))
                        __M_writer(u'" /></div>\n\t\t\t\t\t\t\t\t\t\t<div class="detail-icon"><img class="filesprite" src="/images/text.gif"/></div>\n\t\t\t\t\t\t\t\t\t\t<div class="detail-name" onClick="window.open(\'/data/getfile?host=')
                        __M_writer(escape(host[box]))
                        __M_writer(u'&path=')
                        __M_writer(escape(path[box]))
                        __M_writer(u'/')
                        __M_writer(escape(listing[box][a][1]))
                        __M_writer(u"','")
                        __M_writer(escape(listing[box][a][1]))
                        __M_writer(u'\',\'width=400,height=300,toolbar=no,location=no,directories=no,status=no,menubar=no,resizable=yes,scrollbars=yes\')">')
                        __M_writer(escape(listing[box][a][1]))
                        __M_writer(u'</div>\n\t\t\t\t\t\t\t\t\t\t<div class="detail-size">')
                        __M_writer(escape(listing[box][a][3]))
                        __M_writer(u'</div>\n\t\t\t\t\t\t\t\t\t\t<div class="detail-modified">')
                        __M_writer(escape(listing[box][a][2]))
                        __M_writer(u'</div>\n\t\t\t\t\t\t\t\t\t\t<br class="clear"/>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t</li>\n')
                __M_writer(u'\t\t\t\t\t</ul>\n\t\t\t\t</div>\n')
            else:
                __M_writer(u'\t\t\t\t<div style="padding:90px;text-align:center;color:grey;">')
                __M_writer(escape(selecthostStr))
                __M_writer(u'</div>\n')
            __M_writer(u'\t\t\t<ul>\n\t\t</div>\n    </div>\n')
        __M_writer(u'\n<br>\n<!-- Progress Box -->\n\t<div id="progress">\n\t\t<div class="box-header" style="padding-top:10px">File Transfer Progress</div>\n\t\t<div id="progress-box">\n\t\t\t<div style="position: relative;padding: 3px 0 5px 0;border-bottom:dotted 1px grey">\n\t\t\t\t<div style="width:18px;border:solid white;float:left"></div>\n\t\t\t\t<div class="progress-name"><h3>Name</h3></div>\n\t\t\t\t<div class="progress-host"><h3>Source</h3></div>\n\t\t\t\t<div class="progress-host"><h3>Target</h3></div>\n\t\t\t\t<div class="progress-status"><h3>Status</h3></div>\n\t\t\t\t<div class="progress-time"><h3>Time</h3></div>\n\t\t\t\t<br class="clear"/>\n\t\t    </div>\n        </div>\n    </div>\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headtags(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n\t<script src="/stopwatch.js" type="text/javascript"></script>\n\t<script src="/js/runonload.js"></script>\n\t<script type="text/javascript" src="http://jquery-ui.googlecode.com/svn/tags/latest/ui/jquery-ui.js"></script>\n\t<script type="text/javascript" src="http://jqueryui.com/latest/ui/jquery.ui.sortable.js"></script>\n    <script type="text/javascript" src="http://jqueryui.com/latest/ui/jquery.ui.progressbar.js"></script>\n\n\t<script type="text/javascript">\n\t\tfunction checkAll(id, bID){\n\t\t    var checked = $(\'#\' + id).is(\':checked\');\n\t\t    $("#" + bID + " :checkbox").attr(\'checked\', checked);\n\t\t};\n\n\t\tfunction selectItems(box, bID){\n\t\t    dataString = "box="+box;\n\t\t\tvar files = $("#" + bID + " :checked").each(function(){ dataString += "&file=" + this.name });\n\t\t};\n        \n\t\tfunction changedir(box, dir){\n\t\t\tdataString = "box="+box+"&dir="+dir;\n\t\t\t$.post("/data/changedir", { box:box,dir:dir }, function(){location.href="/data"});\n\t\t};\n\n\t\tfunction download(box, bID){\n\t\t    var myArray = new Array();\n\t\t\t$("#" + bID + " :checked").each(function(){ myArray.push(this.name) });\n\n\t\t    dataString = "box="+box+"&file=[\\"" + myArray[0] + "\\"";\n\t\t\tfor(var i=1;i < myArray.length;i++)\t{\n\t\t\t\tdataString += \',\\"\' + myArray[i] + "\\"";\n\t\t\t}\n\t\t\tdataString += "]";\n\t\t\tif(myArray.length == 0) {\n\t\t\t\talert("Please select a file to download");\n\t\t\t}\n\t\t\telse {\n\t\t\t\twindow.location = \'/data/download.tar.gz?\' + dataString;\n\t\t\t}\n\t\t};\n        \n\t\tfunction deletefiles(box, bID, dir){\n            var fileArray = new Array();\n\t\t\t$("#" + bID + " :checked").each(function(){ fileArray.push(this.name); });\n            if (fileArray.length == 0) {\n                alert(\'Please select a file to be deleted.\');\n                return false;\n            } else {\n\t\t\t    $.post("/data/delete", { box:box, dir:dir, file:fileArray.join(\',\') }, function(){location.href="/data"});\n                return true;\n            }\n\t\t};\n\n\t\tfunction transfer(event,ui){\n\t\t\tvar sourcepath = ui.sender.attr(\'path\');\n\t\t\tvar source = ui.item.attr(\'file\');\n\t\t\tvar target = $(this).attr(\'path\');\n\t\t\tvar sourcehost = ui.sender.attr(\'host\');\n\t\t\tvar targethost = $(this).attr(\'host\');\n\t\t\tvar sourcetype = ui.item.attr(\'type\');\n\t\t\tvar eventid = ui.item.attr(\'var\') + sourcehost.replace(".","") + targethost.replace(".","");\n\t\t\tdataString = "src="+sourcepath+"/"+source+"&srchost="+sourcehost+"&tgt="+target+"&tgthost="+targethost;\n\n\t        $(".fileList li").removeClass(\'alternate\');\n\t        $(".fileList li:nth-child(odd)").addClass(\'alternate\');\n\t\t\tprogressString = "<div id=\'"+eventid+"\'><div class=\'progress-icon\'><img class=\'filesprite\' src=\'/images/waitcursor.gif\'/></div><div class=\'progress-name\'>"+source+"</div>\\n<div class=\'progress-host\'>"+sourcehost+"</div>\\n<div class=\'progress-host\'>"+targethost+"</div>\\n<div class=\'progress-status\'>Queued</div><div id=\'progress-timer\' class=\'progress-time\'></div></div><br class=\'clear\'/>";\n\t\t\t$("#progress-box").append(progressString);\n\n\t\t\t// A Stopwatch instance that displays its time nicely formatted.\n\t\t    var s = new Stopwatch(function(runtime) {\n\t\t         // format time as m:ss.d\n                 var minutes = Math.floor(runtime / 60000);\n                 var seconds = Math.floor(runtime % 60000 / 1000);\n                 var decimals = Math.floor(runtime % 1000 / 100);\n                 var displayText = minutes + ":" + (seconds < 10 ? "0" : "") + seconds + "." + decimals;\n\t\t\t\t $("#"+eventid + " .progress-time").html(displayText);\n            });\n\t\t\ts.doDisplay();\n\t\t\ts.startStop();\n\n\n\t\t    $.ajax({\n\t\t\t    type: "POST",\n\t\t\t\turl: "/data/transfer",\n\t\t\t\tdata: dataString,\n\t\t\t\tbeforeSend: function(){\n\t\t\t\t\t$("#"+eventid + " .progress-status").text("In progress");\n\t\t\t\t},\n\t\t\t\terror: function(msg){\n\t\t\t\t    alert( "Error transfering: " + msg);\n\t\t\t\t\t$("#"+eventid + " .progress-icon").replaceWith("<div class=\'progress-icon\'><img class=\'filesprite\' src=\'/images/redx.png\'/></div>");\n\t\t\t\t\t$("#"+eventid + " .progress-status").text("ERROR");\n\t\t\t        s.startStop();\n\t\t\t\t},\n\t\t\t\tsuccess: function(msg){\n\t\t\t\t\t$("#"+ eventid + " .progress-icon").replaceWith("<div class=\'progress-icon\'><img class=\'filesprite\' src=\'/images/greencheck.png\'/></div>");\n\t\t\t\t\t$("#"+ eventid + " .progress-status").text("Done");\n\t\t\t        s.startStop();\n\t\t\t\t}\n\t\t\t});\n\n\t\t\treturn;\n\t\t};\n\n\t\t<!-- Define draggable and droppable objects -->\n\t\t$(document).ready(function(){\n\t\t\t$("#leftsortable").sortable({\n\t\t\t\t\t\t\t\thelper:\'clone\',\n                                items:\'li\',\n                                connectWith:\'#rightsortable\',\n                                receive: transfer,\n\t\t\t\t\t\t\t\tdropOnEmpty: true\n                            });\n\t\t\t$("#rightsortable").sortable({\n\t\t\t\t\t\t\t\thelper:\'clone\',\n                                items:\'li\',\n                                connectWith:\'#leftsortable\',\n                                receive: transfer,\n\t\t\t\t\t\t\t\tdropOnEmpty: true\n                            });\n\t\t\t$(".fileList li:nth-child(odd)").addClass(\'alternate\');\n\t\t});\n    </script>\n')
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
{"source_encoding": "utf-8", "line_map": {"28": 0, "38": 2, "39": 3, "40": 127, "41": 130, "42": 133, "43": 138, "74": 165, "75": 171, "76": 172, "77": 174, "78": 175, "79": 175, "80": 179, "81": 179, "82": 180, "83": 181, "84": 181, "91": 184, "92": 185, "93": 186, "94": 186, "95": 186, "96": 186, "97": 186, "98": 187, "99": 188, "100": 188, "101": 188, "102": 188, "103": 188, "104": 191, "105": 194, "106": 195, "107": 197, "108": 197, "109": 203, "110": 205, "111": 205, "112": 206, "113": 207, "114": 207, "115": 207, "116": 209, "117": 209, "118": 209, "119": 210, "120": 210, "121": 212, "122": 212, "123": 212, "124": 212, "125": 214, "126": 214, "127": 214, "128": 214, "129": 215, "130": 215, "131": 215, "132": 215, "133": 215, "134": 215, "135": 219, "136": 219, "137": 220, "138": 221, "139": 222, "140": 222, "141": 222, "142": 222, "143": 234, "144": 234, "145": 234, "146": 234, "147": 241, "148": 241, "149": 241, "150": 241, "151": 241, "152": 241, "153": 241, "154": 243, "155": 244, "156": 245, "157": 245, "158": 245, "159": 245, "160": 245, "161": 245, "162": 245, "163": 246, "164": 246, "165": 248, "166": 248, "167": 250, "168": 250, "169": 250, "170": 250, "171": 250, "172": 250, "173": 255, "174": 256, "175": 256, "176": 256, "177": 256, "178": 256, "179": 256, "180": 256, "181": 257, "182": 257, "183": 259, "184": 259, "185": 261, "186": 261, "187": 261, "188": 261, "189": 261, "190": 261, "191": 261, "192": 261, "193": 261, "194": 261, "195": 262, "196": 262, "197": 263, "198": 263, "199": 270, "200": 272, "201": 273, "202": 273, "203": 273, "204": 275, "205": 279, "211": 5, "215": 5, "221": 132, "225": 132, "231": 129, "235": 129, "241": 235}, "uri": "/data/data.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/data/data.mako"}
__M_END_METADATA
"""
