<%
  from authkit.authorize.pylons_adaptors import authorized
  from cyberweb.lib import auth
  
  session = request.environ['beaker.session']
  g = app_globals
  c = tmpl_context
  this_route = request.environ['pylons.routes_dict']
%>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">

  <head>
    <title>${g.title}</title>
	<meta name="Copyright" content="Copyright (c) 2009 Advanced Computing Environments Lab, SDSU">
    <meta name="Author" content="Advanced Computing Environments Lab" >
    <meta name="Keywords" content="cyberweb, python, pylons, grid computing, computational science, sdsu, ace, webservices">

	<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/combo?3.0.0/build/cssreset/reset-min.css&3.0.0/build/cssfonts/fonts-min.css&3.0.0/build/cssgrids/grids-min.css&3.0.0/build/cssbase/base-min.css">
	<link rel="stylesheet" type="text/css" href="/base.css">

	<script type="text/javascript" src="/jquery.js"></script>
	<script type="text/javascript" src="/js/jquery-1.6.2.js"></script>
	<script type="text/javascript" src="/js/jquery.ui.core.js"></script>
	<script type="text/javascript" src="/jquery.tablesorter.js"></script>
	<script type="text/javascript" src="/jquery.form.js"></script> 
	
	<link rel="shortcut icon" href="/favicon.ico">

	<script type="text/javascript">
	  $(document).ready(function() {
		//Show dropdown bar
		setTimeout("$('#messagebar').fadeOut('slow')",5000);
		if($("#myTable") && $("#myTable").tablesorter){
			$("#myTable").tablesorter();
		}
	  });
	</script>

	${next.headtags()}
  </head>

  <body>
	<!--#Navigation bar-->
	<div id="navbar">
	  <ul id="tabs">
		% for k,v,admin in g.menu.get_menu():
		  % if k == 'CyberWeb':
				<li> <a href="/"> <h1><span class="dark">O</span>cean</h1> </a> </li> 
				<li> <a href="/"> <h1><span class="dark">S</span>cience</h1> </a> </li>
				<li> <a href="/"> <h1><span class="dark">E</span>ducation</h1> </a> </li>
				<li> <a href="/"> <h1><span class="dark">P</span>ortal</h1> </a> </li>
		  % elif admin and not authorized(auth.is_admin):
				<noop>
		  % elif k == g.menu.find_title(this_route['controller'],this_route['action'],0):
				<li class=current><a href="${v}">${k}</a></li>
		  % else:
				<li><a href="${v}">${k}</a></li>
		  % endif
		% endfor
	  </ul>
	  <ul id="rightTabs">
		% if session.has_key('user'):
                    <li><a href="/user">${session['user']}</a><li>
                    <li><a href="/signout">Logout</a></p></li>
		% else:
                  <li><a href="/signin">Login</a></p></li>
                  <li><a href="/signup">Signup</a></li>
		% endif
	  </ul>
	</div>
	<!--end navbar-->
	<div id="subnav">
	  <ul id="subnavTabs">
			% for k,v,admin in g.menu.find_menu(this_route['controller'],this_route['action'],1):
			  % if k == g.menu.find_title(this_route['controller'],this_route['action'],1):
				<li class=current><a href="${v}">${k}</a></li>
			  % else:
				<li><a href="${v}">${k}</a></li>
			  % endif
	        % endfor
	  </ul>
	</div>
	<!--end subnavbar-->
	<!--#End Navigation Bar-->

	% if c.status == 1:
	  <div id="messagebar">${c.messagebar_text}</div>
	% else:
	  <div id="messagebar" style="visibility:hidden"></div>
	% endif

	<!--#Body-->
        <div id="content">
	  ${next.body()}
	</div>
	<!--#End Body-->

	<!--#Footer-->
	<div id="footer">

 	   <div class="footer-left">
		Powered by: <h1 style="color: black;">cyber<span class="dark">Web</span></h1>
	   </div>
	   <div class="footer-right">
              <p>Brought to you by the faculty and students of the ACE Lab</p>
              <p>&copy; 2011-2012 San Diego State University ACE Lab</p>
              <p>Contact:  <a href="mailto:info at acel.sdsu.edu">info at acel.sdsu.edu</a></p>
	   </div>
	   <div class="footer-center"> </div>

	</div>
	<!--#End Footer-->

  </body>
</html>
