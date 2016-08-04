var serviceTypeString = null;

var tabOperationObj = new tabOperation();

var serviceTypeAdminObj = new adminData();
serviceTypeAdminObj.columnList = new Array('Service Type','Description','is Active');
serviceTypeAdminObj.dataKeyNames = new Array('name','description','active');
serviceTypeAdminObj.divName = 'serviceTypeSearchContent';
serviceTypeAdminObj.errorConsole = 'errorConsoleServiceType'; 
serviceTypeAdminObj.activityPane = 'activity_pane_serviceType';
serviceTypeAdminObj.checkBoxName = 'check_serviceType_';
serviceTypeAdminObj.tableName = 'serviceTypeTable'
serviceTypeAdminObj.tableRowName = 'serviceTypeRow_';
serviceTypeAdminObj.typeData = 'serviceType';

var serviceNameAdminObj = new adminData();
serviceNameAdminObj.columnList = new Array('Service Name','Service Type','is Active');
serviceNameAdminObj.dataKeyNames = new Array('name','serviceType','active');
serviceNameAdminObj.divName = 'serviceNameSearchContent';
serviceNameAdminObj.errorConsole = 'errorConsoleServiceName'; 
serviceNameAdminObj.activityPane = 'activity_pane_serviceName';
serviceNameAdminObj.checkBoxName = 'check_serviceName_';
serviceNameAdminObj.tableName = 'serviceNameTable'
serviceNameAdminObj.tableRowName = 'serviceNameRow_';
serviceNameAdminObj.typeData = 'serviceName';

var serviceAdminObj = new adminData();

