<%inherit file="/account/account.layout.mako"/>

<%def name="header()">
</%def>

<%def name="headtags()">
</%def>

<%def name="footer()">
</%def>

<%def name="col2main()">
<blockquote>
<h3> Sign into ${config.get('project.fullname','CyberWeb')}</h3> <p>
<form action="/signin" method="post">
<blockquote>
   <table width=200>
     % if c.message:
     <tr>
         <font color=red>${c.message}</font>
         <p>
     </tr>
     % endif
     <tr>
       <td align=right>
           Username: &nbsp;&nbsp;
       </td>
       <td align=right>
         <input type="text" name="username" value="${c.username}">
       </td>
     </tr>
     <tr>
       <td align=right>
         Password: &nbsp;&nbsp;
       </td>
       <td align=right>
         <input type="password" name="password">
       </td>
     </tr>
     <tr>
       <td align=center colspan=2>
       <input type="submit" value="Signin" name="authform" />
       </td>
     </tr>
   </table>
   <blockquote>
      <b><a href="/signup">Request New Account.</a></b>
      <br><b>Forgot your password?</b>  [request password here]
      <br><b>Having problems?</b>  [contact us here]
   </blockquote>
</blockquote>
</form>

	
</blockquote>

</%def>

<%def name="col2right()">
<h3> </h3>
</%def>
