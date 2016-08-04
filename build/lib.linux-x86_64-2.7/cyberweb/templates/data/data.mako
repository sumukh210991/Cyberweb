## data.mako - file browser

<%inherit file="/layout.mako"/>

<%def name="headtags()">
	<script src="/stopwatch.js" type="text/javascript"></script>
	<script src="/js/runonload.js"></script>
	<script type="text/javascript" src="http://jquery-ui.googlecode.com/svn/tags/latest/ui/jquery-ui.js"></script>
	<script type="text/javascript" src="http://jqueryui.com/latest/ui/jquery.ui.sortable.js"></script>
    <script type="text/javascript" src="http://jqueryui.com/latest/ui/jquery.ui.progressbar.js"></script>

	<script type="text/javascript">
		function checkAll(id, bID){
		    var checked = $('#' + id).is(':checked');
		    $("#" + bID + " :checkbox").attr('checked', checked);
		};

		function selectItems(box, bID){
		    dataString = "box="+box;
			var files = $("#" + bID + " :checked").each(function(){ dataString += "&file=" + this.name });
		};
        
		function changedir(box, dir){
			dataString = "box="+box+"&dir="+dir;
			$.post("/data/changedir", { box:box,dir:dir }, function(){location.href="/data"});
		};

		function download(box, bID){
		    var myArray = new Array();
			$("#" + bID + " :checked").each(function(){ myArray.push(this.name) });

		    dataString = "box="+box+"&file=[\"" + myArray[0] + "\"";
			for(var i=1;i < myArray.length;i++)	{
				dataString += ',\"' + myArray[i] + "\"";
			}
			dataString += "]";
			if(myArray.length == 0) {
				alert("Please select a file to download");
			}
			else {
				window.location = '/data/download.tar.gz?' + dataString;
			}
		};
        
		function deletefiles(box, bID, dir){
            var fileArray = new Array();
			$("#" + bID + " :checked").each(function(){ fileArray.push(this.name); });
            if (fileArray.length == 0) {
                alert('Please select a file to be deleted.');
                return false;
            } else {
			    $.post("/data/delete", { box:box, dir:dir, file:fileArray.join(',') }, function(){location.href="/data"});
                return true;
            }
		};

		function transfer(event,ui){
			var sourcepath = ui.sender.attr('path');
			var source = ui.item.attr('file');
			var target = $(this).attr('path');
			var sourcehost = ui.sender.attr('host');
			var targethost = $(this).attr('host');
			var sourcetype = ui.item.attr('type');
			var eventid = ui.item.attr('var') + sourcehost.replace(".","") + targethost.replace(".","");
			dataString = "src="+sourcepath+"/"+source+"&srchost="+sourcehost+"&tgt="+target+"&tgthost="+targethost;

	        $(".fileList li").removeClass('alternate');
	        $(".fileList li:nth-child(odd)").addClass('alternate');
			progressString = "<div id='"+eventid+"'><div class='progress-icon'><img class='filesprite' src='/images/waitcursor.gif'/></div><div class='progress-name'>"+source+"</div>\n<div class='progress-host'>"+sourcehost+"</div>\n<div class='progress-host'>"+targethost+"</div>\n<div class='progress-status'>Queued</div><div id='progress-timer' class='progress-time'></div></div><br class='clear'/>";
			$("#progress-box").append(progressString);

			// A Stopwatch instance that displays its time nicely formatted.
		    var s = new Stopwatch(function(runtime) {
		         // format time as m:ss.d
                 var minutes = Math.floor(runtime / 60000);
                 var seconds = Math.floor(runtime % 60000 / 1000);
                 var decimals = Math.floor(runtime % 1000 / 100);
                 var displayText = minutes + ":" + (seconds < 10 ? "0" : "") + seconds + "." + decimals;
				 $("#"+eventid + " .progress-time").html(displayText);
            });
			s.doDisplay();
			s.startStop();


		    $.ajax({
			    type: "POST",
				url: "/data/transfer",
				data: dataString,
				beforeSend: function(){
					$("#"+eventid + " .progress-status").text("In progress");
				},
				error: function(msg){
				    alert( "Error transfering: " + msg);
					$("#"+eventid + " .progress-icon").replaceWith("<div class='progress-icon'><img class='filesprite' src='/images/redx.png'/></div>");
					$("#"+eventid + " .progress-status").text("ERROR");
			        s.startStop();
				},
				success: function(msg){
					$("#"+ eventid + " .progress-icon").replaceWith("<div class='progress-icon'><img class='filesprite' src='/images/greencheck.png'/></div>");
					$("#"+ eventid + " .progress-status").text("Done");
			        s.startStop();
				}
			});

			return;
		};

		<!-- Define draggable and droppable objects -->
		$(document).ready(function(){
			$("#leftsortable").sortable({
								helper:'clone',
                                items:'li',
                                connectWith:'#rightsortable',
                                receive: transfer,
								dropOnEmpty: true
                            });
			$("#rightsortable").sortable({
								helper:'clone',
                                items:'li',
                                connectWith:'#leftsortable',
                                receive: transfer,
								dropOnEmpty: true
                            });
			$(".fileList li:nth-child(odd)").addClass('alternate');
		});
    </script>
</%def>

<%def name="header()">
</%def>

<%def name="footer()">
</%def>



## Body
<%
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
%>



