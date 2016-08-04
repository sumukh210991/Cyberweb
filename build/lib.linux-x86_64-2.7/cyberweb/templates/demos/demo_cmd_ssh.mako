<%inherit file="/exec/exec.layout.2col.mako"/>

<%def name="col2main()">
<h3> Cyberweb Execution Services: 
<br>Testing simple Unix commands with passwordless SSH authentication.</h3>
<br>CyberWeb User: ${c.cwuser}
<br>CyberWeb Group:
<br> 
<form action="" method="post">
<table border=0>
    <tr>
      <td><b>Select Test Script</b></td>
      <td><b>Select Host:</b></td>
    </tr>
    <tr valign=top>
      <td width=200 valign=top>
       <% cnt=0 %>
       % for i in c.command_options:
          <% checked = "checked" if cnt == 0 else "" %>
          <input type="radio" name="command" value="${i[0]}" ${checked}>&nbsp;&nbsp;&nbsp;${i[1]}<br>
          <% cnt=cnt+1 %>
       % endfor
      </td>
      <td>
          <% cnt=0 %>
          % if  len(c.resources.items()) == 0:
              You currently have SSH connected resources.<br>
              To add compute resource accounts, see MyCyberWeb-->Authentication.
          % else:
              % for r_id, r in c.resources.items():
                   <% checked = "checked" if cnt == 0 else "" %>
                   <input type='radio' name='hostname' value='${r_id}' ${checked}>&nbsp;&nbsp;&nbsp;${r['hostname']}<br>
             <% cnt=cnt+1 %>
             % endfor
          %endif
      </td>
    </tr>
    <tr>
    <td colspan=2 align=left><input type="submit" value="Run Remote Command" /></td>
    </tr>
</table>
</form>

% if c.state:
  <table>
  <tr><td colspan=2><h3>Output:</h3></td></tr>
  <tr><td align=left><h4>Host:  </h4></td> <td> ${c.hostname}</td></tr>
  <tr><td align=left><h4>Host_name:  </h4></td> <td> ${c.hostname_name}</td></tr>
  <tr><td align=left><h4>Command:  </h4></td> <td> ${c.command}</td></tr>
  <tr><td align=left valign=top><h4>Results: </h4></td> 
  <td>
  % for res in c.results:
     ${res} <br>
  % endfor
  </td> </tr>
  </table>
%endif
</%def>
