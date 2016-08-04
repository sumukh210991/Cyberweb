var resourceString = null;
var queueTypeString = null;
var queueInfoString = null;
var queueSystemString = null;
var tabOperationObj = new tabOperation();

var queueTypeAdminObj = new adminData();
queueTypeAdminObj.columnList = new Array('Queue Type','Description','is Active');
queueTypeAdminObj.dataKeyNames = new Array('name','description','active');
queueTypeAdminObj.divName = 'queueTypeSearchContent';
queueTypeAdminObj.errorConsole = 'errorConsoleQueueType'; 
queueTypeAdminObj.activityPane = 'activity_pane_queueType';
queueTypeAdminObj.checkBoxName = 'check_queueType_';
queueTypeAdminObj.tableName = 'queueTypeTable';
queueTypeAdminObj.tableRowName = 'queueTypeRow_';
queueTypeAdminObj.typeData = 'queueType';

var queueSystemAdminObj = new adminData();
queueSystemAdminObj.columnList = new Array('Queue Name','Queue Type','Path','Submit','Delete','Status','Other1','Other2','is Active');
queueSystemAdminObj.dataKeyNames = new Array('name','queueType','path','submit','deleteQueue','status','other1','other2','active');
queueSystemAdminObj.divName = 'queueSystemSearchContent';
queueSystemAdminObj.errorConsole = 'errorConsoleQueueSystem'; 
queueSystemAdminObj.activityPane = 'activity_pane_queueSystem';
queueSystemAdminObj.checkBoxName = 'check_queueSystem_';
queueSystemAdminObj.tableName = 'queueSystemTable';
queueSystemAdminObj.tableRowName = 'queueSystemRow_';
queueSystemAdminObj.typeData = 'queueSystem';

var queueInfoAdminObj = new adminData();
queueInfoAdminObj.columnList = new Array('Name','No','Policy','Max Wall Time','Max Jobs','Max CPUs\/Job','Avg Wait Time','Nodes','CPUS\/Node','Parameters','is Active','Available From');
queueInfoAdminObj.dataKeyNames = new Array('name','no','policy','max_walltime','max_jobs','max_CPUsPerJob','avg_waittime','num_nodes','cpus_per_node','parameters','active','timeStamp');
queueInfoAdminObj.divName = 'queueInfoSearchContent';
queueInfoAdminObj.errorConsole = 'errorConsoleQueueInfo'; 
queueInfoAdminObj.activityPane = 'activity_pane_queueInfo';
queueInfoAdminObj.checkBoxName = 'check_queueInfo_';
queueInfoAdminObj.tableName = 'queueInfoTable';
queueInfoAdminObj.tableRowName = 'queueInfoRow_';
queueInfoAdminObj.typeData = 'queueInfo';

var queueServiceAdminObj = new adminData();
queueServiceAdminObj.columnList = new Array('Queue System Name','Queue Info Name','Resource Name','Directory','Argument','is Active');
queueServiceAdminObj.dataKeyNames = new Array('queueSystemName','queueInfoName','resourceName','bin_dir','arg_string','active');
queueServiceAdminObj.divName = 'queueServiceSearchContent';
queueServiceAdminObj.errorConsole = 'errorConsoleQueueService'; 
queueServiceAdminObj.activityPane = 'activity_pane_queueService';
queueServiceAdminObj.checkBoxName = 'check_queueService_';
queueServiceAdminObj.tableName = 'queueServiceTable';
queueServiceAdminObj.tableRowName = 'queueServiceRow_';
queueServiceAdminObj.typeData = 'queueService';

