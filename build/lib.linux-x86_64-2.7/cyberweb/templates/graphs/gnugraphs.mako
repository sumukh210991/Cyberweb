## index.html
<%inherit file="/1col.mako"/>

<%def name="col1main()">
<h3>Graphs</h3> 
<img src="/images/parsing.svg" alt="image" style="width: 700px; height: 500px;"/>
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



</blockquote>
</%def>
