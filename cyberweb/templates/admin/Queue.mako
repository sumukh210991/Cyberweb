<%inherit file="/admin/newAdmin.mako"/>

<%def name="headtags()">
	<script type="text/javascript" src="/js/admin/queue.js"></script>
</%def>

<%def name="col2left()">
	${self.col2left()}
</%def>

<%def name="col2main()">
	<div id="maincontent">
		<div id="errorConsole" class="errorStyle"></div>
		<div id="menu">
			<ul id="menuList">
				<li id="queueTypeLi" class="selected" onclick="switchTabs(this);">Queue Type</li>
				<li id="queueInfoLi" onclick="switchTabs(this);">Queue Info</li>
				<li id="queueSystemLi" onclick="switchTabs(this);">Queue System</li>
				<li id="queueServiceLi" onclick="switchTabs(this);">Queue Service</li>
			</ul>
		</div>
		<div id="searchcontainer">
			<div id="queueTypeTab" class="classTab">
				<h2 class="header">Queue Types</h2>
				<div id="errorConsoleQueueType" class="errorStyle"></div>
				<div id="activity_pane_queueType">
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
					<div id="queueTypeSearchContent" class="searchContent">	
					</div>
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
				</div>
			</div>
			<div id="queueInfoTab" class="classTab">
				<h2 class="header">Queue Infos</h2>
				<div id="errorConsoleQueueInfo" class="errorStyle"></div>
				<div id="activity_pane_queueInfo">
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
					<div id="queueInfoSearchContent" class="searchContent">
					</div>
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
				</div>
			</div>
			<div id="queueSystemTab" class="classTab">
				<h2 class="header">Queue Systems</h2>
				<div id="errorConsoleQueueSystem" class="errorStyle"></div>
				<div id="activity_pane_queueSystem">
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
					<div id="queueSystemSearchContent" class="searchContent">
					</div>
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
				</div>
			</div>
			<div id="queueServiceTab" class="classTab">
				<h2 class="header">Queue Service</h2>
				<div id="errorConsoleQueueService" class="errorStyle"></div>
				<div id="activity_pane_queueService">
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
					<div id="queueServiceSearchContent" class="searchContent">
					</div>
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
				</div>
			</div>
		</div>
	</div>
	<script type="text/javascript">
		var decodedResourceString = $("<div/>").html("${c.resourceString}").text();
		var decodedQueueTypeString = $("<div/>").html("${c.queueTypeString}").text();
		var decodedQueueInfoString = $("<div/>").html("${c.queueInfoString}").text();
		var decodedQueueSystemString = $("<div/>").html("${c.queueSystemString}").text();
		
		resourceString = eval('(' + decodedResourceString + ')');
		queueTypeString = eval('(' + decodedQueueTypeString + ')');
		queueInfoString = eval('(' + decodedQueueInfoString + ')');
		queueSystemString = eval('(' + decodedQueueSystemString + ')');
		
		init();
	</script>
</%def>