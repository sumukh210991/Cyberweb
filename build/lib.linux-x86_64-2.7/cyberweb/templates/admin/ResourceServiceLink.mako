<%inherit file="/admin/newAdmin.mako"/>

<%def name="headtags()">
	<script type="text/javascript" src="/js/admin/resource_service.js"></script>
	<style>
		.header {
			width: 95%;
			border-spacing: 5px;
			border-collapse:separate;
			margin: 0px;
		}
		
		.header td {
			background-color: #CCCCCC !important;
			border: 0px;
			padding-top: .5em;
    		padding-bottom: .5em;
		}
		
		.clear {
			clear: both;
		}
		
		.resourceList, .serviceList {
			margin: 10px 3em;
		}
		
		.smallHeader {
			width: 50px;
			max-width: 50px;
		}
		
		/*.aviableSevice, .operation, .addedServices {
			float: left;
		}*/
		
		#addedServiceList, #availableServiceList {
			max-width: 150px;
			min-width: 150px;
			min-height: 150px;
			max-height: 150px;
		}
		
		/*.operation {
			vertical-align: middle;
			margin: 30px 0;
			min-height: 150px;
			max-height: 150px;
		}*/
		
		.operation input {
			width: 30px;
			margin: 2px;
			font-weight: bold;
		}
		
		.saveLinks {
			text-align: center;
		}
		
		.saveLinks a {
			text-decoration: underline;
			padding-right: 10px;
			color: #0066CC;
			font-size: 14px;
		}
		
		.textStyle{
			padding: 10px;
		}
	</style>
</%def>

<%def name="col2left()">
	${self.col2left()}
</%def>

<%def name="col2main()">
	<div id="maincontent">
		<h2>Configure Services to Resource</h2>
		<div id="step1">
			<table class="header">
				<tr>
					<td class="smallHeader">Step 1.</td>
					<td> Choose resource to add service </td>
				</tr>
			</table>
			<div class="clear resourceList">
				<span> Resources: </span>
				<select id="resourceList" name="resources">
					<option value="" selected>Select</option>
				% for resource in c.resource:
					<option value="${resource.id}">${resource.name}</option>
				% endfor
				</select>
				<span class="textStyle"> If it is not here, Click <a href="/newadmin/resourceDetails" title="Add Resource">here</a> to add. </span>
			</div>
		</div>
		<div id="step2">
			<table class="header">
				<tr>
					<td class="smallHeader">Step 2.</td>
					<td> Add or Delete Service to Resource </td>
				</tr>
			</table>
			<div class="clear">
				<div id="resourceServiceLinkTab" class="classTab">
					<div id="errorConsoleResourceServiceLink" class="errorStyle"></div>
					<div id="activity_pane_resourceServiceLink">
						<div id="opertaionDiv" class="operation">
							<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
						</div>
						<div id="resourceServiceLinkSearchContent" class="searchContent">
						</div>
						<div id="opertaionDiv" class="operation">
							<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
	<script>
		var decodedServiceString = $("<div/>").html("${c.serviceString}").text();
		var decodedProtocolString = $("<div/>").html("${c.protocolString}").text();
		
		serviceList = eval('(' + decodedServiceString + ')');
		protocolList = eval('(' + decodedProtocolString + ')');
	</script>
</%def>