function init() {
	tabOperationObj.tabList = new Array(document.getElementById('queueTypeLi'),document.getElementById('queueSystemLi'),document.getElementById('queueInfoLi'),document.getElementById('queueServiceLi'));
	tabOperationObj.tabDivList = new Array(document.getElementById('queueTypeTab'),document.getElementById('queueSystemTab'),document.getElementById('queueInfoTab'),document.getElementById('queueServiceTab'));
	tabOperationObj.init();
	tabOperationObj.switchTab(tabOperationObj.tabList[0]);
	
	queueTypeAdminObj.setData(queueTypeData);
	queueTypeAdminObj.setParseResponse(parseQueueTypeResponse);
	queueTypeAdminObj.hideConsole();
	
	queueSystemAdminObj.setData(queueSystemData);
	queueSystemAdminObj.setParseResponse(parseQueueSystemResponse);
	queueSystemAdminObj.hideConsole();
	
	queueInfoAdminObj.setData(queueInfoData);
	queueInfoAdminObj.setParseResponse(parseQueueInfoResponse);
	queueInfoAdminObj.hideConsole();
	
	queueServiceAdminObj.setData(queueServiceData);
	queueServiceAdminObj.setParseResponse(parseQueueServiceResponse);
	queueServiceAdminObj.hideConsole();

	queueTypeAdminObj.getData('/newadmin/forwardRequest','method=view&type=queueType');
}

function queueSystemData(listData) {
	this.id = listData['id'];
	this.name = listData['name'];
	this.queueType = listData['queueType'];
	this.path = listData['path'];
	this.submit = listData['submit'];
	this.deleteQueue = listData['deleteQueue'];
	this.status = listData['status'];
	this.other1 = listData['other1'];
	this.other2 = listData['other2'];
	this.active = listData['active'];
}

function queueTypeData(listData) {
	this.id = listData['id'];
	this.name = listData['name'];
	this.description = listData['description'];
	this.active = listData['active'];
}

function queueInfoData(listData) {
	this.id = listData['id'];
	this.name = listData['name'];
	this.no = listData['no'];
	this.policy = listData['policy'];
	this.max_walltime = listData['max_walltime'];
	this.max_jobs = listData['max_jobs'];
	this.max_CPUsPerJob = listData['max_CPUsPerJob'];
	this.avg_waittime = listData['avg_waittime'];
	this.num_nodes = listData['num_nodes'];
	this.cpus_per_node = listData['cpus_per_node'];
	this.parameters = listData['parameters'];
	this.active = listData['active'];
	this.timeStamp = listData['timeStamp'];
}

function queueServiceData(listData) {
	this.id = listData['id'];
	this.queueSystemName = listData['queueSystemName'];
	this.queueInfoName = listData['queueInfoName'];
	this.resourceName = listData['resourceName'];
	this.bin_dir = listData['bin_dir'];
	this.arg_string = listData['arg_string'];
	this.active = listData['active'];
}

function switchTabs(tabObj) {
	tabOperationObj.switchTab(tabObj);
	
	if(tabObj.id == 'queueTypeLi') {
		queueTypeAdminObj.getData('/newadmin/forwardRequest','method=view&type=queueType');
	} else if(tabObj.id == 'queueSystemLi'){
		queueSystemAdminObj.getData('/newadmin/forwardRequest','method=view&type=queueSystem');
	} else if(tabObj.id == 'queueInfoLi'){
		queueInfoAdminObj.getData('/newadmin/forwardRequest','method=view&type=queueInfo');
	} else {
		queueServiceAdminObj.getData('/newadmin/forwardRequest','method=view&type=queueService');
	}
}

function parseQueueTypeResponse(data) {
	queueTypeAdminObj.parseResponse(data);
}

function parseQueueSystemResponse(data){
	queueSystemAdminObj.parseResponse(data);
}

function parseQueueInfoResponse(data){
	queueInfoAdminObj.parseResponse(data);
}

function parseQueueServiceResponse(data){
	queueServiceAdminObj.parseResponse(data);
}

$('.addNew').live('click', function(event){
	switch(tabOperationObj.currentTab) {
		case 'queueTypeLi' :
			addQueueType();
			break;
		case 'queueSystemLi' :
			addQueueSystem();
			break;
		case 'queueInfoLi' :
			addQueueInfo();
			break;
		case 'queueServiceLi' :
			addQueueService();
			break;
	}
});

