<%inherit file="/1col.mako"/>

<%def name="col1main()">
  <style type="text/css">
    .infobar {
      background:#cccccc;
      padding-left:2px;
      margin-bottom:2px;
    }

    table, td, th, thc,tdc {
      border:0px solid black;
    }
    th {
      vertical-align:top;
      text-align:left; 
    }
    td {
      vertical-align:top;
      text-align:left; 
    }
    thc {
      vertical-align:top;
      text-align:center;
    }
    tdc {
      vertical-align:top;
      text-align:center;
    }
  </style>

<h3>${c.title}</h3>
<form action="/data/jobmonitor" method="post">
<blockquote>
<input type="submit" name="jobmonitor" value="Update My Jobs" />
</blockquote>
<blockquote>
      <table >
          <tr align=left valign=top>
             <th>ID</th>
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
	     <td>${job['ID']}</td>
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
   <blockquote>
      Status Keys:[ 
      % for key, value in sorted(c.jobstateheaders.iteritems(), key=lambda (k,v): (v,k)):
          ${key}=${value} ,
      % endfor
      ] <br>
   </blockquote>
</blockquote>


<input type="hidden" name="jobname" value="${c.jobname}" />
</form>
</%def>
