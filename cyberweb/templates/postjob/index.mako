## data.mako - file browser

<%inherit file="/layout.mako"/>

<%def name="headtags()">

	<link rel="stylesheet" type="text/css" href="/css/highslide.css" />

	<script type="text/javascript" src="/stopwatch.js"></script>
	<script type="text/javascript" src="/js/runonload.js"></script>
	<script type="text/javascript" src="/js/jquery-ui.js"></script>
	<script type="text/javascript" src="/js/jquery.ui.sortable.js"></script>
    <script type="text/javascript" src="/js/jquery.ui.progressbar.js"></script>
	<script type="text/javascript" src="/js/jquery.base64.js"></script>
	<script type="text/javascript" src="/js/jquery.base64.min.js"></script>
	<script type="text/javascript" src="/js/postjob.js"></script>
	<script type="text/javascript" src="/js/highslide.js"></script>
	<script type="text/javascript" src="/js/jwplayer.js" ></script>
	<script type="text/javascript" src="/js/jwplayer.html5.js" ></script>
	<style type='text/css'>
		.form_table tr, .form_table td{
			border: none;
		}
		
		#content, #graphbrowser{
			margin: 0px;
		}
	
		.dark{
			background: none;
		}
		
		.alternate {
    		background-color: none;
		}
	</style>

	<script type="text/javascript">
//<![CDATA[
hs.registerOverlay({
	html: '<div class="closebutton" onclick="return hs.close(this)" title="Close"></div>',
	position: 'top right',
	fade: 2 // fading the semi-transparent overlay looks bad in IE
});


hs.graphicsDir = '../images/';
hs.outlinesDir = '../images/'
hs.outlineType = 'rounded-black';
//hs.wrapperClassName = 'borderless';
//]]>
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


<div id="loading">
	<p><img src="/images/loading2.gif" class="loading_img"></p>
