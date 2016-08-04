<%inherit file="/exec/exec.layout.2col.mako"/>

<%def name="col2main()">
<h3> Cyberweb Execution Services: Run Interactive Unix commands on remote machine</h3>
<br>
<form action="/exec/unix_cmd_action" method="post">
<table border=0>
    <tr> 
    <td><b>Host:</b></td>
    <td width=200>
        <input type="radio" name=hostname value="dolphin.sdsu.edu" checked>  SDSU:  dolphin.sdsu.edu<br>
        <input type="radio" name=hostname value="anthill.sdsu.edu">  SDSU:  anthill.sdsu.edu<br>
        <input type="radio" name=hostname value="pipeline3.sdsu.edu">  SDSU:  pipeline3.sdsu.edu<br>
        <input type="radio" name=hostname value="tg-login.ncsa.teragrid.org" >  NCSA:  tg-login.ncsa.teragrid.org<br>
      </td>
    </tr>
    <tr> 
    <td valign=top><b>Auth Service:</b></td>
    <td width=200>
        <input type="radio" name=auth value="gsissh" checked> GSISSH &nbsp;&nbsp;&nbsp;
        <input type="radio" name=auth value="ssh" > SSH<br>
      </td>
    </tr>
    <tr> 
    <td><b>User Account:</b></td> <td width=200> <input type="text" name=username value="carny">  
      </td>
    </tr>
    <tr> 
    <td valign=top><b>Command:</b></td> <td width=200> <input type="text" name=interactcmd value="/bin/ls">  
      </td>
    </tr>
    <tr> 
    <td valign=top><b>Args:</b></td> <td width=200> <input type="text" name=interactargs value="-al">  
      </td>
    </tr>

    <tr>
    <td colspan=2 align=left><input type="submit" name="unix_cmd_form" value="Run Test Script" /></td>
    </tr>
</table>
</form>
<hr>
<h3>Output:</h3> 
<br><b>Results:</b>
<br>${c.results}
<%
    o=c.results
%>
<br>
<br>

</%def>
#
