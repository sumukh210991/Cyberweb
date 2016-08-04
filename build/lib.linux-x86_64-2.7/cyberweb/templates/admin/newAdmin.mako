<%inherit file="/2col-left.mako"/>

<%def name="headtags()">

	<link rel="stylesheet" type="text/css" href="/css/ui-lightness/jquery-ui-1.8.17.custom.css" media="screen">
	<link rel="stylesheet" type="text/css" href="/css/showLoading.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="/css/admin.css" media="screen">
	
	<script type="text/javascript" src="/js/jquery-1.6.2.js"></script>
	<script type="text/javascript" src="/js/jquery-ui-1.8.17.custom.min.js"></script>
	<script type="text/javascript" src="/js/jquery.showLoading.min.js"></script>
	<script type="text/javascript" src="/js/jquery.dateFormat-1.0.js"></script>
	<script type="text/javascript" src="/js/ajax_post_lib.js"></script>
	<script type="text/javascript" src="/js/newAdmin.js"></script>
	
	<style>
		.col2-left {
			float: left;
			margin: 1em;
			margin-top:3em;
			max-width: 120px;
			overflow-x: auto;
		}
		
		.col2-main {
			margin:1em;
			max-width:80%;
  			min-width:200px;
		}
		
		#leftmenuList li {
			font-family: Verdana, Arial, Helvetica, sans-serif;
			font-size: 12px;
			line-height: 2em;
			list-style: disc outside none;
			display: list-item;
			margin-left: 1em;
		}
	</style>
	
    ${next.headtags()}
</%def>

<%def name="header()">
	
</%def>

<%def name="footer()">
	
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
		<%
			print this_route['controller']
			print this_route['action'] 
		%>
        % for k,v,admin in g.menu.find_menu(this_route['controller'],'groupDetails',2):
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

<%def name="col2main()">
    ${next.col2main()}
</%def>