</div>
<div id="graphbrowser">
<!-- For Loop Browser Box -->
	<div>
  		<div class="machine-browser">
			## Browser Box location information (i.e. host,path)
            ## cyberweb home data should come from development.ini configuration file
			<div class="file-box">
			## Browser Box location information (i.e. host,path)
			<form name="browserLocation" method="post" action="">
				<input type="hidden" name="box" value="${box}" />
				<div class="header-text">Host:</div>
				<div class="header-input">
				<!--<select name="host" onchange="this.form.submit();" >-->
				<select name="host" id="host" onchange="select_Host();" >
				    <option VALUE="">${selecthostStr}...</option>
		              % for account_id, resource in session['available_resources'].items():
						<%
								if  'longboard' in resource['name']:
										name = 'CyberWeb Home'
						%>
						% if host[box] == account_id:
							<option VALUE="${account_id}" selected="selected">${resource['name']}</option>
						% else:
							<option VALUE="${account_id}">${resource['name']}</option>
						% endif
					  % endfor
				</select>
				</div>
				<br class="clear"/>
				<div class="header-text">Directory:</div>
				<div class="header-input">
					<input type="text" size="20" name="path" id="host_path" value="${path[box]}" />
				</div>
				<div class="header-input">
					<input id="get_listing_button" type="submit" class="button" value="Go" />
				</div>
				<br class="clear"/>
				<div class="header-text"></div>
				
				<div id='' class="header-icon" onClick="changedir('${box}','..Parent Directory')"><img src="/images/uponedir.jpg" alt="Go to Parent Directory" /></div>
				<div id='' class="header-icon" onClick="changedir('${box}','..Home Directory')"><img src="/images/home.jpg" alt="Go to Home Directory" /></div>
				<div id='' class="header-icon" onClick="changedir('${box}','..Refresh Listing')"><img src="/images/refresh2.jpg" alt="Refresh listing" /></div>				
				<!--
				<div id='' class="header-icon" onClick="selectItems('${box}','${box}sortable')"><img src="/images/rename.gif"/></div>				
				<div id='' class="header-icon" onClick="download('${box}','${box}sortable')"><img src="/images/move.gif"/></div>
				<div id='' class="header-icon" onClick="deletefiles('${box}','${box}sortable', '${path[box]}')"><img src="/images/trash.gif"/></div>
				-->
				<br class="clear"/>
			</form>
	
			<div id="${box}databox" class="dataarea">
				% if host[box] != '' and path[box] != '':
					<!--<div style="position: relative;padding: 3px 0 5px 0;border-bottom:dotted 1px grey">
						<div class="detail-check">
							<input type="checkbox" id="${box}checkall" onClick="checkAll(this.id, '${box}sortable')"/>
						</div>
						<div style="margin-left:7px;width:7px;border:solid white;float:left"></div>
						<div class="detail-name"><h3>Name</h3></div>
						<div class="detail-size"><h3>Size</h3></div>
						<div class="detail-modified"><h3>Modified</h3></div>
						<br class="clear"/>
					</div>-->
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
											<div class="detail-check"><!--<input type="checkbox" name="${listvar[box][a]}" />--></div>
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
											<div class="detail-check"><!--<input type="checkbox" name="${listing[box][a][1]}" />--></div>
											<div class="detail-icon"><img class="filesprite" src="/images/text.gif"/></div>
											<div class="detail-name" onClick="javascript: return setFileName(this)">${listing[box][a][1]}</div>
											<!--<div class="detail-size">${listing[box][a][3]}</div>
											<div class="detail-modified">${listing[box][a][2]}</div>-->
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
			<div id="select_job_div">
				<form class="select_job_form">
					<input type="hidden" name="job_path" id="job_path" value="${path[box]}" />
					<input type="hidden" name="script" value="read.job.summary.ssh"/>
					<input type="hidden" name="file_name" id= "file_name" value=""/>
					 % for resource,name in session['available_resources'].items():
						<%
							#if name == 'longboard':
							if  'longboard' in name:
								name = 'CyberWeb Home'
						%>
						<input type="hidden" name="host" value="${resource}" />
					% endfor
					<!--<input class="select_job" type="button" name="submit" value="Analyze Job" />-->
					<!--<input class="image_submit" type="button" name="image_submit" value="Display Image" />-->
					<!--<input class="create_remote_script" type="button" name="create_remote_script" value="Create Remote Script" />-->
				</form>
			</div>
			
			<div id="job_summary">
	 			<!--<img src="images/open.png" alt="open job summary">-->
	 			<h4>Job Summary</h4>
				<div id='summary'></div>
			</div>
			
			<div style='clear:both'><br /></div>
		</div>
	 	<div class='plot_options'>
	 		<form name='get_plot_form' id='get_plot_form' onsubmit="javascript: return false;">
				<table class="options_table">
					<tr id='options_table_tr1'>
						<td>
							<div id="analysis_types_div">
								<h3>Analysis Type</h3>
								<select id="analysisTypes" name="analysisTypes" >
									<option value="" selected>--Select--</option>
									% for item in c.plots['analysisTypes']: 
										<option name="${item['label']}" value="${item['name']}">${item['label']}</option>
									% endfor
								</select>							
								<input type='hidden' id='plot_file' name='plot_file' value=''/>
								<input type='hidden' id='check_selected_job' name='check_selected_job' value=''/>
							</div>
						</td>
					</tr>
				</table>
				<label id="job_selected"></label>
				<label id='plot_filename'></label>
	 		</form>
	 		
			<div id="plot_table_wrapper">
				<table id="plot_table">
					
					
					
				</table>
				<div id='movie_holder'>
					<!--<embed id="myVideoTag" width="670" height="377" name="plugin" 
							src="" 
							type="video" play="false">
					</embed>
					-->
					
					
				</div>
			</div>
	 	</div>	
  	</div>
 </div>

<br>
</div>
