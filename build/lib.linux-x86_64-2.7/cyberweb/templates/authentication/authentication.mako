<%inherit file="/authentication/authentication.layout.mako"/>


<%def name="headtags()">
</%def>


<%def name="col2main()">

<h2>Authentication Credential Summary for CyberWeb User: ${c.user}</h2>
<p>
<h3>PKI Credentials</h3>
<table>
   <tr>
      <td>Account</td><td>Hostname</td>Status</td><td>Date</td>
   </tr>
   <tr> <td>account1</td><td>hostname1</td>Status</td><td>date</td> </tr>
   <tr> <td>account2</td><td>hostname2</td>Status</td><td>date</td> </tr>
   <tr> <td>account3</td><td>hostname3</td>Status</td><td>date</td> </tr>
</table>
<p>
<h3>GSI Credentials</h3>
<table>
   <tr> <td>Account</td><td>DN</td><td>MyProxy Server</td><td>Credential Info</td> </tr>
   <tr> <td>account1</td><td>DN1</td><td>MyProxy Server</td><td>Credential1 Info</td> </tr>
   <tr> <td>account2</td><td>DN2</td><td>MyProxy Server</td><td>Credential2 Info</td>
   <tr> <td>account3</td><td>DN3</td><td>MyProxy Server</td><td>Credential3 Info</td>
   <tr> <td>account4</td><td>DN4</td><td>MyProxy Server</td><td>Credential4 Info</td>
   </tr>
</table>
</%def>