$('.delete').live('click', function(event) {
	
	switch(tabOperationObj.currentTab) {
		case 'queueTypeLi' :
			queueTypeAdminObj.deleteOperation(queueTypeAdminObj, queueTypeString);
			break;
		case 'queueSystemLi' :
			queueSystemAdminObj.deleteOperation(queueSystemAdminObj, queueSystemString);
			break;
		case 'queueInfoLi' :
			queueInfoAdminObj.deleteOperation(queueInfoAdminObj, queueInfoString);
			break;
		case 'queueServiceLi' :
			queueServiceAdminObj.deleteOperation(queueServiceAdminObj);
			break;
	}
});

$('.greyRow,.blueRow').live('click',function (event) {
	var input = $('input', event.target);
	if (event.target.tagName.toUpperCase() === "INPUT" || input.length > 0) {
        // link exist in the item which is clicked
		return true;
    } else {
    	
    	switch(tabOperationObj.currentTab) {
			case 'queueTypeLi' :
				queueTypeAdminObj.makeEditable(this, makeEditableQueueTypeRow, saveQueueTypeRow);
				break;
			case 'queueSystemLi' :
				queueSystemAdminObj.makeEditable(this, makeEditableQueueSystemRow, saveQueueSystemRow);
				break;
			case 'queueInfoLi' :
				queueInfoAdminObj.makeEditable(this, makeEditableQueueInfoRow, saveQueueInfoRow);
				break;
			case 'queueServiceLi' :
				queueServiceAdminObj.makeEditable(this, makeEditableQueueServiceRow, saveQueueServiceRow);
				break;
		}
    }
});

function addQueueType() {
	var newQueueTypeData = {
			id: "new_" + queueTypeAdminObj.newRowId,
			name: '',
			description: '',
			active: 'True'
	}
	
	var queueTypeDataObj = new queueTypeData(newQueueTypeData);
	
	queueTypeAdminObj.addOperation(queueTypeDataObj, makeEditableQueueTypeRow, saveQueueTypeRow);
}

function addQueueSystem() {
	var newQueueSystemData = {
			id: "new_" + queueSystemAdminObj.newRowId,
			name: '',
			queueType: 0,
			path: '',
			submit: '',
			deleteQueue: '',
			status: '',
			other1: '',
			other2:'',
			active: 'True'
	}
	
	var queueSystemDataObj = new queueSystemData(newQueueSystemData);
	
	queueSystemAdminObj.addOperation(queueSystemDataObj, makeEditableQueueSystemRow, saveQueueSystemRow);
}

function addQueueInfo() {
	var newQueueInfoData = {
			id: "new_" + queueInfoAdminObj.newRowId,
			name: '',
			no: 0,
			policy: '',
			max_walltime: 1,
			max_jobs: 1,
			max_CPUsPerJob: 1,
			avg_waittime: '',
			num_nodes: 1,
			cpus_per_node: 1,
			parameters: '',
			active: 'True',
			timeStamp: $.format.date(new Date(),"yyyy-MM-dd HH:mm:ss.SSS")
	}
	
	var queueInfoDataObj = new queueInfoData(newQueueInfoData);
	
	queueInfoAdminObj.addOperation(queueInfoDataObj, makeEditableQueueInfoRow, saveQueueInfoRow);
}

function addQueueService(){
	var newQueueServiceData = {
			id: "new_" + queueServiceAdminObj.newRowId,
			queueSystemName: '',
			queueInfoName: '',
			resourceName: '',
			bin_dir: '',
			arg_string: '',
			active: 'True'
	}
	
	var queueServiceDataObj = new queueServiceData(newQueueServiceData);
	
	queueServiceAdminObj.addOperation(queueServiceDataObj, makeEditableQueueServiceRow, saveQueueServiceRow);
}

function makeEditableQueueTypeRow(index, tdObj, dataObj) {
	switch(index) {
		case 1:
			name = "queueTypeName_"+dataObj.id;
			id = "queueTypeName_"+dataObj.id;
			value = dataObj.name;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 2:
			name = "queueTypeDescription_"+dataObj.id;
			id = "queueTypeDescription_"+dataObj.id;
			value = dataObj.description;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 3:
			name = "isActive_"+dataObj.id;
			id = "isActive_"+dataObj.id;
			value = (dataObj.active.toLowerCase() === 'true');
			$(tdObj).html('<input type="radio" name="' + name + '" value="True"/> True <input type="radio" name="' + name + '" value="False"/> False ');
			if(value) {
				$("input:radio[name=" + name + "]:nth(0)").attr('checked', true);
			} else {
				$("input:radio[name=" + name + "]:nth(1)").attr('checked', true);
			}
			break;
	}
}

