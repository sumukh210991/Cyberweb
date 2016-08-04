<%inherit file="/account/account.layout.mako"/>

<%def name="headtags()">
	<script type="text/javascript" src="/js/account/account.js"></script>
	
	<style>
		.confirmationStyle {
			color: #064F08;
			margin: 0;
			padding: 1em;
			font-weight: bold;
		}
	</style>
</%def>

<%def name="col2left()">
	${self.col2left()}
</%def>

<%def name="col2main()">
	<div id="maincontent">
		<div id="menu">
		</div>
		<div id="searchcontainer">
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
				<div id="errorConsoleAccount" class="confirmationStyle"></div>
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
	<input type="hidden" id="userCredential" />
	<script type="text/javascript">
		var decodedResourceString = $("<div/>").html("${c.resourceString}").text();
		
		resourceString = eval('(' + decodedResourceString + ')');
		userName = '${c.user}';
		userId = '${c.userId}';
		
		init();
	</script>
</%def>