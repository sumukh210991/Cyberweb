## index.html
<%inherit file="/1col.mako"/>

<%def name="col1main()">
  <style type="text/css">
    .infobar {
      background:#cccccc;
      padding-left:2px;
      margin-bottom:2px;
    }

    table, td, th {
      border:1px solid black;
    }
    th {
      vertical-align:top;
    }
    td {
      vertical-align:top;
    }
  </style>

<h3>MyCyberWeb:  ${c.title} </h3>
<hr>

<table width=90%>
   <tr>
   <!----------------  LEFT COL  ------------------->
   <td>
      <table style="width:350px">
         <tr style="text-align:top;"> <td>
            <div class="infobar">My Information</div>
            <br>Last login: ${c.info['Last login']} &nbsp;&nbsp;
            <br>from ip address:  ${c.info['from']}
         </td> </tr>
         <tr> <td>
             <div class="infobar">My Groups & Projects</div>
             No group information available at this time.
         </td> </tr>
         <tr> <td>
            <div class="infobar">My Remote Accounts </div>
              <% l = len(c.user_resources ) %>
              [length(c.user_resources)] = [- ${l} -]  <br>
              <hr>
              % if l == 0 :
                  You currently have no SSH connected resources.<br>
                  To add compute resource accounts, see MyCyberWeb-->Authentication. 
              % else:
                  % for index, item in enumerate(c.user_resources):
                      &nbsp;&nbsp;${item['account_name']}  @ ${item['hostname']} <br>
                  % endfor
              % endif
         </td> </tr>
         <tr> <td>
            <div class="infobar">Recent Messages </div>
            % if len(c.messages):
               <table>
                  <tr>
                     % for j in c.messageheaders:
                        <th>${j}</th>
                     % endfor
                  </tr>
                  % for i in c.messages:
                     <tr>
                        % for j in c.messageheaders:
                           % if i.has_key(j):
                              <td>${i[j]}</td>
                           % else:
                              <td></td>
                           % endif
                        % endfor
                     </tr>
                  % endfor
               </table>
            % else:
                 &nbsp;&nbsp;No messages. 
            % endif
            [More >]
         </td> </tr>
      </table>
   </td>

   <!----------------  RIGHT COL  ------------------->
   <td>
      <table>
      <tr align=left valign=top> <td>
         <div class="infobar">MyJobs</div>
      </td></tr>
      <tr align=left valign=top> <td>
         <form action="/user" method="post">
         <input type="submit" name="jobsummary" value="Update Jobs" />
         </form>
      </td></tr>
      <tr align=left valign=top><td>
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
<%
        sort_on = "Name"
        jsort = [(dict_[sort_on], dict_) for dict_ in c.jobs]
        jsort.sort()
        sorted_jobs = [dict_ for (key, dict_) in jsort]
               ##% for job in c.jobs:
%>
               % for job in reversed(sorted_jobs):
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

         </td> </tr>
         <tr align=left valign=top>
            <td>
            <div class="infobar">My Resources & Services</div>

      </td> </tr>
      </table>


   <!------- end right column -->
   </td> </tr>
   <!------- end main table  ----->
</table>

<%
	sort_on = "Name"
	jsort = [(dict_[sort_on], dict_) for dict_ in c.jobs]
	jsort.sort()
	sorted_jobs = [dict_ for (key, dict_) in jsort]
%>
<hr>
===========================================================<br>
% for j in reversed(sorted_jobs):
JOB: ${j['Name']} <br>
% endfor
<hr>
===========================================================<br>
</%def>
