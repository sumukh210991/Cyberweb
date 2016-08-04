<%inherit file="/exec/exec.layout.2col.mako"/>

<%def name="col2main()">
<h3> Cyberweb Execution Services for ${c.cwuser}.
<br>Testing simple Unix commands running on local web service machine, with no authentication.</h3>
<br>
<form action="/exec/demo_cmd_action" method="post">
<table border=0>
    <tr> 
    <td><b>Select Test Script</b></td>
    </tr>
    <tr>
      <td width=200>
        <input type="radio" name="script" value="date.local" checked >  Date<br>
        <input type="radio" name="script" value="ls.local">  Dir Listing<br>
      </td>
    </tr>
    <tr>
    <td  align=left><input type="submit" name="demo_cmd_form" value="Run Test Script" /></td>
    </tr>
</table>
</form>
<hr>
<%
    try: 
        x=c.jobid
    except Exception, e: 
        c.jobid=0

    try: 
        s=c.results.split('||')
    except Exception, e: 
        s=[] 

%>

<h3><b>Job Submitted: ${c.jobid}</h3>
<h3><b>Results:</h3>

   %for l in s :
      <br>${l}
   % endfor
   
</%def>