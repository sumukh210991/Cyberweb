<%inherit file="./gsicreds.layout.mako"/>


<%def name="headtags()">
</%def>


<%def name="col2main()">

<h2>GSI Cred: Del</h2>
<h3>CyberWeb User: ${c.user}</h3>
<p>
<p> status: ${c.status}
<br> gsidir: ${c.gsidir}
<p>
<p><b>Current Credentials:
<p>
<h3>GSI Credentials</h3>
<form action="/gsicreds/gsicred_del_action" method="post">
 <table>
   <tr> <td>Account</td><td>DN</td><td>MyProxy Server</td><td>Credential Info</td><td></td> </tr>
   <tr> <td>account1</td><td>DN1</td><td>MyProxy Server</td><td>Credential1 Info</td><td>[DEL]</td></tr>
   <tr> <td>account2</td><td>DN2</td><td>MyProxy Server</td><td>Credential2 Info</td><td>[DEL]</td></tr>
   <tr> <td>account3</td><td>DN3</td><td>MyProxy Server</td><td>Credential3 Info</td><td>[DEL]</td></tr>
   <tr> <td>account4</td><td>DN4</td><td>MyProxy Server</td><td>Credential4 Info</td><td>[DEL]</td></tr>
   </tr>
</table>
<p>
<input type="text" name="txtone"><br>
<input type="text" name="txttwo"><br>

<input type="submit" value="Delete Credential" name="/gsicreds/gsicred_del_action" />
</form>
<hr>
${c.request_params}
<hr>
 % for k in c.request_params :
     ${k} <br>
  % endfor

</%def>
