<%inherit file="/2col-left.mako"/>

<%def name="headtags()">
</%def>

<%def name="footer()">
</%def>

<%def name="header()">
</%def>

<%def name="footer()">
</%def>

<%def name="col2main()">
    ${self.col2main()}
</%def>

<%def name="col2left()">
<%
  session = request.environ['beaker.session']
  g = app_globals
  c = tmpl_context
  this_route = request.environ['pylons.routes_dict']
%>
<!--#Implement sub_menu as a Left Menu Navigation Panel -->
    <div id="leftmenu">
		<ul id="leftmenuList">
        % for k,v,admin in g.menu.find_menu(this_route['controller'],this_route['action'],2):
             % if k == g.menu.find_title(this_route['controller'],this_route['action'],2):
                 <li class=current><a href="${v}">${k}</a></li>
             % else:
                 <li><a href="${v}">${k}</a></li>
             % endif
        % endfor
        </ul>
	</div>
<!--#End Left Menu Navigation Panel -->
</%def>


<p>

${next.body()}
