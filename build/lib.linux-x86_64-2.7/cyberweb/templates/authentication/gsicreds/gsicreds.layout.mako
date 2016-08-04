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
        % for k2,v2,admin in g.menu.find_menu('authentication','index',2):
            % if k2 == g.menu.find_title('authentication','index',2):
                 <li class=current><a href="${v2}">${k2}</a></li>
            % else:
                 <li><a href="${v2}">${k2}</a></li>
                 % if  'gsicreds' in v2 :
                     % for k3,v3,admin in g.menu.find_menu('gsicreds','index',3):
                         % if k3 == g.menu.find_title('gsicreds','index',3):
                             <li class=current><a href="${v3}">Q3${k3}</a></li>
                         % else:
                             <li><a href="${v3}">&nbsp;&nbsp;${k3}</a></li>
                         % endif
                     % endfor
                 % endif
            % endif
            <p>
        % endfor
        </ul>
   </div>
<!--#End Left Menu Navigation Panel -->
</%def>


<p>

${next.body()}
