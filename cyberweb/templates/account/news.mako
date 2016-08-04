<%inherit file="/layout.mako"/>

<%def name="headtags()">
	<script type="text/javascript" src="http://jqueryui.com/latest/jquery-1.3.2.js"></script>
</%def>

<%def name="footer()">
</%def>


<div class="col1-main">

  <div id="newsandmessages">
        <h3>News and Messages</h3>
  <%
    cnt=0
    context.write('<table class="d0">')
    for m in c.messages:
       if ( (cnt % 2) == 0 ):
          context.write('<tr class="d0">')
          context.write('<td width=100><mfd0>' + m["date"] + ': </mfd1> </td><td> </mfd0><mf0>' + m["message"] + '</mf0</td>' )
          context.write('</tr>')
       else:
          context.write('<tr class="d1">')
          context.write('<td width=100><mfd1>' + m["date"] + ': </mfd1> </td><td> <mf1>' + m["message"] + '</mf1></td>' )
          context.write('</tr>')
       endif
       cnt=cnt+1
    endfor
    context.write("</table>")
  %>  
  </div>



</div>
