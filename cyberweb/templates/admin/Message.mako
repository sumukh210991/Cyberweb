<%inherit file="/admin/newAdmin.mako"/>

<%def name="headtags()">
	<script type="text/javascript" src="/js/admin/message.js"></script>
</%def>

<%def name="col2left()">
	${self.col2left()}
</%def>

<%def name="col2main()">
	<div id="maincontent">
		<div id="errorConsole" class="errorStyle"></div>
		<div id="menu">
			<ul id="menuList">
				<li id="messageTypeLi" class="selected" onclick="switchTabs(this);">Message Type</li>
				<li id="messageLi" onclick="switchTabs(this);">Message</li>
			</ul>
		</div>
		<div id="searchcontainer">
			<div id="messageTypeTab" class="classTab">
				<h2 class="header">Message Types</h2>
				<div id="errorConsoleMessageType" class="errorStyle"></div>
				<div id="activity_pane_messageType">
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
					<div id="messageTypeSearchContent" class="searchContent">	
					</div>
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
				</div>
			</div>
			<div id="messageTab" class="classTab">
				<h2 class="header">Messages</h2>
				<div id="errorConsoleMessage" class="errorStyle"></div>
				<div id="activity_pane_message">
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
					<div id="messageSearchContent" class="searchContent">
					</div>
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
				</div>
			</div>
		</div>
	</div>
	<script type="text/javascript">
		var decodedUserString = $("<div/>").html("${c.userString}").text();
		var decodedGroupString = $("<div/>").html("${c.groupString}").text();
		var decodedMessageTypeString = $("<div/>").html("${c.messageTypeString}").text();
		
		userString = eval('(' + decodedUserString + ')');
		groupString = eval('(' + decodedGroupString + ')');
		messageTypeString = eval('(' + decodedMessageTypeString + ')');
		init();
	</script>
</%def>