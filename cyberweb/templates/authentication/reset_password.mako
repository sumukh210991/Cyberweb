<%inherit file="/authentication/authentication.layout.mako"/>

<%def name="headtags()">
</%def>

<%def name="col2main()">

	<script type="text/javascript">
		function changePassword() {
			var messageCenter = document.getElementById("messageCenter");
			var newpassword = document.getElementById("newpassword");
			var newconfirmpassword = document.getElementById("newconfirmpassword");
			
			if(newpassword.value == newconfirmpassword.value) {
				$.post('/authentication/changePassword',$('#prefbar').serialize(),getResult);
			} else {
				messageCenter.innerHTML = "New Password and Confirmation Password do not match.";
				messageCenter.className = 'errorConsole';
				setTimeout("$('#messageCenter').hide('slow');",10000);
			}
		}
		
		function getResult(data) {
			$('#messageCenter').show('slow');
			var messageCenter = document.getElementById("messageCenter");
			myData = eval("(" + data + ")");
			var isError = myData['Error'];
			var message = myData['Message'];
			messageCenter.innerHTML = message;
			if(isError.toUpperCase() == 'TRUE') {
				messageCenter.className = 'errorConsole';
			} else {
				messageCenter.className = 'messageConsole';
			}
			setTimeout("$('#messageCenter').hide('slow');",10000);
		}
	</script>
	
  <style type="text/css">
  	.errorConsole {
  		margin: 0.5em;
  		color: red;
  		font-weight: bold;
  	}
  	.messageConsole {
  		margin: 0.5em;
  		color: green;
  		font-weight: bold;
  	}
    .prefbutton {
      margin:0 10px 0 10px;
      display:inline;
    }
    .prefbuttons {
      width: 190px;
      margin: 0 auto;
      text-align: center;
    }
    .prefheader {
      float:left;
      width: 130px;
      text-align: right;
      color: grey;
      font-weight: bold;
      margin: 5px 0 5px 0;
    }
    .prefvalue {
      float:left;
      padding-left:15px;
      width: 323px;
      margin: 5px 0 5px 0;
    }
    .prefbar {
      background:#cccccc;
      padding-left:15px;
      margin-bottom:7px;
    }
  </style>

  <div style="width:500px">

  <div class="prefbar">Change Password for CyberWeb User:   ${c.account['username']}</div>
  	<div id="messageCenter"></div>
  	<form id="prefbar" name="prefbar" mathod="POST" action="">
  		<div id="oldpasswordDiv" class="prefrow">
			<div class="prefheader">Old Password:</div><div class="prefvalue"><input type="password" 
                             id="oldpassword" name="oldpassword" value=""/></div>
		</div>
		<div id="newpasswordDiv" class="prefrow">
			<div class="prefheader">New Password:</div><div class="prefvalue"><input type="password" 
                             id="newpassword" name="newpassword" value=""/></div>
		</div>
		<div id="newconfirmpasswordDiv" class="prefrow">
			<div class="prefheader">Confirm Password:</div><div class="prefvalue"><input type="password" 
                             id="newconfirmpassword" name="newconfirmpassword" value=""/></div>
		</div>
		
		<br>
		<div class="prefbuttons">
    		<div id="savebutton" class="prefbutton"><a href="#" onClick="changePassword();">Save Password</a></div>
    		<div id="cancelbutton" class="prefbutton"><a href="#" onClick="document.prefbar.clear();">Cancel</a></div>
  		</div>
	</form>
  </div>
  <br><br>

  </div>
</%def>
