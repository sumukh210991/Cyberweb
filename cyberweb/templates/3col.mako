
<%inherit file="/layout.mako"/>

<%def name="headtags()">
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

<body>
<div id="content">
	<div class="col3-side">
	    ${self.col3left()}
	</div>
	<div class="col3-main">
	    ${self.col3main()}
	</div>
	<div class="col3-side">
	    ${self.col3right()}
	</div>
<div>
