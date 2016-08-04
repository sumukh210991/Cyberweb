<%inherit file="/admin/newAdmin.mako"/>

<%def name="headtags()">
	<script type="text/javascript" src="/js/admin/service.js"></script>
</%def>

<%def name="col2left()">
	${self.col2left()}
</%def>

<%def name="col2main()">
	<div id="maincontent">
		<div id="errorConsole" class="errorStyle"></div>
		<div id="menu">
			<ul id="menuList">
				<li id="serviceTypeLi" class="selected" onclick="switchTabs(this);">Service Type</li>
				<li id="serviceNameLi" onclick="switchTabs(this);">Service Name</li>
				<li id="serviceLi" onclick="switchTabs(this);">Services</li>
			</ul>
		</div>
		<div id="searchcontainer">
			<div id="serviceTypeTab" class="classTab">
				<h2 class="header">Service Types</h2>
				<div id="errorConsoleServiceType" class="errorStyle"></div>
				<div id="activity_pane_serviceType">
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
					<div id="serviceTypeSearchContent" class="searchContent">	
					</div>
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
				</div>
			</div>
			<div id="serviceNameTab" class="classTab">
				<h2 class="header">Service Names</h2>
				<div id="errorConsoleServiceName" class="errorStyle"></div>
				<div id="activity_pane_serviceName">
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
					<div id="serviceNameSearchContent" class="searchContent">
					</div>
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
				</div>
			</div>
			<div id="servicesTab" class="classTab">
				<table id="searchService">
					<tr>
						<td><label>Services</label></td>
						<td>
							<select id="serviceList" MULTIPLE>
							% for service in c.service:
								<option value="${service.id}">${service.name}</option>
							% endfor
							</select>
						</td>
					</tr>
					<tr>
						<td></td>
						<td>
							<input type="button" class="buttonStyle" value="Show Resources" onclick="searchServices();"/> <input type="button" class="buttonStyle" value="Refresh" onclick="refereshService();"/>
						</td>
					</tr>
				</table>
				<div id="serviceSearchContent" class="searchContent">
				</div>
			</div>
		</div>
	</div>
	<script type="text/javascript">
		var decodedServiceTypeString = $("<div/>").html("${c.serviceTypeString}").text();
		serviceTypeString = eval('(' + decodedServiceTypeString + ')');
		
		init();
	</script>
</%def>