## data.mako - file browser

<%inherit file="/layout.mako"/>

<%def name="headtags()">
</%def>

<%def name="header()">
</%def>

<%def name="footer()">
</%def>



## Body
<form action="" enctype="multipart/form-data" method="post">
<p>
Please specify a file to upload:<br>
<input type="file" name="datafile" size="40">
</p>
<div>
<input type="submit" value="Send">
</div>
</form>
