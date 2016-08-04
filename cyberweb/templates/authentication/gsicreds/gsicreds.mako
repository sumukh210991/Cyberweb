<%inherit file="./gsicreds.layout.mako"/>

<%def name="headtags()">
</%def>


<%def name="col2main()">

<h2>GSI Credential Management for CyberWeb User: ${c.user}</h2>
<p>
<p> c.gsidir: ${c.gsidir}
<p> c.status: ${c.status}
<table>
   <tr>
      <td>account</td><td>DN</td><td>MyProxy Server</td><td>Credential Info</td>
   </tr>
   <tr>
      <td>account</td><td>DN</td><td>MyProxy Server</td><td>Credential Info</td>
   </tr>
   <tr>
      <td>account</td><td>DN</td><td>MyProxy Server</td><td>Credential Info</td>
   </tr>
   <tr>
      <td>account</td><td>DN</td><td>MyProxy Server</td><td>Credential Info</td>
   </tr>
</table>
<p>
<p> Note: several of the functions on left menu might be put into one page for  credential management
(add/del/modify).

<hr>
<%
  session = request.environ['beaker.session']
  g = app_globals
%>
% for k,v,admin in g.menu.find_menu('gsicreds','index',1):
    <li class=current>IDX1  V: "${v}, K=${k}</li>
% endfor
<hr>
% for k,v,admin in g.menu.find_menu('gsicreds','index',2):
    <li class=current>IDX2  V: "${v}, K=${k}</li>
% endfor
<hr>
% for k,v,admin in g.menu.find_menu('gsicreds','index',3):
    <li class=current>IDX3  V: "${v}, K=${k}</li>
% endfor
<hr>

</%def>
