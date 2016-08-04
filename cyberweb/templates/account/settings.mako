<%inherit file="/account/account.layout.mako"/>

<%def name="headtags()">
</%def>

<%def name="col2main()">

        <script type="text/javascript">
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
  <h2>Change your personal information.</h2>
  <br>
  <p>
  <form name="dataForm" method="POST" action="">
  <div class="prefbar">User Information</div>
  <div id="accounttable">
      % for k,v in c.account.items():
        <div id="${k}" class="prefrow">
          <div class="prefheader">${k}:</div>
          % if k == 'password':
            <div class="prefvalue"><input type="password" name="${k}" value="${v}"/></div>
          % else:
            <div class="prefvalue"><input type="text" name="${k}" value="${v}"/></div>
          % endif
        </div>
        <div class="clear"></div>
      % endfor
  </div>
  % if c.message:
    <div id="status" class="prefrow">
    <div class="prefbuttons">
    % if c.error:
      <font color="red">${c.message}</font>
    % else:
      <font color="green">${c.message}</font>
    % endif
    </div>
    </div>
  % endif

  <br>
  <div class="prefbuttons">
    <div id="savebutton" class="prefbutton"><a href="#" onClick="document.dataForm.submit()">Save User Information</a></div>
    <div id="cancelbutton" class="prefbutton"><a href="#" onClick="document.dataForm.clear()">Cancel</a></div>
  </div>
  <div class="clear"></div>
  </form>

  <!-- <br><br>
  <form name="prefForm" method="POST" action="">
  <div class="prefbar">CyberWeb Preferences</div>
  % if c.devmessage:
     &nbsp;&nbsp;&nbsp;(${c.devmessage})
  %endif
  <div id="preftable">
      % for k,v in c.pref.items():
        <div id="${k}" class="prefrow">
          <div class="prefheader">${k}:</div>
          % if k == 'password':
            <div class="prefvalue"><input type="password" name="${k}" value="${v}"/></div>
          % else:
            <div class="prefvalue"><input type="text" name="${k}" value="${v}"/></div>
          % endif
        </div>
        <div class="clear"></div>
      % endfor
  </div>
  % if c.message:
    <div id="status" class="prefrow">
    <div class="prefbuttons">
    % if c.error:
      <font color="red">${c.message}</font>
    % else:
      <font color="green">${c.message}</font>
    % endif
    </div>
    </div>
  % endif

  <br>
  <div class="prefbuttons">
    <div id="savebutton" class="prefbutton"><a href="#" onClick="document.prefForm.submit()">Save Preferences</a></div>
    <div id="cancelbutton" class="prefbutton"><a href="#" onClick="document.prefForm.clear()">Cancel</a></div>
  </div>
  <div class="clear"></div>
  </form> -->

  </div>
  <br><br>
  <div class="prefbar">Login Statistics</div>
  <div id="infotable">
      % for k,v in c.info.items():
        <div class="prefrow">
          <div class="prefheader">${k}</div>
          <div class="prefvalue">${v}</div>
        </div>
        <div class="clear"></div>
      % endfor
  </div>

  </div>
</%def>
