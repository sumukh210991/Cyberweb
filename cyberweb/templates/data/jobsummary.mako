<%inherit file="/1col.mako"/>

<%def name="col1main()">
<h3>${c.title}</h3>
<form action="/data/jobsummary" method="post">
<blockquote>
<!--- _states = ['setup','queued', 'running', 'idle', 'paused', 'finished', 'error', 'cancelled', 'timeout', 'unknown'] --->
<blockquote>
     <input type="submit" name="jobsummary" value="MyJobs" />
</blockquote>
  <table>
     <tr align=left valign=top>
        <th>ID</th>
        <th>Job Name</th>
        <th>Status</th>
        <th>Resource</th>
        <th>Submit Time</th>
        <th>Start Time</th>
        <th>End Time</th>
      </tr>
  % for job in c.jobs:
      <tr align=center valign=top>
          <td>${job['ID']}</td>
          <td>${job['Name']}</td>
          <td>${job['StatusKey']} </td>
          <td>${job['Resource']}</td>
	  <td>${job['Submit Time']}</td>
	  <td>${job['Start Time']}</td>
	  <td>${job['End Time']}</td>
      </tr>
  % endfor
  </table>
</blockquote>

<blockquote>
      Status Keys:[
      % for key, value in sorted(c.jobstateheaders.iteritems(), key=lambda (k,v): (v,k)):
          ${key}=${value} ,
      % endfor
      ] <br>
   </blockquote>
         <input type="hidden" name="jobname" value="${c.jobname}" />
</form>
</%def>
