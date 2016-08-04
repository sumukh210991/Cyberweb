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
            <td>${j[k]}</td>
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

