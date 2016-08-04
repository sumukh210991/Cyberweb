var queueSystemString = null;
var tabOperationObj = new tabOperation();
var resourceList = new Array();

var resourceNameAdminObj = new adminData();
resourceNameAdminObj.columnList = new Array('Resource Name','Host Name','Institution','Total Memory / GB','No. CPUs','Memory / CPU','No. Nodes','Path','Queue','is Active','Available From');
resourceNameAdminObj.dataKeyNames = new Array('resourceName','hostName','institution','total_memory_gb','num_cpus','memory_per_cpu_gb','num_nodes','path','queue','active','timeStamp');
resourceNameAdminObj.divName = 'resourceNameSearchContent';
resourceNameAdminObj.errorConsole = 'errorConsoleResourceName'; 
resourceNameAdminObj.activityPane = 'activity_pane_resourceName';
resourceNameAdminObj.checkBoxName = 'check_resourceName_';
resourceNameAdminObj.tableName = 'resourceNameTable'
resourceNameAdminObj.tableRowName = 'resourceNameRow_';
resourceNameAdminObj.typeData = 'resourceName';

function resourceNameData(listData) {
	this.id = listData['id'];
	this.resourceName = listData['resourceName'];
	this.hostName = listData['hostName'];
	this.institution = listData['institution'];
	this.total_memory_gb = listData['total_memory_gb'];
	this.num_cpus = listData['num_cpus'];
	this.memory_per_cpu_gb = listData['memory_per_cpu_gb'];
	this.num_nodes = listData['num_nodes'];
	this.path = listData['path'];
	this.queue = listData['queue'];
	this.active = listData['active'];
	this.timeStamp = listData['timeStamp'];
}

function resourceData(reName,hostName,institution,path,queue,timeStamp) {
	this.resourceName = reName;
	this.hostName = hostName;
	this.institution = institution;
	this.path = path;
	this.queue = queue;
	this.timeStamp = timeStamp;
	this.serviceList = new Array();
}

function serciveData(seName,seType,protocolName,path,command,port) {
	this.serviceName = seName;
	this.serviceType = seType;
	this.protocolName = protocolName;
	this.path = path;
	this.command = command;
	this.port = port;
	this.resourceList = new Array();
}

function initializeForm() {
	tabOperationObj.tabList = new Array(document.getElementById('resourceNameLi'),document.getElementById('resourceLi'));
	tabOperationObj.tabDivList = new Array(document.getElementById('resourceNameTab'),document.getElementById('resourceTab'));
	tabOperationObj.init();
	tabOperationObj.switchTab(tabOperationObj.tabList[0]);
	
	resourceNameAdminObj.setData(resourceNameData);
	resourceNameAdminObj.setParseResponse(parseResourceNameResponse);
	resourceNameAdminObj.hideConsole();
	
	resourceNameAdminObj.getData('/newadmin/forwardRequest','method=view&type=resourceName');
}

function switchTabs(tabObj) {
	tabOperationObj.switchTab(tabObj);
	
	if(tabObj.id == 'resourceNameLi') {
		resourceNameAdminObj.getData('/newadmin/forwardRequest','method=view&type=resourceName');
	}
}

function searchResource() {
	var url = '/newadmin/resourceSearch';
	var param = '';
	var selectCombo = document.getElementById("resourceList");
	var selectedResource = '';
	for (var i=0;i<selectCombo.length;i++){
		if(selectCombo.options[i].selected) {
			selectedResource += selectCombo.options[i].value + ',';
		}
	}
	if(selectedResource == ''){
		$('#errorConsole').html('<h3>Please select Resources</h3>');
		$('#errorConsole').show('slow');
	} else {
		selectedResource = selectedResource.substr(0,selectedResource.length-1);
		param = 'resources=' + selectedResource;
		$('#errorConsole').hide('slow');
	}
	lastResourceURL = url;
	var req = new HttpRequest(url,parseResourceResponse);
	req.send(param);
}

function parseResourceResponse(data) {
	var resourceCount = 0;
	var resourceDivObj = document.getElementById('resoruceSearchContent');
	resourceDivObj.innerHTML = '';
	resourceList = new Array();
	myData = eval(data);
	for (key in myData) {
		var objIndividual = myData[key];
		var resourceObj = new resourceData(objIndividual['Resource Name'],null,null,null,null,null);
		var count = 0;
		var serciveInnerList = new Array();
		var serviceList = objIndividual['Services'];
		for(key1 in serviceList) {
			var serviceObjJSON = serviceList[key1];
			var serciveObj = new serciveData(serviceObjJSON['serviceName'],serviceObjJSON['serviceType'],serviceObjJSON['protocol'],serviceObjJSON['path'],serviceObjJSON['command'],serviceObjJSON['port']);
			serciveInnerList[count++] = serciveObj;
		}
		resourceObj.serviceList = serciveInnerList;
		resourceList[resourceCount++] = resourceObj;
	}
	populateResourceLists(resourceList);
}