function init() {
	tabOperationObj.tabList = new Array(document.getElementById('serviceTypeLi'),document.getElementById('serviceNameLi'),document.getElementById('serviceLi'));
	tabOperationObj.tabDivList = new Array(document.getElementById('serviceTypeTab'),document.getElementById('serviceNameTab'),document.getElementById('servicesTab'));
	tabOperationObj.init();
	tabOperationObj.switchTab(tabOperationObj.tabList[0]);
	
	serviceTypeAdminObj.setData(serviceTypeData);
	serviceTypeAdminObj.setParseResponse(parseServiceTypeResponse);
	serviceTypeAdminObj.hideConsole();
	
	serviceNameAdminObj.setData(serviceNameData);
	serviceNameAdminObj.setParseResponse(parseServiceNameResponse);
	serviceNameAdminObj.hideConsole();
	
	serviceAdminObj.setParseResponse(parseServiceResponse);
	
	serviceTypeAdminObj.getData('/newadmin/forwardRequest','method=view&type=serviceType');
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

function serviceNameData(listData) {
	this.id = listData['id'];
	this.name = listData['name'];
	this.serviceType = listData['serviceType'];
	this.active = listData['active'];
}

function serviceTypeData(listData) {
	this.id = listData['id'];
	this.name = listData['name'];
	this.description = listData['description'];
	this.active = listData['active'];
}

function switchTabs(tabObj) {
	tabOperationObj.switchTab(tabObj);
	
	if(tabObj.id == 'serviceTypeLi') {
		serviceTypeAdminObj.getData('/newadmin/forwardRequest','method=view&type=serviceType');
	} else {
		serviceNameAdminObj.getData('/newadmin/forwardRequest','method=view&type=serviceName');
	}
}

function parseServiceTypeResponse(data) {
	serviceTypeAdminObj.parseResponse(data);
}

function parseServiceNameResponse(data){
	serviceNameAdminObj.parseResponse(data);
}

function searchServices() {
	var url = '/newadmin/serviceSearch';
	var param = '';
	var selectCombo = document.getElementById("serviceList");
	var selectedSevice = '';
	for(var i=0;i<selectCombo.length;i++) {
		if(selectCombo.options[i].selected) {
			selectedSevice += selectCombo.options[i].value + ',';
		}
	}
	
	if(selectedSevice == ''){
		$('#errorConsole').html('<h3>Please select Services</h3>');
		$('#errorConsole').show('slow');
		return;
	} else {
		selectedSevice = selectedSevice.substr(0,selectedSevice.length-1);
		url += '?services=' + selectedSevice;
		$('#errorConsole').hide('slow');
	}
	
	serviceAdminObj.getData(url,param);
}

function parseServiceResponse(data) {
	var serviceCount = 0;
	var serviceDivObj = document.getElementById('serviceSearchContent');
	serviceDivObj.innerHTML = '';
	serviceList = new Array();
	myData = eval(data);
	for (key in myData) {
		var objIndividual = myData[key];
		var serciveObj = new serciveData(objIndividual['Service Name'],null,null,null,null,null);
		var count = 0 ;
		var resourceInnerList = new Array();
		var resourceList = objIndividual['Resources'];
		for(key1 in resourceList) {
			var resourceObjJSON = resourceList[key1];
			var resoruceObj = new resourceData(resourceObjJSON['resourceName'],resourceObjJSON['hostName'],resourceObjJSON['institution'],resourceObjJSON['path'],resourceObjJSON['queue'],resourceObjJSON['timeStamp']);
			resourceInnerList[count++] = resoruceObj;
		}
		serciveObj.resourceList = resourceInnerList;
		serviceList[serviceCount++] = serciveObj;
	}
	populateServiceLists(serviceList);
}

function populateServiceLists(listArray) {
	var serviceDivObj = document.getElementById('serviceSearchContent');
	for(var i=0;i<listArray.length;i++){
		var serviceObj = listArray[i];
		var divObj = document.createElement('div');
		var h3Obj = document.createElement('h3');
		h3Obj.innerHTML = 'Resources utilized for <span id="resourceName" class="labelName">' + serviceObj.serviceName + '</span> Services</h3>';
		var h4Obj = document.createElement('h4');
		h4Obj.innerHTML = 'Resources';
		var tableObj = document.createElement('table');
		var rowObj = tableObj.insertRow(-1);
		rowObj.className = "tableHeader";
		var cell1 = rowObj.insertCell(0);
		cell1.innerHTML = 'Resources Name';
		var cell2 = rowObj.insertCell(1);
		cell2.innerHTML = 'Host Name';
		var cell3 = rowObj.insertCell(2);
		cell3.innerHTML = 'Institution';
		var cell4 = rowObj.insertCell(3);
		cell4.innerHTML = 'Path';
		var cell5 = rowObj.insertCell(4);
		cell5.innerHTML = 'Queue';
		var cell6 = rowObj.insertCell(5);
		cell6.innerHTML = 'Time Stamp';
		var cell7 = rowObj.insertCell(6);
		cell7.innerHTML = '';
		
		var resourceInnerList = serviceObj.resourceList;
		var preClassName = 'greyRow';
		for(var j=0;j<resourceInnerList.length;j++) {
			var resourceObj = resourceInnerList[j];
			var rowObj = tableObj.insertRow(-1);
			var cell1 = rowObj.insertCell(0);
			cell1.innerHTML = resourceObj.resourceName;
			var cell2 = rowObj.insertCell(1);
			cell2.innerHTML = resourceObj.hostName;
			var cell3 = rowObj.insertCell(2);
			cell3.innerHTML = resourceObj.institution;
			var cell4 = rowObj.insertCell(3);
			cell4.innerHTML = resourceObj.path;
			var cell5 = rowObj.insertCell(4);
			cell5.innerHTML = resourceObj.queue;
			var cell6 = rowObj.insertCell(5);
			cell6.innerHTML = resourceObj.timeStamp;
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
		serviceDivObj.appendChild(divObj);
	}
}

function refereshService() {
	var serviceDivObj = document.getElementById('serviceSearchContent');
	serviceDivObj.innerHTML = '';
	$('#errorConsole').hide('slow');
	var selectCombo = document.getElementById("serviceList");
	for(var i=0;i<selectCombo.length;i++) {
		selectCombo.options[i].selected = false;
	}
}

$('.addNew').live('click', function(event){
	switch(tabOperationObj.currentTab) {
		case 'serviceTypeLi' :
			addServiceType();
			break;
		case 'serviceNameLi' :
			addServiceName();
			break;
	}
});

$('.delete').live('click', function(event) {
	switch(tabOperationObj.currentTab) {
		case 'serviceTypeLi' :
			serviceTypeAdminObj.deleteOperation(serviceTypeAdminObj);
			break;
		case 'serviceNameLi' :
			serviceNameAdminObj.deleteOperation(serviceNameAdminObj);
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
			case 'serviceTypeLi' :
				serviceTypeAdminObj.makeEditable(this, makeEditableServiceTypeRow, saveServiceTypeRow);
				break;
			case 'serviceNameLi' :
				serviceNameAdminObj.makeEditable(this, makeEditableServiceNameRow, saveServiceNameRow);
				break;
		}
    }
});

function addServiceType() {
	var newData = {
			id: "new_" + serviceTypeAdminObj.newRowId,
			name: '',
			description: '',
			active: 'True'
	}
	
	var dataObj = new serviceTypeData(newData);
	
	serviceTypeAdminObj.addOperation(dataObj, makeEditableServiceTypeRow, saveServiceTypeRow);
}

function addServiceName() {
	var newData = {
			id: "new_" + serviceNameAdminObj.newRowId,
			name: '',
			serviceType: '',
			active: 'False'
	}
	
	var dataObj = new serviceNameData(newData);
	
	serviceNameAdminObj.addOperation(dataObj, makeEditableServiceNameRow, saveServiceNameRow);
}

function makeEditableServiceTypeRow(index, tdObj, dataObj) {
	switch(index) {
		case 1:
			name = "serviceTypeName_"+dataObj.id;
			id = "serviceTypeName_"+dataObj.id;
			value = dataObj.name;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 2:
			name = "serviceTypeDescription_"+dataObj.id;
			id = "serviceTypeDescription_"+dataObj.id;
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

function makeEditableServiceNameRow(index, tdObj, dataObj) {
	switch(index) {
		case 1:
			name = "serviceName_"+dataObj.id;
			id = "serviceName_"+dataObj.id;
			value = dataObj.name;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 2:
			name = "serviceType_"+dataObj.id;
			id = "serviceType_"+dataObj.id;
			value = dataObj.serviceType;
			var serviceTypeSelect = $('<select id="' + id + '"/>');
			for(var i=0;i<serviceTypeString.length;i++) {
				if(serviceTypeString[i]) {
					if(serviceTypeString[i].serviceTypeName == value) {
						$(serviceTypeSelect).append('<option value="' + serviceTypeString[i].id + '" selected>' + serviceTypeString[i].serviceTypeName + '</option>')
					} else {
						$(serviceTypeSelect).append('<option value="' + serviceTypeString[i].id + '">' + serviceTypeString[i].serviceTypeName + '</option>')
					}
				}
			}
			$(tdObj).empty();
			$(tdObj).append(serviceTypeSelect);
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

function saveServiceTypeRow(rowId, rowObj){
	var dataObj = null;
	var method = 'save';
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		rowId = rowId.split("_")[1];
	}
	
	var serviceTypeName = $('#serviceTypeName_'+rowId).val();
	var serviceTypeDescription = $('#serviceTypeDescription_'+rowId).val();
	var active = $('input:radio[name=isActive_'+rowId+']:checked').val();
	
	dataObj = serviceTypeAdminObj.dataList[rowId];
	
	var paramData = {
		type: serviceTypeAdminObj.typeData,
		method: method,
		parameter:JSON.stringify({
			serviceTypeId: rowId,
			name: serviceTypeName,
			description: serviceTypeDescription,
			active:active
		})
	};
	
	$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
		if(method == 'add'){
			rowId = data['dataId'];
			//alert("rowId = " + rowId);
			$(rowObj).attr('id',serviceTypeAdminObj.tableRowName + rowId);
			var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
			$(checkBox).attr("id",serviceTypeAdminObj.checkBoxName + rowId);
			$(checkBox).val(rowId);
			
			var newData = {
					id: rowId,
					name: serviceTypeName,
					description: serviceTypeDescription,
					active:active
			}
			
			dataObj = new serviceTypeData(newData);
			
			serviceTypeAdminObj.dataList[rowId] = dataObj;
			
			if(serviceTypeString != null) {
				serviceTypeString.push({
					id: rowId,
					serviceTypeName: serviceTypeName
				});
			}
		} else if(method == 'save'){
			dataObj.name = serviceTypeName;
			dataObj.description = serviceTypeDescription;
			dataObj.active = active;
		}
		
		serviceTypeAdminObj.convertToNonEditable(rowObj,dataObj);
		
	},error:function(xhr, textStatus){
		throw "Error occured while saving data. Please try again later.";
	},type: "POST", dataType:"json"});
}

function saveServiceNameRow(rowId, rowObj){
	var dataObj = null;
	var method = 'save';
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		rowId = rowId.split("_")[1];
	}
	
	var serviceName = $('#serviceName_'+rowId).val();
	var serviceTypeId = $('#serviceType_'+rowId).val();
	var serviceTypeName = $('#serviceType_' + rowId + ' option:selected').text();
	var active = $('input:radio[name=isActive_'+rowId+']:checked').val();
	
	dataObj = serviceNameAdminObj.dataList[rowId];
	
	var paramData = {
		type: serviceNameAdminObj.typeData,
		method: method,
		parameter:JSON.stringify({
			serviceNameId: rowId,
			name: serviceName,
			serviceTypeId: serviceTypeId,
			active:active
		})
	};
	
	$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
		if(method == 'add'){
			rowId = data['dataId'];
			//alert("rowId = " + rowId);
			$(rowObj).attr('id',serviceNameAdminObj.tableRowName + rowId);
			var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
			$(checkBox).attr("id",serviceNameAdminObj.checkBoxName + rowId);
			$(checkBox).val(rowId);
			
			var newData = {
					id: rowId,
					name: serviceName,
					serviceType: serviceTypeName,
					active:active
			}
			
			dataObj = new serviceNameData(newData);
			
			serviceNameAdminObj.dataList[rowId] = dataObj;
			
		} else if(method == 'save'){
			dataObj.name = serviceName;
			dataObj.serviceType = serviceTypeName;
			dataObj.active = active;
		}
		
		serviceNameAdminObj.convertToNonEditable(rowObj,dataObj);
		
	},error:function(xhr, textStatus){
		throw "Error occured while saving data. Please try again later.";
	},type: "POST", dataType:"json"});
}