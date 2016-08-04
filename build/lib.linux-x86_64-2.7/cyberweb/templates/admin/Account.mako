<%inherit file="/admin/newAdmin.mako"/>

<%def name="headtags()">
	<script type="text/javascript" src="/js/admin/account.js"></script>
</%def>

<%def name="col2left()">
	${self.col2left()}
</%def>

<%def name="col2main()">
	<div id="maincontent">
		<div id="menu">
			<ul id="menuList">
				<li id="accountLi" onclick="switchTabs(this);">Accounts</li>
				<li id="authkeyLi" class="selected" onclick="switchTabs(this);">Pki Credential</li>
			</ul>
		</div>
		<div id="searchcontainer">
			<div id="authKeyTab" class="classTab">
				<h2 class="header">Auth Key</h2>
				<div id="errorConsoleAuthKey" class="errorStyle"></div>
				<div id="activity_pane_authKey">
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
					<div id="authKeySearchContent" class="searchContent">	
					</div>
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
				</div>
			</div>
			<div id="accountTab" class="classTab">
				<div id="dialog-modal" title="Configure PKI/SSH Passwordless connection to">
					<h2>Add your key</h2>
					<br><p>CyberWeb generates a PKI public/private key pair for your CyberWeb user account. To enable access to a CyberWeb resource, you must have a valid user account and password on that resource. CyberWeb will use the username and password for authentication and installation of the PKI credential onto the remote host. The password is not stored or saved by CyberWeb.</p>
					<p>Note: If your account on the remote resource is not ready, this step can be done at a later time - just click on the cancel button.</p>
					<form name="addResource" method="post" action="">
					  	<label>Username: </label>
					  	<input type="text" name="user" id="sshUserName" value=""/>
						<br/>
						
					  	<label>Password: </label>
					  	<input type="password" name="password" id="sshPassword" />
						<br/>
					</form>
				</div>
				<h2 class="header">Account</h2>
				<div id="errorConsoleAccount" class="errorStyle"></div>
				<div id="activity_pane_account">
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
					<div id="accountSearchContent" class="searchContent">
					</div>
					<div id="opertaionDiv" class="operation">
						<a href="#" class="addNew menuLink"><img src="/images/icon_add-plus.gif" width="34" height="34"/>Add New</a>&nbsp;<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
				</div>
			</div>
		</div>
	</div>
	<script type="text/javascript">
		tabOperationObj.tabList = new Array(document.getElementById('accountLi'),document.getElementById('authkeyLi'));
		tabOperationObj.tabDivList = new Array(document.getElementById('accountTab'),document.getElementById('authKeyTab'));
		tabOperationObj.init();
		tabOperationObj.switchTab(tabOperationObj.tabList[0]);
		
		accountAdminObj.setData(accountsData);
		accountAdminObj.setPopulateData(populateAccountLists);
		accountAdminObj.setParseResponse(parseAccountResponse);
		accountAdminObj.activityPane = 'activity_pane_account';
		
		authKeyAdminObj.setData(authKeyData);
		authKeyAdminObj.setPopulateData(populateAuthKeyLists);
		authKeyAdminObj.setParseResponse(parseAuthKeyResponse);
		authKeyAdminObj.activityPane = 'activity_pane_authKey';
		
		accountAdminObj.getData('/newadmin/forwardRequest','method=view&type=account');
		
		var decodedResourceString = $("<div/>").html("${c.resourceString}").text();
		var decodedUserString = $("<div/>").html("${c.userString}").text();
		
		resourceString = eval('(' + decodedResourceString + ')');
		userString = eval('(' + decodedUserString + ')');
		userName = '${c.user}';
	</script>
</%def>