function makeEditableQueueInfoRow(index, tdObj, dataObj) {
	switch(index) {
		case 1:
			name = "queueInfoName_"+dataObj.id;
			id = "queueInfoName_"+dataObj.id;
			value = dataObj.name;
			$(tdObj).html('<input type="text" style="width:150px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 2:
			name = "queueInfoNo_"+dataObj.id;
			id = "queueInfoNo_"+dataObj.id;
			value = dataObj.no;
			$(tdObj).html('<input type="text" style="width:20px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 3:
			name = "queueInfoPolicy_"+dataObj.id;
			id = "queueInfoPolicy_"+dataObj.id;
			value = dataObj.policy;
			$(tdObj).html('<input type="text" style="width:100px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 4:
			name = "queueInfoMax_walltime_"+dataObj.id;
			id = "queueInfoMax_walltime_"+dataObj.id;
			value = dataObj.max_walltime;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 5:
			name = "queueInfoMax_jobs_"+dataObj.id;
			id = "queueInfoMax_jobs_"+dataObj.id;
			value = dataObj.max_jobs;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 6:
			name = "queueInfoMax_CPUsPerJob_"+dataObj.id;
			id = "queueInfoMax_CPUsPerJob_"+dataObj.id;
			value = dataObj.max_CPUsPerJob;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 7:
			name = "queueInfoAvg_waittime_"+dataObj.id;
			id = "queueInfoAvg_waittime_"+dataObj.id;
			value = dataObj.avg_waittime;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 8:
			name = "queueInfoNum_nodes_"+dataObj.id;
			id = "queueInfoNum_nodes_"+dataObj.id;
			value = dataObj.num_nodes;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 9:
			name = "queueInfoCpus_per_node_"+dataObj.id;
			id = "queueInfoCpus_per_node_"+dataObj.id;
			value = dataObj.cpus_per_node;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 10:
			name = "queueInfoParameters_"+dataObj.id;
			id = "queueInfoParameters_"+dataObj.id;
			value = dataObj.parameters;
			$(tdObj).html('<input type="text" style="width:100px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 11:
			name = "isActive_"+dataObj.id;
			id = "isActive_"+dataObj.id;
			value = (dataObj.active.toLowerCase() === 'true');
			$(tdObj).html('<input type="radio" name="' + name + '" value="True"/> True <input type="radio" name="' + name + '" value="False"/> False ');
			if(value) {
				$("input:radio[name=" + name + "]:nth(0)").attr('checked', true);
			} else {
				$("input:radio[name=" + name + "]:nth(1)").attr('checked', true);
			}
			break;
	}
}

function makeEditableQueueSystemRow(index, tdObj, dataObj) {
	switch(index) {
		case 1:
			name = "queueSystemName_"+dataObj.id;
			id = "queueSystemName_"+dataObj.id;
			value = dataObj.name;
			$(tdObj).html('<input type="text" style="width:150px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 2:
			name = "queueTypeId_"+dataObj.id;
			id = "queueTypeId_"+dataObj.id;
			value = dataObj.queueType;
			var queueTypeSelect = $('<select id="' + id + '"/>');
			for(var i=0;i<queueTypeString.length;i++) {
				if(queueTypeString[i]) {
					if(queueTypeString[i].queueTypeName == value) {
						$(queueTypeSelect).append('<option value="' + queueTypeString[i].id + '" selected>' + queueTypeString[i].queueTypeName + '</option>')
					} else {
						$(queueTypeSelect).append('<option value="' + queueTypeString[i].id + '">' + queueTypeString[i].queueTypeName + '</option>')
					}
				}
			}
			$(tdObj).empty();
			$(tdObj).append(queueTypeSelect);
			break;
		case 3:
			name = "queueSystemPath_"+dataObj.id;
			id = "queueSystemPath_"+dataObj.id;
			value = dataObj.path;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 4:
			name = "queueSystemSubmit_"+dataObj.id;
			id = "queueSystemSubmit_"+dataObj.id;
			value = dataObj.submit;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 5:
			name = "queueSystemDelete_"+dataObj.id;
			id = "queueSystemDelete_"+dataObj.id;
			value = dataObj.deleteQueue;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 6:
			name = "queueSystemStatus_"+dataObj.id;
			id = "queueSystemStatus_"+dataObj.id;
			value = dataObj.status;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 7:
			name = "queueSystemOther1_"+dataObj.id;
			id = "queueSystemOther1_"+dataObj.id;
			value = dataObj.other1;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 8:
			name = "queueSystemOther2_"+dataObj.id;
			id = "queueSystemOther2_"+dataObj.id;
			value = dataObj.other2;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 9:
			name = "isActive_"+dataObj.id;
			id = "isActive_"+dataObj.id;
			value = (dataObj.active.toLowerCase() === 'true');
			$(tdObj).html('<input type="radio" name="' + name + '" value="True"/> True <input type="radio" name="' + name + '" value="False"/> False ');
			if(value) {
				$("input:radio[name=" + name + "]:nth(0)").attr('checked', true);
			} else {
				$("input:radio[name=" + name + "]:nth(1)").attr('checked', true);
			}
			break;
	}
}

function makeEditableQueueServiceRow(index, tdObj, dataObj) {
	switch(index) {
		case 1:
			name = "queueSystemName_"+dataObj.id;
			id = "queueSystemName_"+dataObj.id;
			value = dataObj.queueSystemName;
			var queueSystemSelect = $('<select id="' + id + '"/>');
			$(queueSystemSelect).append('<option value="">None</option>')
			for(var i=0;i<queueSystemString.length;i++) {
				if(queueSystemString[i]) {
					if(queueSystemString[i].queueSystemName == value) {
						$(queueSystemSelect).append('<option value="' + queueSystemString[i].id + '" selected>' + queueSystemString[i].queueSystemName + '</option>')
					} else {
						$(queueSystemSelect).append('<option value="' + queueSystemString[i].id + '">' + queueSystemString[i].queueSystemName + '</option>')
					}
				}
			}
			$(tdObj).empty();
			$(tdObj).append(queueSystemSelect);
			break;
		case 2:
			name = "queueInfoName_"+dataObj.id;
			id = "queueInfoName_"+dataObj.id;
			value = dataObj.queueInfoName;
			var queueInfoSelect = $('<select id="' + id + '"/>');
			for(var i=0;i<queueInfoString.length;i++) {
				if(queueInfoString[i]) {
					if(queueInfoString[i].queueInfoName == value) {
						$(queueInfoSelect).append('<option value="' + queueInfoString[i].id + '" selected>' + queueInfoString[i].queueInfoName + '</option>')
					} else {
						$(queueInfoSelect).append('<option value="' + queueInfoString[i].id + '">' + queueInfoString[i].queueInfoName + '</option>')
					}
				}
			}
			$(tdObj).empty();
			$(tdObj).append(queueInfoSelect);
			break;
		case 3:
			name = "resourceName_"+dataObj.id;
			id = "resourceName_"+dataObj.id;
			value = dataObj.resourceName;
			var resourceSelect = $('<select id="' + id + '"/>');
			for(var i=0;i<resourceString.length;i++) {
				if(resourceString[i].resourceName == value) {
					$(resourceSelect).append('<option value="' + resourceString[i].id + '" selected>' + resourceString[i].resourceName + '</option>')
				} else {
					$(resourceSelect).append('<option value="' + resourceString[i].id + '">' + resourceString[i].resourceName + '</option>')
				}
			}
			$(tdObj).empty();
			$(tdObj).append(resourceSelect);
			break;
		case 4:
			name = "binDir_"+dataObj.id;
			id = "binDir_"+dataObj.id;
			value = dataObj.bin_dir;
			$(tdObj).html('<input type="text" size="10" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 5:
			name = "argString_"+dataObj.id;
			id = "argString_"+dataObj.id;
			value = dataObj.arg_string;
			$(tdObj).html('<input type="text" size="10" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 6:
			name = "isActive_"+dataObj.id;
			id = "isActive_"+dataObj.id;
			value = (dataObj.active.toLowerCase() === 'true');
			$(tdObj).html('<input type="radio" name="' + name + '" value="True"/> True <input type="radio" name="' + name + '" value="False"/> False ');
			if(value) {
				$("input:radio[name=" + name + "]:nth(0)").attr('checked', true);
			} else {
				$("input:radio[name=" + name + "]:nth(1)").attr('checked', true);
			}
			break;
	}
}

function saveQueueTypeRow(rowId, rowObj){
	var dataObj = null;
	var method = 'save';
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		rowId = rowId.split("_")[1];
	}
	
	var queueTypeName = $('#queueTypeName_'+rowId).val();
	var queueTypeDescription = $('#queueTypeDescription_'+rowId).val();
	var active = $('input:radio[name=isActive_'+rowId+']:checked').val();
	
	dataObj = queueTypeAdminObj.dataList[rowId];
	
	var paramData = {
		type: queueTypeAdminObj.typeData,
		method: method,
		parameter:JSON.stringify({
			queueTypeId: rowId,
			name: queueTypeName,
			description: queueTypeDescription,
			active:active
		})
	};
	
	$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
		if(method == 'add'){
			rowId = data['dataId'];
			//alert("rowId = " + rowId);
			$(rowObj).attr('id',queueTypeAdminObj.tableRowName + rowId);
			var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
			$(checkBox).attr("id",queueTypeAdminObj.checkBoxName + rowId);
			$(checkBox).val(rowId);
			
			var newData = {
					id: rowId,
					name: queueTypeName,
					description: queueTypeDescription,
					active:active
			}
			
			dataObj = new queueTypeData(newData);
			
			queueTypeAdminObj.dataList[rowId] = dataObj;
			
			if(queueTypeString != null) {
				queueTypeString.push({
					id: rowId,
					queueTypeName: queueTypeName
				});
			}
		} else if(method == 'save'){
			dataObj.name = queueTypeName;
			dataObj.description = queueTypeDescription;
			dataObj.active = active;
		}
		
		queueTypeAdminObj.convertToNonEditable(rowObj,dataObj);
		
	},error:function(xhr, textStatus){
		throw "Error occured while saving data. Please try again later.";
	},type: "POST", dataType:"json"});
}

function saveQueueInfoRow(rowId, rowObj){
	var dataObj = null;
	var method = 'save';
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		rowId = rowId.split("_")[1];
	}
	
	var queueInfoName = $('#queueInfoName_'+rowId).val();
	var queueInfoNo = $('#queueInfoNo_'+rowId).val();
	var queueInfoPolicy = $('#queueInfoPolicy_'+rowId).val();
	var queueInfoMax_walltime = $('#queueInfoMax_walltime_'+rowId).val();
	var queueInfoMax_jobs = $('#queueInfoMax_jobs_'+rowId).val();
	var queueInfoMax_CPUsPerJob = $('#queueInfoMax_CPUsPerJob_'+rowId).val();
	var queueInfoAvg_waittime = $('#queueInfoAvg_waittime_'+rowId).val();
	var queueInfoNum_nodes = $('#queueInfoNum_nodes_'+rowId).val();
	var queueInfoCpus_per_node = $('#queueInfoCpus_per_node_'+rowId).val();
	var queueInfoParameters = $('#queueInfoParameters_'+rowId).val();
	var active = $('input:radio[name=isActive_'+rowId+']:checked').val();
	
	dataObj = queueInfoAdminObj.dataList[rowId];
	
	var paramData = {
		type: queueInfoAdminObj.typeData,
		method: method,
		parameter:JSON.stringify({
			queueInfoId: rowId,
			name: queueInfoName,
			no: queueInfoNo,
			policy: queueInfoPolicy,
			max_walltime: queueInfoMax_walltime,
			max_jobs: queueInfoMax_jobs,
			max_CPUsPerJob: queueInfoMax_CPUsPerJob,
			avg_waittime: queueInfoAvg_waittime,
			num_nodes: queueInfoNum_nodes,
			cpus_per_node: queueInfoCpus_per_node,
			parameters: queueInfoParameters,
			active:active
		})
	};
	
	$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
		if(method == 'add'){
			rowId = data['dataId'];
			//alert("rowId = " + rowId);
			$(rowObj).attr('id',queueInfoAdminObj.tableRowName + rowId);
			var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
			$(checkBox).attr("id",queueInfoAdminObj.checkBoxName + rowId);
			$(checkBox).val(rowId);
			
			var newData = {
					id: rowId,
					name: queueInfoName,
					no: queueInfoNo,
					policy: queueInfoPolicy,
					max_walltime: queueInfoMax_walltime,
					max_jobs: queueInfoMax_jobs,
					max_CPUsPerJob: queueInfoMax_CPUsPerJob,
					avg_waittime: queueInfoAvg_waittime,
					num_nodes: queueInfoNum_nodes,
					cpus_per_node: queueInfoCpus_per_node,
					parameters: queueInfoParameters,
					active:active,
					timeStamp: $.format.date(new Date(),"yyyy-MM-dd HH:mm:ss.SSS")
			}
			
			dataObj = new queueInfoData(newData);
			
			queueInfoAdminObj.dataList[rowId] = dataObj;
			
			if(queueInfoString != null) {
				queueInfoString.push({
					id: rowId,
					queueInfoName: queueInfoName
				});
			}
		} else if(method == 'save'){
			dataObj.name = queueInfoName;
			dataObj.no = queueInfoNo,
			dataObj.policy = queueInfoPolicy,
			dataObj.max_walltime = queueInfoMax_walltime,
			dataObj.max_jobs = queueInfoMax_jobs,
			dataObj.max_CPUsPerJob = queueInfoMax_CPUsPerJob,
			dataObj.avg_waittime = queueInfoAvg_waittime,
			dataObj.num_nodes = queueInfoNum_nodes,
			dataObj.cpus_per_node = queueInfoCpus_per_node,
			dataObj.parameters = queueInfoParameters
			dataObj.active = active;
		}
		
		queueInfoAdminObj.convertToNonEditable(rowObj,dataObj);
		
	},error:function(xhr, textStatus){
		throw "Error occured while saving data. Please try again later.";
	},type: "POST", dataType:"json"});
}

