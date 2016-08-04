<%inherit file="/authentication/authentication.layout.mako"/>

<%def name="headtags()">
	<style>
		.errorStyle{
			margin: 0;
			padding: 1em;
			color: red;
			font-weight: bold;
		}
		
		.formStyle th, .formStyle td{
			border: 0;
		}
		
		.label {
			text-align: right;
		}
	</style>
</%def>

<%def name="col2main()">
  <style type="text/css">
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

  <div style="width:500px;">
  	<h2>Private/Public Key Authentication.</h2>
	  % if not c.current_keys:
	    <br>The public private/key combination allows CyberWeb to SSH to a particular SSH enabled resource
	    <p> on behalf of a user. You must already have access to the resource in order to use this feature.
	    <p> To get started click the button below and CyberWeb will create a key pair for you.
	    <div class="prefbar">Create a new key</div>
	    <form name="dataForm" method="POST" action="">
	    <div class="prefbuttons">
	      <input type="hidden" name="CreateKey" value="True">
	      <div id="savebutton" class="prefbutton"><a href="#" onClick="document.dataForm.submit()">Create key pair</a></div>
	      <div id="cancelbutton" class="prefbutton"><a href="#" onClick="document.dataForm.clear()">Cancel</a></div>
	    </div>
	    <div class="clear"></div>
	    </form>
	  % else:
	    % if c.keymade:
	      <br><font color="green">You have successfully created a public/private key pair.<p></font>
	    % endif
	    <p>
	    <div class="prefbar">Instructions to add a resource.</div>
	    <p>1. Highlight and copy the key below.</p>
	    <form name="pubkey" method="post" action="">  
            <table border=1 style="table-layout:fixed; width:100px">
	        % for i in c.current_keys:
                    <tr><td style="overflow:hidden; width:500px;WORD-BREAK:BREAK-ALL">
                        ${i.public_key}
                    </td></tr>
	        % endfor
            </table>
	  </form>
	    <p>2. Using your current username and password, login to the resource you wish to add.</p>
	    <p>3. Paste the key string you copied in Step 1 into the file ~/.ssh/authorized_keys. If this file does not exist, create it.</p>
C.USERID=  [  ${c.user_id}  ]<br>
	    <div id="accounttable">
	    </div>
	    <br>
	  % endif
	  <h2>Add your key</h2>
	  <form name="addResource" method="post" action="">  
		% if c.message:
			<div class="errorStyle">
			Message:	${c.message}<br/>
			</div>
		% endif
		<table class="formStyle">
			<tr>
				<td class="label"><label>Host: </label></td>
				<td><select name="host">
					    <OPTION VALUE=""></option>
				          % for resource in c.resources:
							<%
									name = resource.name
									if 'longboard' in resource.name:
											name = 'CyberWeb Home'
							%>
							% if c.resource_id == resource.id:
								<OPTION VALUE="${resource.id}" selected="selected">${name}</option>
							% else:
								<OPTION VALUE="${resource.id}">${name}</option>
							% endif
						  % endfor
					</select>
				</td>
			</tr>
			<tr>
				<td class="label"><label>Username: </label></td>
				<td><input type="text" name="user" value="${c.user}"/></td>
			</tr>
			<tr>
				<td class="label"><label>Password: </label></td>
				<td><input type="password" name="password"/></td>
			</tr>
			<tr>
				<td></td>
				<td><input type="submit" name="submit" /></td>
			</tr>
		</table>
	  </form>
	</div>
</%def>
