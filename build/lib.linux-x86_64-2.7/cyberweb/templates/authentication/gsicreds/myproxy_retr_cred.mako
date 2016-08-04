## index.html
<%inherit file="/authentication/authentication.layout.mako"/>

<p>http://localhost:8080/authentication/grid_credentials
<p> /templates/authentication/index.mako
##REMOTE USER: ${session['remote_user']}
##<p>SESSION DATA::${session}
<p>
##REQUEST: ${c.request}<br>
##REQUEST: ${c.request['myproxy_username']}
<hr>
RESULTS: ${c.results}


