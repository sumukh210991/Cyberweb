var serviceList = new Array();
var protocolList = new Array();
var resourceId = 0;

var resourceServiceLinkAdminObj = new adminData();
resourceServiceLinkAdminObj.columnList = new Array('Service Name','Protocol','Path','Command','Port','is Active','Available From');
resourceServiceLinkAdminObj.dataKeyNames = new Array('service_name','protocol','path','command','port','active','timeStamp');
resourceServiceLinkAdminObj.divName = 'resourceServiceLinkSearchContent';
resourceServiceLinkAdminObj.errorConsole = 'errorConsoleResourceServiceLink'; 
resourceServiceLinkAdminObj.activityPane = 'activity_pane_resourceServiceLink';
resourceServiceLinkAdminObj.checkBoxName = 'check_resourceServiceLink_';
resourceServiceLinkAdminObj.tableName = 'resourceServiceLinkTable';
resourceServiceLinkAdminObj.tableRowName = 'resourceServiceLinkRow_';
resourceServiceLinkAdminObj.typeData = 'resourceServiceLink';

$(document).ready(function() {
	$('#resourceServiceLinkTab').hide();
	$("#resourceList option:first").attr('selected','selected');
	resourceServiceLinkAdminObj.hideConsole();
	resourceServiceLinkAdminObj.setData(resourceServiceLinkData);
	resourceServiceLinkAdminObj.setParseResponse(parseResourceServiceLinkResponse);
	resourceServiceLinkAdminObj.hideConsole();
});

function resourceServiceLinkData(listData) {
	this.id = listData['id'];
	this.service_name = listData['service_name'];
	this.protocol = listData['protocol'];
	this.path = listData['path'];
	this.command = listData['command'];
	this.port = listData['port'];
	this.active = listData['active'];
	this.timeStamp = listData['timestamp'];
}

function parseResourceServiceLinkResponse(data){
	resourceServiceLinkAdminObj.parseResponse(data);
}

$('#resourceList').live('change', function(event) {
	
	if($('#resourceList').val() == '') {
		$('#resourceServiceLinkTab').hide();
	} else {
		resourceId = $('#resourceList').val();
		
		$('#resourceServiceLinkTab').show();
		
		var parameter = JSON.stringify({
			resourceId: $('#resourceList').val()
		});
		
		resourceServiceLinkAdminObj.getData('/newadmin/forwardRequest','method=view&type=resourceServiceLink&parameter='+parameter);
	}
});

$('.addNew').live('click', function(event){
	var newData = {
			id: "new_" + resourceServiceLinkAdminObj.newRowId,
			service_name: '',
			protocol: '',
			path:'',
			command:'',
			port:'',
			active: 'True',
			timestamp:$.format.date(new Date(),"yyyy-MM-dd HH:mm:ss.SSS")
	}
	
	var dataObj = new resourceServiceLinkData(newData);
	
	resourceServiceLinkAdminObj.addOperation(dataObj, makeEditableRow, saveRow);
});

$('.delete').live('click', function(event) {
	resourceServiceLinkAdminObj.deleteOperation(resourceServiceLinkAdminObj);
});

$('.greyRow,.blueRow').live('click',function (event) {
	var input = $('input', event.target);
	if (event.target.tagName.toUpperCase() === "INPUT" || input.length > 0) {
        // link exist in the item which is clicked
		return true;
    } else {
    	resourceServiceLinkAdminObj.makeEditable(this, makeEditableRow, saveRow);
    }
});

function makeEditableRow(index, tdObj, dataObj) {
	switch(index) {
		case 1:
			name = "serviceId_"+dataObj.id;
			id = "serviceId_"+dataObj.id;
			value = dataObj.service_name;
			var serviceSelect = $('<select id="' + id + '"/>');
			for(var i=0;i<serviceList.length;i++) {
				if(serviceList[i].serviceName == value) {
					$(serviceSelect).append('<option value="' + serviceList[i].serviceId + '" selected>' + serviceList[i].serviceName + '</option>')
				} else {
					$(serviceSelect).append('<option value="' + serviceList[i].serviceId + '">' + serviceList[i].serviceName + '</option>')
				}
			}
			$(tdObj).empty();
			$(tdObj).append(serviceSelect);
			break;
		case 2:
			name = "protocolId_"+dataObj.id;
			id = "protocolId_"+dataObj.id;
			value = dataObj.protocol;
			var protocolSelect = $('<select id="' + id + '"/>');
			for(var i=0;i<protocolList.length;i++) {
				if(protocolList[i].protocolName == value) {
					$(protocolSelect).append('<option value="' + protocolList[i].protocolId + '" selected>' + protocolList[i].protocolName + '</option>')
				} else {
					$(protocolSelect).append('<option value="' + protocolList[i].protocolId + '">' + protocolList[i].protocolName + '</option>')
				}
			}
			$(tdObj).empty();
			$(tdObj).append(protocolSelect);
			break;
		case 3:
			name = "path_"+dataObj.id;
			id = "path_"+dataObj.id;
			value = dataObj.path;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 4:
			name = "command_"+dataObj.id;
			id = "command_"+dataObj.id;
			value = dataObj.command;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 5:
			name = "port_"+dataObj.id;
			id = "port_"+dataObj.id;
			value = dataObj.port;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
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

function saveRow(rowId, rowObj){
	var dataObj = null;
	var method = 'save';
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		rowId = rowId.split("_")[1];
	}
	
	var serviceNameId = $('#serviceId_'+rowId).val();
	var serviceName = $('#serviceId_' + rowId + ' option:selected').text();
	var protocolId = $('#protocolId_'+rowId).val();
	var protocolName = $('#protocolId_' + rowId + ' option:selected').text();
	var path = $('#path_'+rowId).val();
	var command = $('#command_'+rowId).val();
	var port = $('#port_'+rowId).val();
	var active = $('input:radio[name=isActive_'+rowId+']:checked').val();
	
	dataObj = resourceServiceLinkAdminObj.dataList[rowId];
	
	var paramData = {
		type: resourceServiceLinkAdminObj.typeData,
		method: method,
		parameter:JSON.stringify({
			serviceId: rowId,
			serviceNameId: serviceNameId,
			protocolId: protocolId,
			path: path,
			command: command,
			port: port,
			resourceId: resourceId,
			active:active
		})
	};
	
	$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
		if(method == 'add'){
			rowId = data['dataId'];
			//alert("rowId = " + rowId);
			$(rowObj).attr('id',resourceServiceLinkAdminObj.tableRowName + rowId);
			var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
			$(checkBox).attr("id",resourceServiceLinkAdminObj.checkBoxName + rowId);
			$(checkBox).val(rowId);
			
			var newData = {
					id: rowId,
					service_name: serviceName,
					protocol: protocolName,
					path:path,
					command:command,
					port:port,
					active:active,
					timestamp:$.format.date(new Date(),"yyyy-MM-dd HH:mm:ss.SSS")
			}
			
			dataObj = new resourceServiceLinkData(newData);
			
			resourceServiceLinkAdminObj.dataList[rowId] = dataObj;
		} else if(method == 'save'){
			dataObj.service_name = serviceName;
			dataObj.protocol = protocolName;
			dataObj.path = path;
			dataObj.command = command;
			dataObj.port = port;
			dataObj.active = active;
		}
		
		resourceServiceLinkAdminObj.convertToNonEditable(rowObj,dataObj);
		
	},error:function(xhr, textStatus){
		throw "Error occured while saving data. Please try again later.";
	},type: "POST", dataType:"json"});
}