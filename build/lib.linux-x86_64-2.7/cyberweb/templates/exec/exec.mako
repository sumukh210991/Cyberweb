<%inherit file="/1col.mako"/>

<%def name="col1main()">
<h3>${c.title}</h3>
<p>

   <table>
   <tr> <td>
  <div class="infobar">MyJobs</div>
  <table>
     <tr align=left valign=top>
        <th>ID</th>
        <th>Job Name</th>
        <th>Status</th>
        <th>Resource</th>
        <th>Submit</th>
        <th>Start</th>
        <th>End </th>
      </tr>
  % for j in c.jobs:
      <tr align=left valign=top>
          <td>${j['ID']}</td>
          <td>${j['Name']}</td>
          <td>${j['Resource']}</td>
          <td>C</td>
          <td>${j['Submit Time']}</td>
          <td>${j['Start Time']}</td>
          <td>${j['End Time']}</td>
      </tr>
  % endfor
  </table>

</%def>