<div id="browser">
<!-- For Loop Browser Box -->
  %for box in ['left','right']:
    <div class="file-box">
		## Browser Box location information (i.e. host,path)
		<form name="browserLocation" method="post" action="">
		    <input type="hidden" name="box" value="${box}" />
		    <div class="header-text">Host:</div>
		    <div class="header-input">
				<select name="host" onchange="this.form.submit();">
				    <OPTION VALUE="">${selecthostStr}...</option>
		              % for account_id, resource in session['available_resources'].items():
						<%
								if  'longboard' in resource['name']:
										name = 'CyberWeb Home'
						%>
						% if host[box] == account_id:
							<OPTION VALUE="${account_id}" selected="selected">${resource['name']}</option>
						% else:
							<OPTION VALUE="${account_id}">${resource['name']}</option>
						% endif
					  % endfor
				</select>
		    </div>
		    <br class="clear"/>
		    % if not app_globals.is_community_model:
		    <div class="header-text">Directory:</div>
		    <div class="header-input">
				<input type="text" size="100" name="path" value="${path[box]}" />
		    </div>
		    <div class="header-input">
				<input type="submit" class="button" value="Go" />
		    </div>
		    % endif
		    <br class="clear"/>
		    <div class="header-text"></div>
		    <div id='' class="header-icon" onClick="changedir('${box}','..Parent Directory')"><img src="/images/uponedir.jpg" alt="Go to Parent Directory" /></div>
		    % if not app_globals.is_community_model:
		    <div id='' class="header-icon" onClick="changedir('${box}','..User Home Directory')">~</div>
		    % endif
		    <div id='' class="header-icon" onClick="changedir('${box}','..Home Directory')"><img src="/images/home.jpg" alt="Go to Home Directory" /></div>
		    <div id='' class="header-icon" onClick="changedir('${box}','..Refresh Listing')"><img src="/images/refresh2.jpg" alt="Refresh listing" /></div>
			<!--
		    <div id='' class="header-icon" onClick="selectItems('${box}','${box}sortable')"><img src="/images/rename.gif"/></div>
			-->
		    <div id='' class="header-icon" onClick="download('${box}','${box}sortable')"><img src="/images/move.gif"/></div>
		    <div id='' class="header-icon" onClick="deletefiles('${box}','${box}sortable', '${path[box]}')"><img src="/images/trash.gif"/></div>
		    <br class="clear"/>
		</form>

		<div id="${box}databox" class="dataarea">
			% if host[box] != '' and path[box] != '':
				<div style="position: relative;padding: 3px 0 5px 0;border-bottom:dotted 1px grey">
					<div class="detail-check"><input type="checkbox" id="${box}checkall" onClick="checkAll(this.id, '${box}sortable')"/></div>
			        <div style="margin-left:7px;width:7px;border:solid white;float:left"></div>
					<div class="detail-name"><h3>Name</h3></div>
					<div class="detail-size"><h3>Size</h3></div>
					<div class="detail-modified"><h3>Modified</h3></div>
				    <br class="clear"/>
				</div>
				<li>
					<div id=''>
						<div style="position: relative;">
							<div style="width:12px;border:solid white;float:left"></div>
							<div class="detail-icon"><img class="filesprite" src="/images/uparrow.gif"/></div>
							<div class="detail-name"><a href="#" onClick="changedir('${box}','..Parent Directory', '${path[box]}')">Parent Directory..</a></div>
							<br class="clear"/>
						</div>
					</div>
				</li>

				## Output of ls
				<div id="${box}sortable" class="sortable" host="${host[box]}" path="${path[box]}">
					<ul class="fileList">
					  % for a in listarr[box]:
						% if dirvar[box][a] == 1:
							<li var="${listvar[box][a]}" file="${a}" host="${host[box]}" type="directory">
								<div class="${box}drag">
									<div style="position: relative;">
										<div class="detail-check"><input type="checkbox" name="${listvar[box][a]}" /></div>
										<div class="detail-icon"><img class="filesprite" src="/images/folder.gif"/></div>
										<div class="detail-name"><a href="#" onClick="changedir('${box}','${a}')">${a}</a></div>
										<br class="clear"/>
									</div>
								</div>
							</li>
						% else:
							<li var="${listvar[box][a]}" file="${listing[box][a][1]}" host="${host[box]}" type="file">
								<div class="${box}drag">
									<div style="position: relative;">
										<div class="detail-check"><input type="checkbox" name="${listing[box][a][1]}" /></div>
										<div class="detail-icon"><img class="filesprite" src="/images/text.gif"/></div>
										<div class="detail-name" onClick="window.open('/data/getfile?host=${host[box]}&path=${path[box]}/${listing[box][a][1]}','${listing[box][a][1]}','width=400,height=300,toolbar=no,location=no,directories=no,status=no,menubar=no,resizable=yes,scrollbars=yes')">${listing[box][a][1]}</div>
										<div class="detail-size">${listing[box][a][3]}</div>
										<div class="detail-modified">${listing[box][a][2]}</div>
										<br class="clear"/>
									</div>
								</div>
							</li>
						% endif
					  % endfor
					</ul>
				</div>
			% else:
				<div style="padding:90px;text-align:center;color:grey;">${selecthostStr}</div>
			% endif:
			<ul>
		</div>
    </div>
  %endfor

<br>
<!-- Progress Box -->
	<div id="progress">
		<div class="box-header" style="padding-top:10px">File Transfer Progress</div>
		<div id="progress-box">
			<div style="position: relative;padding: 3px 0 5px 0;border-bottom:dotted 1px grey">
				<div style="width:18px;border:solid white;float:left"></div>
				<div class="progress-name"><h3>Name</h3></div>
				<div class="progress-host"><h3>Source</h3></div>
				<div class="progress-host"><h3>Target</h3></div>
				<div class="progress-status"><h3>Status</h3></div>
				<div class="progress-time"><h3>Time</h3></div>
				<br class="clear"/>
		    </div>
        </div>
    </div>
</div>
