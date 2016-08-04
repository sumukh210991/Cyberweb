<%inherit file="/account/account.layout.mako"/>

<%def name="headtags()">
</%def>

<%def name="col2main()">

%if c.status == 1:
  <meta http-equiv="REFRESH" content="10;url=/signin">
  <font color=green>${h.html.literal(c.statusinfo)}</font><br>
  <br>
  <br>
  Please login to use your account. You will be redirected to the signin page in 10 seconds.
  You can also click <a href="/signin">here</a>.
% else:
  <h3>CyberWeb Account Request Form: </h3>
  <br><font color=red>${h.html.literal(c.statusinfo)}</font>
  <p>
  <form action="" method="post">
  <table border=1>
  <tr>
     <td>Username:&nbsp;&nbsp;</td>
     <td><input type="text" name="cw_username" value=${c.username}> </td>
  </tr>
  <tr>
     <td>Passphrase:</td>
     <td><input type="password" name="password" value=${c.password}></td>
  </tr>
  <tr>
     <td>Verify Passphrase:</td>
     <td><input type="password" name="password_verify" value=${c.password_verify}></td>
  </tr>
  <tr>
     <td>Firstname:</td>
     <td><input type="text" name="firstname" value=${c.firstname} ></td>
  </tr>
  <tr>
     <td>Lastname:</td>
     <td><input type="text" name="lastname" value=${c.lastname}></td>
  </tr>
  <tr>
     <td>Email:</td>
     <td><input type="text" name="email" value=${c.email}></td>
  </tr>
  <tr>
     <td>Institution:</td>
     <td><input type="text" name="institution" value=${c.institution}></td>
  </tr>
  <tr>
     <td>Reason:</td>
     <td><input type="text" name="reason" value=${c.reason}></td>
  </tr>
  </table>

  <br>
  <input type="submit" name="reqacct_form">
  </form>
% endif

</%def>