function saveQueueSystemRow(rowId, rowObj){
	var dataObj = null;
	var method = 'save';
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		rowId = rowId.split("_")[1];
	}
	
	var queueSystemName = $('#queueSystemName_'+rowId).val();
	var queueTypeId = $('#queueTypeId_'+rowId).val();
	var queueTypeName = $('#queueTypeId_' + rowId + ' option:selected').text();
	var queueSystemPath = $('#queueSystemPath_'+rowId).val();
	var queueSystemSubmit = $('#queueSystemSubmit_'+rowId).val();
	var queueSystemDelete = $('#queueSystemDelete_'+rowId).val();
	var queueSystemStatus = $('#queueSystemStatus_'+rowId).val();
	var queueSystemOther1 = $('#queueSystemOther1_'+rowId).val();
	var queueSystemOther2 = $('#queueSystemOther2_'+rowId).val();
	var active = $('input:radio[name=isActive_'+rowId+']:checked').val();
	
	dataObj = queueSystemAdminObj.dataList[rowId];
	
	var paramData = {
		type: queueSystemAdminObj.typeData,
		method: method,
		parameter:JSON.stringify({
			queueSystemId: rowId,
			name: queueSystemName,
			queueType: queueTypeId,
			path: queueSystemPath,
			submit: queueSystemSubmit,
			deleteQueue: queueSystemDelete,
			status: queueSystemStatus,
			other1: queueSystemOther1,
			other2: queueSystemOther2,
			active:active
		})
	};
	
	$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
		if(method == 'add'){
			rowId = data['dataId'];
			//alert("rowId = " + rowId);
			$(rowObj).attr('id',queueSystemAdminObj.tableRowName + rowId);
			var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
			$(checkBox).attr("id",queueSystemAdminObj.checkBoxName + rowId);
			$(checkBox).val(rowId);
			
			var newData = {
					id: rowId,
					name: queueSystemName,
					queueType: queueTypeName,
					path: queueSystemPath,
					submit: queueSystemSubmit,
					deleteQueue: queueSystemDelete,
					status: queueSystemStatus,
					other1: queueSystemOther1,
					other2: queueSystemOther2,
					active:active
			}
			
			dataObj = new queueSystemData(newData);
			
			queueSystemAdminObj.dataList[rowId] = dataObj;
			
			if(queueSystemString != null) {
				queueSystemString.push({
					id: rowId,
					queueSystemName: queueSystemName
				});
			}
		} else if(method == 'save'){
			dataObj.name = queueSystemName,
			dataObj.queueType = queueTypeName,
			dataObj.path = queueSystemPath,
			dataObj.submit = queueSystemSubmit,
			dataObj.deleteQueue = queueSystemDelete,
			dataObj.status = queueSystemStatus,
			dataObj.other1 = queueSystemOther1,
			dataObj.other2 = queueSystemOther2;
			dataObj.active = active;
		}
		
		queueSystemAdminObj.convertToNonEditable(rowObj,dataObj);
		
	},error:function(xhr, textStatus){
		throw "Error occured while saving data. Please try again later.";
	},type: "POST", dataType:"json"});
}

