<%inherit file="/exec/exec.layout.2col.mako"/>

<%def name="col2main()">
<h3> Cyberweb Execution Services: 
<br>Testing Basic Job creation and management (non Jodis).</h3>
<br>CyberWeb User: ${c.cwuser}
<br>CyberWeb Group:
<br> 
<blockquote>
step 1: pick a command; pick a machine <br>
step 2: create the job <br>
step 3: start the job <br>
step 4: del the job <br>
step 5: view the job output <br>

<form action="" method="post">
<table border=0>
    <tr>
      <td><b>Select Test Script</b></td>
      <td><b>Select Host:</b></td>
    </tr>
    <tr valign=top>
      <td width=200 valign=top>
       % for i in c.command_options:
           <% checked = "checked" if i[0] == c.command else "" %>
          <input type="radio" name="command" value="${i[0]}" ${checked}>&nbsp;&nbsp;&nbsp;${i[1]}<br>
       % endfor
      </td>
      <td>
       % for i in c.resources:
           <% checked = "checked" if i == c.hostname else "" %>
          <input type="radio" name="hostname" value="${i}" ${checked}>&nbsp;&nbsp;&nbsp;${i}<br>
       % endfor
      </td>
    </tr>
    <tr>
    <td colspan=2 align=left>
	<input type="radio" name="job" value="add">&nbsp;&nbsp;&nbsp;Add a new job
        <input type="radio" name="job" value="add">&nbsp;&nbsp;&nbsp;Run Remote Command
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
  <tr><td align=left><h4>Jobname:  </h4></td> <td> ${c.jobname}</td></tr>
  <tr><td align=left><h4>JobID:  </h4></td> <td> ${c.jobid}</td></tr>
  <tr><td align=left><h4>Hostname:  </h4></td> <td> ${c.hostname}</td></tr>
  <tr><td align=left><h4>Command:  </h4></td> <td> ${c.command}</td></tr>
  <tr><td align=left valign=top><h4>Results: </h4></td> 
  <td>
  % for i in c.results :
    <br>${i}
  % endfor
  </td> </tr>
  </table>
%endif
</%def>
