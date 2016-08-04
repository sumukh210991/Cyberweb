<%inherit file="/admin/newAdmin.mako"/>

<%def name="headtags()">
	<script type="text/javascript" src="/js/admin/group.js"></script>
	<style>
		.passwordTable {
			width: 100%;
		}
		
		.passwordTable td{
			border: 0px;
			text-align: left;
		}
		
		.rightLable {
			text-align: right !important;
		}
	</style>
</%def>

<%def name="col2left()">
	${self.col2left()}
</%def>

<%def name="col2main()">
	<div id="maincontent">
		<div id="menu">
			<ul id="menuList">
				<li id="userLi" class="selected" onclick="switchTabs(this);">User</li>
				<li id="groupLi" onclick="switchTabs(this);">Group</li>
				<li id="userGroupLi" onclick="switchTabs(this);">User group</li>
			</ul>
		</div>
		<div id="searchcontainer">
			<div id="userTab" class="classTab">
				<div id="dialog-modal" title="Set Password">
					<h2>Set or Change Password</h2>
					<br>Please set or change password. if you do not wish to modify it, please click cancel.
					<form name="changePassword" method="post" action="">
						<table class="passwordTable">
							<tr>
								<td class="rightLable"><label>Password: </label>
								<td><input type="password" name="pass" id="password" value=""/></td>
							</tr>
							<tr>
								<td class="rightLable"><label>Confirm Password: </label>
								<td><input type="password" name="confPass" id="confirmPassword" value=""/></td>
							</tr>
						</table>
					</form>
					<input type="hidden" id="passwordField" />
				</div>
				<h2 class="header">Users</h2>
				<div id="errorConsoleUsers" class="errorStyle"></div>
				<div id="activity_pane_users">
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
					<div id="userSearchContent" class="searchContent">	
					</div>
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
				</div>
			</div>
			<div id="groupTab" class="classTab">
				<h2 class="header">Groups</h2>
				<div id="errorConsoleGroups" class="errorStyle"></div>
				<div id="activity_pane_groups">
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
					<div id="groupSearchContent" class="searchContent">
					</div>
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
				</div>
			</div>
			<div id="userGroupTab" class="classTab">
				<h2 class="header">User Group Association</h2>
				<div id="errorConsoleUsersGroups" class="errorStyle"></div>
				<div id="activity_pane_users_groups">
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
					<div id="userGroupSearchContent" class="searchContent">
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
		
		userString = eval('(' + decodedUserString + ')');
		groupString = eval('(' + decodedGroupString + ')');
		
		init();
	</script>
</%def>