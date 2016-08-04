<%inherit file="/exec/exec.layout.2col.mako"/>

<%def name="col2main()">
<h3> Cyberweb Execution Services: Testing simple Unix commands with GSI authentication.</h3>
<br>
<form action="/exec/demo_cmd_gsi_action" method="post">
<table border=0>
    <tr> 
    <td><b>Select Test Script</b></td>
    <td><b>Select Host:</b></td>
    </tr>
    <tr valign=top>
      <td width=200 valign=top>
        <input type="radio" name="script" value="hostinfo" checked>HostInfo + GSI auth<br>
        <input type="radio" name="script" value="ls">  Dir Listing<br>
        <input type="radio" name="script" value="qstat">  Queue Status<br>
      </td>
           <td>
       <% 
           res = []
           for resource  in c.resources:
              res.append(resource)
           endfor
        %>

       <input type="radio" name="hostname" value="${res[0]}" checked>&nbsp;&nbsp;&nbsp;${res[0]}<br>
       % for r in res[1:] :
            <input type="radio" name="hostname" value="${r}">&nbsp;&nbsp;&nbsp;${r} <br>
       % endfor
        
      </td>
 
    </tr>
    <tr>
    <td colspan=2 align=left><input type="submit" name="demo_cmd_gsi_form" value="Run Test Script" /></td>
    </tr>
</table>
</form>
<hr>
<h3><b>Results:</h3>
<b>Host:</b>  ${c.hostname}
<%
    s0 = c.results
    s1 = s0.splitlines( )
%>
% for l in s1 :
    <br>${l}
% endfor

<hr>
${s1}
</%def>