function populateResourceLists(listArray) {
	var resourceDivObj = document.getElementById('resoruceSearchContent');
	for(var i=0;i<listArray.length;i++){
		var resourceObj = listArray[i];
		var divObj = document.createElement('div');
		var h3Obj = document.createElement('h3');
		h3Obj.innerHTML = 'Services running on <span id="serviceName" class="labelName" >' + resourceObj.resourceName + '</span> Resource</h3>';
		var h4Obj = document.createElement('h4');
		h4Obj.innerHTML = 'Services';
		var tableObj = document.createElement('table');
		
		var rowObj = tableObj.insertRow(-1);
		rowObj.className = "tableHeader";
		var cell1 = rowObj.insertCell(0);
		cell1.innerHTML = 'Service Name';
		var cell2 = rowObj.insertCell(1);
		cell2.innerHTML = 'Service Type';
		var cell3 = rowObj.insertCell(2);
		cell3.innerHTML = 'Protocol Name';
		var cell4 = rowObj.insertCell(3);
		cell4.innerHTML = 'Path';
		var cell5 = rowObj.insertCell(4);
		cell5.innerHTML = 'Command';
		var cell6 = rowObj.insertCell(5);
		cell6.innerHTML = 'Port';
		var cell7 = rowObj.insertCell(6);
		cell7.innerHTML = '';

		var serviceInnerList = resourceObj.serviceList;
		var preClassName = 'greyRow';
		for(var j=0;j<serviceInnerList.length;j++) {
			var serviceObj = serviceInnerList[j];
			var rowObj = tableObj.insertRow(-1);
			var cell1 = rowObj.insertCell(0);
			cell1.innerHTML = serviceObj.serviceName;
			var cell2 = rowObj.insertCell(1);
			cell2.innerHTML = serviceObj.serviceType;
			var cell3 = rowObj.insertCell(2);
			cell3.innerHTML = serviceObj.protocolName;
			var cell4 = rowObj.insertCell(3);
			cell4.innerHTML = serviceObj.path;
			var cell5 = rowObj.insertCell(4);
			cell5.innerHTML = serviceObj.command;
			var cell6 = rowObj.insertCell(5);
			cell6.innerHTML = serviceObj.port;
			var cell7 = rowObj.insertCell(6);
			cell7.innerHTML = '<input type="button" value="Test" class="testButtonStyle" />';
			if(preClassName == 'blueRow') {
				rowObj.className='greyRow';
				preClassName = 'greyRow';
			} else {
				rowObj.className='blueRow';
				preClassName = 'blueRow';
			}
		}
		divObj.appendChild(h3Obj);
		divObj.appendChild(h4Obj);
		divObj.appendChild(tableObj);
		resourceDivObj.appendChild(divObj);
	}
}

function refereshResource() {
	var resourceDivObj = document.getElementById('resoruceSearchContent');
	resourceDivObj.innerHTML = '';
	$('#errorConsole').hide('slow');
	var selectCombo = document.getElementById("resourceList");
	for(var i=0;i<selectCombo.length;i++) {
		selectCombo.options[i].selected = false;
	}
}

function parseResourceNameResponse(data){
	resourceNameAdminObj.parseResponse(data);
}

$('.addNew').live('click', function(event){
	switch(tabOperationObj.currentTab) {
		case 'resourceNameLi' :
			addResourceName();
			break;
	}
});

$('.delete').live('click', function(event) {
	switch(tabOperationObj.currentTab) {
		case 'resourceNameLi' :
			resourceNameAdminObj.deleteOperation(resourceNameAdminObj);
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
			case 'resourceNameLi' :
				resourceNameAdminObj.makeEditable(this, makeEditableResourceNameRow, saveResourceNameRow);
				break;
		}
    }
});

function addResourceName() {
	var newData = {
			id: "new_" + resourceNameAdminObj.newRowId,
			resourceName: '',
			hostName: '',
			institution: '',
			total_memory_gb: 1,
			num_cpus: 1,
			memory_per_cpu_gb: 1,
			num_nodes: 1,
			path: '',
			queue: '',
			active: 'False',
			timeStamp: $.format.date(new Date(),"yyyy-MM-dd HH:mm:ss.SSS")
	}
	
	var dataObj = new resourceNameData(newData);
	
	resourceNameAdminObj.addOperation(dataObj, makeEditableResourceNameRow, saveResourceNameRow);
}

