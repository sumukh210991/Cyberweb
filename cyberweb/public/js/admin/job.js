var jobAdminObj = new adminData();
jobAdminObj.columnList = new Array('job Name','Parent Job Id','State','Submit Time','Start Time','End Time','User','Service');
jobAdminObj.dataKeyNames = new Array('name','parent_job_id','state','submit_time','start_time','end_time','userName','serviceName');
jobAdminObj.divName = 'jobSearchContent';
jobAdminObj.errorConsole = 'errorConsoleProtocol'; 
jobAdminObj.activityPane = 'activity_pane_job';
jobAdminObj.checkBoxName = 'check_job_';
jobAdminObj.tableName = 'jobTable'
jobAdminObj.tableRowName = 'jobRow_';
jobAdminObj.typeData = 'job';
jobAdminObj.isEditable = false;

function init() {
	jobAdminObj.setData(jobData);
	jobAdminObj.setParseResponse(parseProtocolResponse);
	
	jobAdminObj.getData('/newadmin/forwardRequest','method=view&type=job');
}

function jobData(listData) {
	this.id = listData['id'];
	this.name = listData['name'];
	this.parent_job_id = listData['parent_job_id'];
	this.state = listData['state'];
	this.submit_time = listData['submit_time'];
	this.start_time = listData['start_time'];
	this.end_time = listData['end_time'];
	this.userName = listData['userName'];
	this.serviceName = listData['serviceName'];
}

function parseProtocolResponse(data){
	jobAdminObj.parseResponse(data);
}

$('.delete').live('click', function(event) {
	jobAdminObj.deleteOperation(jobAdminObj);
});