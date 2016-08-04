<%inherit file="/layout.mako"/>

<%
  from authkit.authorize.pylons_adaptors import authorized
  from cyberweb.lib import auth

  session = request.environ['beaker.session']
  g = app_globals
  c = tmpl_context
%>

<%def name="headtags()">
	${next.headtags()}
</%def>

<%def name="header()">
    ${self.header()}
</%def>

<%def name="subnavtabs()">
    ${self.subnavtabs()}
</%def>

<%def name="footer()">
    ${self.footer()}
</%def>

<div class="col2-left">
    ${next.col2left()}
</div>
<div class="col2-main">
    ${next.col2main()}
</div>
