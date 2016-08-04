<%inherit file="./gsicreds.layout.mako"/>

<%def name="headtags()">
</%def>

<%def name="col2main()">

<h2>GSI Cred: Stat </h2>
<h3>CyberWeb User: ${c.user}</h3>
<p>
<p> status: ${c.status}
<br> gsidir: ${c.gsidir}
<p>
<br>Listing of all credentials and the status/last update 
<table>
   <tr> <td>account</td><td>DN</td><td>MyProxy Server</td><td>Credential Info</td><td>Date</td> </tr>
   <tr> <td>account1</td><td>DN1</td><td>MyProxy Server</td><td>Credential1 Info</td><td>Date</td> </tr>
   <tr> <td>account2</td><td>DN2</td><td>MyProxy Server</td><td>Credential2 Info</td><td>Date</td> </tr>
   <tr> <td>account3</td><td>DN3</td><td>MyProxy Server</td><td>Credential3 Info</td><td>Date</td> </tr>
</table>
</%def>
