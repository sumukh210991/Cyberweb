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

<div class="col2-main">
    ${self.col2main()}
</div>
<div class="col2-right">
    ${self.col2right()}
</div>
