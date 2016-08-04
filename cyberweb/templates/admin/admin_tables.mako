<%inherit file="/admin/admin.layout.mako"/>

<%def name="headtags()">
	<script type="text/javascript" src="/jquery.js"></script>
	<script type="text/javascript" src="http://jqueryui.com/latest/jquery-1.3.2.js"></script>
	<script type="text/javascript" src="http://jqueryui.com/latest/ui/jquery.ui.core.js"></script>

    <script type="text/javascript">
	var fields=['id','Username','Firstname','Lastname','Email','Institution','Date Requested'];
    function verify(id,action) {
		$.ajax({
			type: "POST",
			url: "/admin/verify_user",
			data: "id=" + id + "&action=" + action,
			error: function(){
				alert( "Error: Please contact the administrator or try again later.");
			},
			success: function(incoming){
                var action = eval('(' + incoming + ')');

				if (action.error) {
					alert("I received an error. " + action.Message);
					return;
				}

				$("#action" + id).html(action.Message);
			}
		});
    };
    </SCRIPT>
</%def>

<%def name="col2main()">
	<style type="text/css">
			thead {
    float: left;
    text-align: right;
    margin-right: 1em;
    width: 10em;
}

form div {
    margin: 0.5em;
    float: left;
    width: 100%;
}

form input[type="submit"] {
    margin-top: 1em;
    margin-left: 9em;
}
	</style>
      <br>
      <form name="dataForm" method="POST" action="">
  	  % if c.form_data:
  	  <table border=0>
  		${c.form_data}
  	  </table>
	  % else:
        <font color="white">cheating</font>No data in the table
	  % endif
    </form>
</%def>
