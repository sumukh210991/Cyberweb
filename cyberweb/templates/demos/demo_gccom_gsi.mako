<%inherit file="/exec/exec.layout.2col.mako"/>

<%def name="col2main()">
<h3> Cyberweb Execution Services: Testing GCOM-NG with GSI authenticationi to TeraGrid Host.</h3>
<br>
<form action="/exec/demo_cmd_gsi_action" method="post">
<table border=0>
    <tr> 
    <td><b>Select Test Script</b></td>
    <td><b>Select Host:</b></td>
    </tr>
    <tr valign=top>
      <td width=200 valign=top>
        <input type="radio" name="script" value="rungccom.gsi.py ">  Run GCOM<br>
      </td>
      <td>
<%
         res = []
         res.append("tg-login.ncsa.teragrid.org")
         res.append("tg-login.frost.ncar.teragrid.org")
%>
        % for r in res :
            <input type="radio" name="hostname" value="${r}">${r} <br>
        % endfor
            <input type="radio" name="hostname" value="${r}" checked>${r} <br>
      </td>
    </tr>
    <tr>
    <td colspan=2 align=left><input type="submit" name="demo_gccom_gsi_form" value="Run Test Script" /></td>
    </tr>
</table>
</form>
<hr>
<h3>Output:</h3> 
<b>Host:</b>  ${c.hostname}
<br><b>Script:</b>  ${c.script}
<br><b>Results:</b>
<br>${c.results}
<%
    o=c.results
%>
<br>
<br>

</%def>
#
