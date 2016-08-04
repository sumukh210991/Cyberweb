<%inherit file="/authentication/authentication.layout.mako"/>

<%def name="headtags()">
</%def>

<%def name="col2main()">

#####
## Check for existing proxy: At the command line, type grid-proxy-info. If you already have a proxy, you can start computing. If you receive an error saying that you do not have a temporary proxy, then continue below. (If this is your first time logging in to a TeraGrid resource, you can skip this step.)
## Create certificate proxy: Run myproxy-logon -l <username> You will get a prompt to enter your MyProxy passphrase. Use the TeraGrid-wide (Portal) username and password that you received in your packet for this step.
## Verify proxy: Run grid-proxy-info again.
#####
<h2>GSI Cred: Create </h2>
<h3>CyberWeb User: ${c.user}</h3>
<%
      emsg =  c.errmessage.split('.') 
      context.write('<p><font color=red>')
      context.write('<b>MyProxy Login Error:</b><br>')  
      context.write('</font>')
      for el in emsg[0:len(emsg)-1]:
         a = el.split(':')
         context.write('&nbsp;&nbsp;&nbsp<em>'+ str(a[1]) + '</em><br>')
      endfor
      context.write('<p>')  
      c.errmessage = '' 
%>
  <form action="/gsicreds/myproxy_logon_action" method="post">

  <table border=1>
  <tr>
     <td>MyProxy Server:</td>
     <td><input type="text" name="myproxy_hostname" value="myproxy.teragrid.org"></td>
  </tr>
  <tr>
     <td>Grid Credential Username:&nbsp;&nbsp; </td>
     <td><input type="text" name="myproxy_username" value=""> </td>
  </tr>
  <tr>
     <td>Certificate Passphrase:</td>
     <td><input type="password" name="myproxy_password" value=""></td>
  </tr>
  <tr>
     <td>MyProxy Port:</td>
     <td><input type="text" name="myproxy_port" value="7512"></td>
  </tr>
  <tr>
     <td>Proxy Lifetime (hours):<br>
   Lifetime of proxies delegated by<br> the server (default 12 hours)
    </td>
     <td><input type="text" name="myproxy_lifetime" value="8760"></td>
  </tr>
<table>

<input type="submit" name="authenticationform" />
</form>

<hr>
RESULTS: 
<blockquote>
     <h3>${c.status}</h3>
     <h3>${c.results}</h3>
</blockquote>


</%def>
