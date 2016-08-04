<%inherit file="/exec/exec.layout.2col.mako"/>

<%def name="col2main()">
        <h3> Cyberweb Execution Services: Demo JODIS functionality.</h3>
	<br>
	<form action="" method="post">
	<table border=0>
	    <tr><th>Current Jobs</th></tr>
            % for i in c.current_jobs:
	    <tr><td>
		% if c.jobname == i:
                	<input type="radio" name="job" value="${i}" checked>&nbsp;&nbsp;&nbsp;${i}<br>
		% else:
                	<input type="radio" name="job" value="${i}">&nbsp;&nbsp;&nbsp;${i}<br>
		% endif
	    </td></tr>
            % endfor
            <tr><td>
		<input type="radio" name="job" value="add">&nbsp;&nbsp;&nbsp;Add a new job
		<select name="service">
		% for i in c.services:
			% if c.service_id == i.id:
				<option value="${i.id}" selected="selected">${i.service_name.name} @ ${i.resource.name}</option>
			% else:
				<option value="${i.id}">${i.service_name.name} @ ${i.resource.name}</option>
			% endif
		% endfor
		</select>
	    </td></tr>
	</table>
	% if c.job:
		<table>
		<tr><th colspan="2">${c.jobname}</th></tr>
		<tr><th>ID:</th><td>${c.job.id}</td></tr>
		<tr><th>Name:</th><td>${c.job.name}</td></tr>
		<tr><th>Service:</th><td>${c.job.service.service_name.name} (${c.job.service.id})</td></tr>
		<tr><th>Resource:</th><td>${c.job.service.resource.name}</td></tr>
		<tr><th>State:</th><td>${c.job.state}</td></tr>
		% if not len(c.job.listTasks()):
			<tr><th>Tasks:</th><td>No Tasks</tr></tr>
		% else:
			<% tasklen = len(c.job.listTasks()) + 1 %>
			<tr><th rowspan="${tasklen}">Tasks:</th></tr>
			% for i in c.job.listTasks():
				<tr><td>${i}</tr></td>
			% endfor
		% endif
                <tr><td colspan="2">
					<input type="radio" name="task" value="add">&nbsp;&nbsp;&nbsp;Add a new task<br>
                </td></tr>
		% if c.job.listTasks():
                <tr><td colspan="2">
					<input type="radio" name="task" value="run">&nbsp;&nbsp;&nbsp;Run the job<br>
                </td></tr>
                <tr><td colspan="2">
					<input type="radio" name="task" value="monitor">&nbsp;&nbsp;&nbsp;Monitor the job<br>
                </td></tr>
		% endif
                <input type="hidden" name="jobname" value="${c.jobname}"/>
		</table>
	% endif
	<input type="submit" value="Run Remote Command" />
	</form>
	
	% if c.monitor:
		<table>
			<tr>
				<th>Job</th>
				<th>Queue ID</th>
				<th>Status</th>
			</tr>
		% for job, i in c.monitor.items():
			<tr>
				<td>${job}</td><td>${i[0][0]}</td><td>${i[0][1]}</td>
			</tr>
		% endfor
		</table>
	% endif
</%def>
