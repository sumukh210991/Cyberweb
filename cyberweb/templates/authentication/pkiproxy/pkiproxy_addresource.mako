<%inherit file="./pkiproxy.layout.mako"/>

<%def name="headtags()">
</%def>


<%def name="col2main()">

<h2>ADD Resource:  PKI Credential Management for CyberWeb User: ${c.user}</h2>
<p>
<p> status: ${c.status}
<table>
<h3>PKI Credentials</h3>
<table>
   <tr>
      <td>Account</td><td>Hostname</td>Status</td><td>Date</td>
   </tr>
   <tr> <td>account1</td><td>hostname1</td>Status</td><td>date</td> </tr>
   <tr> <td>account2</td><td>hostname2</td>Status</td><td>date</td> </tr>
   <tr> <td>account3</td><td>hostname3</td>Status</td><td>date</td> </tr>
</table>

<hr>
<%
  session = request.environ['beaker.session']
  g = app_globals
%>
% for k,v,admin in g.menu.find_menu('pkiproxy','index',1):
    <li class=current>IDX1  V: "${v}, K=${k}</li>
% endfor
<hr>
% for k,v,admin in g.menu.find_menu('pkiproxy','index',2):
    <li class=current>IDX2  V: "${v}, K=${k}</li>
% endfor
<hr>
% for k,v,admin in g.menu.find_menu('pkiproxy','index',3):
    <li class=current>IDX3  V: "${v}, K=${k}</li>
% endfor
<hr>

</%def>