function makeEditableResourceNameRow(index, tdObj, dataObj) {
	switch(index) {
		case 1:
			name = "resourceName_"+dataObj.id;
			id = "resourceName_"+dataObj.id;
			value = dataObj.resourceName;
			$(tdObj).html('<input type="text" style="width:100px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 2:
			name = "hostName_"+dataObj.id;
			id = "hostName_"+dataObj.id;
			value = dataObj.hostName;
			$(tdObj).html('<input type="text" style="width:100px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 3:
			name = "institution_"+dataObj.id;
			id = "institution_"+dataObj.id;
			value = dataObj.institution;
			$(tdObj).html('<input type="text" style="width:100px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 4:
			name = "total_memory_gb_"+dataObj.id;
			id = "total_memory_gb_"+dataObj.id;
			value = dataObj.total_memory_gb;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 5:
			name = "num_cpus_"+dataObj.id;
			id = "num_cpus_"+dataObj.id;
			value = dataObj.num_cpus;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 6:
			name = "memory_per_cpu_gb_"+dataObj.id;
			id = "memory_per_cpu_gb_"+dataObj.id;
			value = dataObj.memory_per_cpu_gb;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 7:
			name = "num_nodes_"+dataObj.id;
			id = "num_nodes_"+dataObj.id;
			value = dataObj.num_nodes;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 8:
			name = "path_"+dataObj.id;
			id = "path_"+dataObj.id;
			value = dataObj.path;
			$(tdObj).html('<input type="text" style="width:50px" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 9:
			name = "queueSystemName_"+dataObj.id;
			id = "queueSystemName_"+dataObj.id;
			value = dataObj.queue;
			var queueSystemSelect = $('<select id="' + id + '"/>');
			$(queueSystemSelect).append('<option value="">Select</option>');
			for(var i=0;i<queueSystemString.length;i++) {
				if(queueSystemString[i].queueSystemName == value) {
					$(queueSystemSelect).append('<option value="' + queueSystemString[i].queueSystemId + '" selected>' + queueSystemString[i].queueSystemName + '</option>');
				} else {
					$(queueSystemSelect).append('<option value="' + queueSystemString[i].queueSystemId + '">' + queueSystemString[i].queueSystemName + '</option>');
				}
			}
			$(tdObj).empty();
			$(tdObj).append(queueSystemSelect);
			break;
		case 10:
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

function saveResourceNameRow(rowId, rowObj){
	var dataObj = null;
	var method = 'save';
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		rowId = rowId.split("_")[1];
	}
	
	var resourceName = $('#resourceName_'+rowId).val();
	var hostName = $('#hostName_'+rowId).val();
	var institution = $('#institution_'+rowId).val();
	var totalMemoryGB = $('#total_memory_gb_'+rowId).val();
	var numCPUs = $('#num_cpus_'+rowId).val();
	var memoryPerCPUGB = $('#memory_per_cpu_gb_'+rowId).val();
	var numNodes = $('#num_nodes_'+rowId).val();
	var path = $('#path_'+rowId).val();
	var queueId = $('#queueSystemName_'+rowId).val();
	var queueName = $('#queueSystemName_' + rowId + ' option:selected').text();
	var active = $('input:radio[name=isActive_'+rowId+']:checked').val();
	
	if(queueId == '') {
		queueName = 'None';
	}
	
	dataObj = resourceNameAdminObj.dataList[rowId];
	
	var paramData = {
		type: resourceNameAdminObj.typeData,
		method: method,
		parameter:JSON.stringify({
			resourceNameId: rowId,
			resourceName: resourceName,
			hostName: hostName,
			institution: institution,
			total_memory_gb: totalMemoryGB,
			num_cpus: numCPUs,
			memory_per_cpu_gb: memoryPerCPUGB,
			num_nodes: numNodes,
			path: path,
			queue: queueName,
			active:active
		})
	};
	
	$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
		if(method == 'add'){
			rowId = data['dataId'];
			//alert("rowId = " + rowId);
			$(rowObj).attr('id',resourceNameAdminObj.tableRowName + rowId);
			var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
			$(checkBox).attr("id",resourceNameAdminObj.checkBoxName + rowId);
			$(checkBox).val(rowId);
			
			var newData = {
					id: "new_" + resourceNameAdminObj.newRowId,
					resourceName: resourceName,
					hostName: hostName,
					institution: institution,
					total_memory_gb: totalMemoryGB,
					num_cpus: numCPUs,
					memory_per_cpu_gb: memoryPerCPUGB,
					num_nodes: numNodes,
					path: path,
					queue: queueName,
					active:active,
					timeStamp: $.format.date(new Date(),"yyyy-MM-dd HH:mm:ss.SSS")
			}
			
			dataObj = new resourceNameData(newData);
			
			resourceNameAdminObj.dataList[rowId] = dataObj;
		} else if(method == 'save'){
			dataObj.resourceName = resourceName;
			dataObj.hostName = hostName;
			dataObj.institution = institution;
			dataObj.total_memory_gb = totalMemoryGB;
			dataObj.num_cpus = numCPUs;
			dataObj.memory_per_cpu_gb = memoryPerCPUGB;
			dataObj.num_nodes = numNodes;
			dataObj.path = path;
			dataObj.queue = queueName;
			dataObj.active = active;
		}
		
		resourceNameAdminObj.convertToNonEditable(rowObj,dataObj);
		
	},error:function(xhr, textStatus){
		throw "Error occured while saving data. Please try again later.";
	},type: "POST", dataType:"json"});
}