<%inherit file="/2col-left.mako"/>

<%def name="headtags()">
	<link rel="stylesheet" type="text/css" href="/css/ui-lightness/jquery-ui-1.8.17.custom.css" media="screen">
	<link rel="stylesheet" type="text/css" href="/css/showLoading.css" media="screen" />
	
	<script type="text/javascript" src="/js/jquery-1.6.2.js"></script>
	<script type="text/javascript" src="/js/jquery-ui-1.8.17.custom.min.js"></script>
	<script type="text/javascript" src="/js/jquery.showLoading.min.js"></script>
	<script type="text/javascript" src="/js/jquery.dateFormat-1.0.js"></script>
	
	${next.headtags()}
</%def>

<%def name="footer()">
</%def>

<%def name="header()">
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
        % for k,v,admin in g.menu.find_menu('authentication','index',2):
             % if k == g.menu.find_title('authentication','index',2):
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
