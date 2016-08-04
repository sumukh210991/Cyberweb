<%inherit file="/authentication/authentication.layout.mako"/>


<%def name="headtags()">
</%def>


<%def name="col2main()">

<h2>GSI Cred: Del</h2>
<h3>CyberWeb User: ${c.user}</h3>
<p>
<p><b>Current Credentials:

<p>
<h3>GSI Credentials</h3>
<table>
   <tr> <td>Account</td><td>DN</td><td>MyProxy Server</td><td>Credential Info</td><td></td> </tr>
   <tr> <td>account1</td><td>DN1</td><td>MyProxy Server</td><td>Credential1 Info</td><td>[DEL]</td></tr>
   <tr> <td>account2</td><td>DN2</td><td>MyProxy Server</td><td>Credential2 Info</td><td>[DEL]</td></tr>
   <tr> <td>account3</td><td>DN3</td><td>MyProxy Server</td><td>Credential3 Info</td><td>[DEL]</td></tr>
   <tr> <td>account4</td><td>DN4</td><td>MyProxy Server</td><td>Credential4 Info</td><td>[DEL]</td></tr>
   </tr>
</table>

</%def>
