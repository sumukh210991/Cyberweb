## index.html
<%inherit file="/1col.mako"/>

<%def name="col1main()">
<h3>${c.title} </h3>

<blockquote>
Last login: ${c.info['Last login']} &nbsp;&nbsp;from ip address:  ${c.info['from']}
<p>
<h3>Messages</h3>
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
      No messages. <br>
  % endif

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
<br>
% if len(c.passwordLessAccount):
<h3> Password less SSH resource is: </h3>
<ul>
	% for index, item in enumerate(c.passwordLessAccount):
	<li>  ${item['hostname']} resource connected through ${item['name']} account. </li>
	% endfor
</ul>
% else:
<h3>You have no passwordless SSH connected resources.</h3>
% endif
</blockquote>
</%def>
