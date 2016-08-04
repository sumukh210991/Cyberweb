<%inherit file="/authentication/authentication.layout.mako"/>


<%def name="headtags()">
</%def>


<%def name="col2main()">

<h2>GSI Cred: Renew </h2>
<h3>CyberWeb User: ${c.user}</h3>
<p>
<p>List All Current Credentials
<p>All certificates should be autorenewed; if there is a problem, then the status 
will be set.
<p>
<table>
   <tr> <td>GSI Acct ID</td><td>DN</td><td>MyProxy Server</td><td>Credential Status</td><td>Renew Date</td> </tr>
   <tr> <td>GSI Acct1 ID</td><td>DN</td><td>MyProxy Server</td><td>Credential1 Status</td><td>Renew Date</td> </tr>
   <tr> <td>GSI Acct2 ID</td><td>DN</td><td>MyProxy Server</td><td>Credential2 Status</td><td>Renew Date</td> </tr>
   <tr> <td>GSI Acct3 ID</td><td>DN</td><td>MyProxy Server</td><td>Credential3 Status</td><td>Renew Date</td> </tr>
</table>


</%def>
