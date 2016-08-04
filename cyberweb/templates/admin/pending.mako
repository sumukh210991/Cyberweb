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
	<div id=""><h3>Pending Account Requests</h3></div>
    <br>
    <form name="dataForm" method="POST" action="">
	% if c.approve_users.count():
    <table id="datatable">
        <tr id="header">
          <th>Username</th>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Email</th>
          <th>Institution</th>
          <th>Date Requested</th>
          <th>Action</th>
        </tr>
        % for i in c.appove_users:
		<tr id="tablerow${i.id}">
		  <td visibility:hidden>${i.id}</td>
		  <td>${i.username}</td>
		  <td>${i.firstname}</td>
		  <td>${i.lastname}</td>
		  <td>${i.email}</td>
		  <td>${i.institution}</td>
		  <td>${i.date_requested}</td>
				<td>
                  <div id="action${row[c.pk_pos[0]]}">
                    <a href="#" onClick="verify('${row[c.pk_pos[0]]}',1)">Accept</a><font color="white">tst</color>
                    <a href="#" onClick="verify('${row[c.pk_pos[0]]}',0)">Reject</a>
                  </div>
				</td>
		</tr>
        % endfor
    </table>
	% else:
        <font color="white">cheating</font>No pending user requests.
	% endif
    </form>
</%def>
