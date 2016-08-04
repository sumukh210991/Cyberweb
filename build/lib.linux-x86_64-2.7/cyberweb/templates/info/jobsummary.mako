<%inherit file="/1col.mako"/>

<%def name="col1main()">
<h3>${c.title}</h3>
<p>
% for i in ['Queued','Running','Finished','Crashed']:
  <%
   v = c.jobs[i]
   ilow = i.lower()
   %>
  <br>
  <h3>${i} Jobs</h3>
  % if len(v):
  <table>
    <tr>
    % for j in c.jobheaders:
        <th>${j}</th>
    % endfor
    </tr>
    % for j in v:
        <tr>
        % for k in c.jobheaders:
          % if j.has_key(k):
            % if k == 'ID':
            <td><a href="#" onclick="window.open('/data/getresults/${j[k]}','Job results','width=400,height=300,toolbar=no,location=no,directories=no,status=no,menubar=no')">${j[k]}</a></td>
            % else:
            <td>${j[k]}</td>
            % endif
          % else:
            <td></td>
          % endif
        % endfor
        </tr>
    % endfor
  </table>
  % else:
      No jobs ${ilow}.<br>
  % endif
% endfor

</%def>

