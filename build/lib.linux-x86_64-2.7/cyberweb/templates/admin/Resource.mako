<%inherit file="/admin/newAdmin.mako"/>

<%def name="headtags()">
	<script type="text/javascript" src="/js/admin/resource.js"></script>
</%def>

<%def name="col2left()">
	${self.col2left()}
</%def>

<%def name="col2main()">
	<div id="maincontent">
		<div id="errorConsole" class="errorStyle"></div>
		<div id="menu">
			<ul id="menuList">
				<li id="resourceNameLi" class="selected" onclick="switchTabs(this);">Resource Name</li>
				<li id="resourceLi" onclick="switchTabs(this);">Resource</li>
			</ul>
		</div>
		<div id="searchcontainer">
			<div id="resourceNameTab" class="classTab">
				<h2 class="header">Resource Names</h2>
				<div id="errorConsoleResourceName" class="errorStyle"></div>
				<div id="activity_pane_resourceName">
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
					<div id="resourceNameSearchContent" class="searchContent">
					</div>
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
				</div>
			</div>
			<div id="resourceTab" class="classTab">
				<table id="searchResource">
					<tr>
						<td><label>Resources:</label></td>
						<td>
							<select id="resourceList" name="resources" MULTIPLE>
							
							% for resource in c.resource:
								<option value="${resource.id}">${resource.name}</option>
							% endfor
							</select>
						</td>
					</tr>
					<tr>
						<td></td>
						<td>
							<input type="button" class="buttonStyle" value="Show Services" onclick="searchResource();"/> <input type="button" class="buttonStyle" value="Refresh" onclick="refereshResource();"/>
						</td>
					</tr>
				</table>
				<div id="resoruceSearchContent" class="searchContent">	
				</div>
			</div>
		</div>
	</div>
	<script>
		var decodedQueueSystemString = $("<div/>").html("${c.queueSystemString}").text();
		queueSystemString = eval('(' + decodedQueueSystemString + ')');
		
		initializeForm();
	</script>
</%def>