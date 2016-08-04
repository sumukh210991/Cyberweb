## index.html

<%inherit file="/layout.mako"/>

<%def name="header()">

</%def>

<%def name="headtags()">
</%def>

<%def name="footer()">
</%def>

<body>
<center>
<h2>${c.err_code} ${c.err_message}</h2>
<p><p>We're sorry! This page is not available. Please visit the <A HREF="/">CyberWeb homepage</A>.
<br>If you feel like this is a mistake, please contact your system administrator.
<br>If you have an account, please <A HREF="/signin">login</A>.
</center>

</body>
