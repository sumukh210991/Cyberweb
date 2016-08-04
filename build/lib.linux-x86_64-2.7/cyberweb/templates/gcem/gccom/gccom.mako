<%inherit file="/1col.mako"/>

<%def name="col1main()">
<h3>${c.title}</h3>
<p>
<form action="/gccom/jobmonitor" method="post">
<blockquote>
<input type="submit" name="jobmonitor" value="Update My Jobs" />
</blockquote>
<blockquote>
      <table >
          <tr align=left valign=top>
             <!--<th>ID</th>-->
             <th>Job Name</th>
             <th>Status</th>
             <th>Resource</th>
             <th>Submit Time</th>
             <th>Start Time</th>
             <th>End Time</th>
          </tr>
   % if c.jobs:
      % for job in c.jobs:
          <tr align=left valign=top>
             <td>${job['Name']}</td>
             <td>${job['StatusKey']}</td>
             <td>${job['Resource']}</td>
             <td>${job['Submit Time']}</td>
             <td>${job['Start Time']}</td>
             <th>Etime</th>
          </tr>
      % endfor
   % else:
          <tr align=left valign=top>
             <th> </th> <th> </th> <th> </th> <th> </th> <th> </th> <th> </th> <th> </th>
          </tr>
   % endif

      </table>
	<pre><blockquote>
      Status Keys:[ 
       for key, value in sorted(c.jobstateheaders.iteritems(), key=lambda (k,v): (v,k)):
          {key}={value} ,
       endfor
      
      ] </pre><br>
   </blockquote>
</blockquote>


</%def>
