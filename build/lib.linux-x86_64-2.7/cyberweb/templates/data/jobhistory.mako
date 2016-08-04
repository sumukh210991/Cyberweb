<%inherit file="/2col-left.mako"/>

<%def name="headtags()">
</%def>

<%def name="header()">
</%def>

<%def name="footer()">
</%def>

<%def name="col2left()">
  <%
      # to add new navigation menu item just copy a line and modify the first action,
      # When adding a new menu column. place it in singular. (i.e. when adding users, add "user")
      # The code will check the plural as well
      menulist = {
                    'jobhistory': [('all','View All'),('queued','Pending'),('running','Running'),('finished','Finished'),('error','Crashed')],
                }
      a = ''
      arr = menulist.keys()
      for i in arr:
          if c.current_subnavtab.find(i) > -1 or c.current_subnavtab.find(i+'s') > -1:
             a = i
      menu = menulist[a] if menulist.has_key(a) else dict()
  %>

  % for k,v in menu:
    <div class=leftnav><a href="/data/jobhistory/${k}" value="${k}" >${v}</a></div>
  % endfor
</%def>

<%def name="col2main()">
  <%
   i = c.list.capitalize()
   ilow = i.lower()
  %>

  <br>
  <h3>${i} Jobs</h3>
  % if len(c.jobs):
  <br>
  ${c.jobs.pager('$link_previous ~2~ $link_next')}
  <table>
    <tr>
      <th>ID</th>
      <th>Name</th>
      <th>Service</th>
      <th>Resource</th>
      % if c.list == 'all':
        <th>Status</th>
      % endif
      <th>Submit Time</th>
      <th>Start Time</th>
      <th>End Time</th>
      <th>Results</th>
    </tr>
    % for j in c.jobs:
	 <%
	 	submit_time = j.submit_time.strftime("%m/%d/%y %H:%M:%S") if j.submit_time else ''
	 	start_time = j.start_time.strftime("%m/%d/%y %H:%M:%S") if j.start_time else ''
	 	end_time = j.end_time.strftime("%m/%d/%y %H:%M:%S") if j.end_time else ''
		status = h.JobState.get_name(j.state)
		if not status:
		  status = ''
	 %>

        <tr>
         <td><a href="#" onclick="window.open('/data/getresults/${j}','Results:${j}','width=400,height=300,toolbar=no,location=no,directories=no,status=no,menubar=no')">${j}</a></td>
         <td>${j.name}</td>
         <td>${j.service.service.name}</td>
         <td>${j.service.resource.name}</td>
       % if c.list == 'all':
         <td>${status}</td>
       % endif
         <td>${submit_time}</td>
         <td>${start_time}</td>
         <td>${end_time}</td>
	  % if status == 'finished' and j:
         <td><a href="#" onclick="window.open('/data/jobviewer/${j}','Job results','width=500,height=650,toolbar=no,location=no,directories=no,status=no,menubar=no')">Results</a></td>
	  % else:
         <td></td>
	  % endif
        </tr>
    % endfor
  </table>
  ${c.jobs.pager('$link_previous ~2~ $link_next')}
  % else:
      No jobs ${ilow}.<br>
  % endif
</%def>
