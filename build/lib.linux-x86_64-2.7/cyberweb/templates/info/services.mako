## index.html
<%inherit file="/1col.mako"/>

<%def name="col1main()">
<h3>CyberWeb Information Services</h3>
<br>
<table>
   <tr id="header">
      <td>Resource</td>
     % for i in c.services:
      <td>${i[0]}</td>
     % endfor
   </tr>
   % for k,v in c.resources.items():
   <tr>
      <td>${k}</td>
     % for i in v:
       % if i == 1:
          <td><img class="filesprite" src="/images/checkmark.png"/></td>
       % else:
          <td></td>
       % endif
     % endfor
   </tr>
   % endfor
</table>
<div style="margin-bottom:40px" />
</%def>
