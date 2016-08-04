<%inherit file="/admin/newAdmin.mako"/>

<%def name="headtags()">
	<script type="text/javascript" src="/js/admin/job.js"></script>
</%def>

<%def name="col2left()">
	${self.col2left()}
</%def>

<%def name="col2main()">
	<div id="maincontent">
		<div id="searchcontainer">
			<div id="jobTab" class="classTab">
				<h2 class="header">Jobs</h2>
				<div id="errorConsoleJob" class="errorStyle"></div>
				<div id="activity_pane_job">
					<div id="opertaionDiv" class="operation">
						<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
					<div id="jobSearchContent" class="searchContent">
					</div>
					<div id="opertaionDiv" class="operation">
						<a href="#" class="delete"><img src="/images/delete_icon.png" width="34" height="34"/>Delete</a>
					</div>
				</div>
			</div>
		</div>
	</div>
	<script type="text/javascript">
		init();
	</script>
</%def>