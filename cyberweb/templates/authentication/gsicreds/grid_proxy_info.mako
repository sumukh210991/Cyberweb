<%inherit file="/authentication/authentication.layout.mako"/>

<%def name="headtags()">
</%def>


<%def name="col2main()">

<h3>Grid Proxy Info </h3>

<form action="/user/grid_proxy_info_action" method="post">
  <table border=1>
    <tr>
       <td>CyberWeb User Accountname: </td>
       <td> ${c.user} </td>
    </tr>
    <tr>
        <td>Grid Credential Username:&nbsp;&nbsp; </td>
        <td><input type="text" name="myproxy_username" value=""> </td>
    </tr>
  <table>
  <input type="submit" value="Check My Credential" name="/user/grid_proxy_info_action" />
</form>

<hr><h3>Results of grid-proxy-info query:</h3>
<blockquote>
  % for r in c.results :
     ${r} <br>
  % endfor
</blockquote>
     ${c.general}

</%def>