function saveQueueServiceRow(rowId, rowObj){
	var dataObj = null;
	var method = 'save';
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		rowId = rowId.split("_")[1];
	}
	
	var queueSystemId = $('#queueSystemName_'+rowId).val();
	var queueSystemName = $('#queueSystemName_' + rowId + ' option:selected').text();
	var queueInfoId = $('#queueInfoName_'+rowId).val();
	var queueInfoName = $('#queueInfoName_' + rowId + ' option:selected').text();
	var resourceId = $('#resourceName_'+rowId).val();
	var resourceName = $('#resourceName_' + rowId + ' option:selected').text();
	var binDir = $('#binDir_'+rowId).val();
	var argString = $('#argString_'+rowId).val();
	var active = $('input:radio[name=isActive_'+rowId+']:checked').val();
	
	dataObj = queueServiceAdminObj.dataList[rowId];
	
	var paramData = {
		type: queueServiceAdminObj.typeData,
		method: method,
		parameter:JSON.stringify({
			queueServiceId: rowId,
			queueSystemId: queueSystemId,
			queueInfoId: queueInfoId,
			resourceId: resourceId,
			bin_dir: binDir,
			arg_string: argString,
			active:active
		})
	};
	
	$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
		if(method == 'add'){
			rowId = data['dataId'];
			//alert("rowId = " + rowId);
			$(rowObj).attr('id',queueServiceAdminObj.tableRowName + rowId);
			var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
			$(checkBox).attr("id",queueServiceAdminObj.checkBoxName + rowId);
			$(checkBox).val(rowId);
			
			var newData = {
					id: rowId,
					queueSystemName: queueSystemName,
					queueInfoName: queueInfoName,
					resourceName: resourceName,
					bin_dir: binDir,
					arg_string: argString,
					active:active
			}
			
			dataObj = new queueServiceData(newData);
			
			queueServiceAdminObj.dataList[rowId] = dataObj;
		} else if(method == 'save'){
			dataObj.queueSystemName = queueSystemName,
			dataObj.queueInfoName = queueInfoName,
			dataObj.resourceName = resourceName,
			dataObj.bin_dir = binDir,
			dataObj.arg_string = argString;
			dataObj.active = active;
		}
		
		queueServiceAdminObj.convertToNonEditable(rowObj,dataObj);
		
	},error:function(xhr, textStatus){
		throw "Error occured while saving data. Please try again later.";
	},type: "POST", dataType:"json"});
}