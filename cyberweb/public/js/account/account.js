var tabOperationObj = new tabOperation();
var resoruceString = null;
var serviceString = null;
var userName = null;
var userId = -1;

var accountAdminObj = new adminData();
accountAdminObj.columnList = new Array('Account ID','Resource','Service','Description','Credential Status');
accountAdminObj.dataKeyNames = new Array('accountName','resourceName','serviceName','description','configureAccount');
accountAdminObj.divName = 'accountSearchContent';
accountAdminObj.errorConsole = 'errorConsoleAccount'; 
accountAdminObj.activityPane = 'activity_pane_account';
accountAdminObj.checkBoxName = 'check_account_';
accountAdminObj.tableName = 'accountTable'
accountAdminObj.tableRowName = 'accountRow_';
accountAdminObj.typeData = 'account';
accountAdminObj.url = '/user/forwardRequest';

function init() {
	tabOperationObj.init();
	accountAdminObj.setData(accountData);
	accountAdminObj.setParseResponse(parseAccountResponse);
	accountAdminObj.hideConsole();
	
	accountAdminObj.getData('/user/forwardRequest','method=view&type=account');
	
	$( "#dialog-modal" ).dialog({
		autoOpen: false,
		height: 360,
		width: 560,
		modal: true,
		resizable: false,
		buttons: {
			"Save": function() {
				if($('#sshUserName').val() == '') {
					alert("Please specify User Name");
					return false;
				} else if($('#sshPassword').val() == '') {
					alert("Please specify password");
					return false;
				}
				$(this).dialog("close");
				var userCredential = document.getElementById('userCredential');
				var rowId = $(userCredential).attr('rowId');
				var accountId = $(userCredential).attr('accountId');
				var openFrom = $(userCredential).attr('openFrom');
				var rowObj = document.getElementById(rowId);
				var dataObj = accountAdminObj.dataList[accountId];
				dataObj.userName = $('#sshUserName').val();
				dataObj.userPassword = $('#sshPassword').val();
				dataObj.isCreateKeys = true;
				
				if('Save' == openFrom) {
					saveRow(rowId, rowObj);
				}
				return true;
			},
			"Cancel": function() {
				$(this).dialog("close");
				
				var userCredential = document.getElementById('userCredential');
				var rowId = $(userCredential).attr('rowId');
				var accountId = $(userCredential).attr('accountId');
				var openFrom = $(userCredential).attr('openFrom');
				var dataObj = accountAdminObj.dataList[accountId];
				
				var rowObj = document.getElementById(rowId);
				
				dataObj.isCreateKeys = false;
				dataObj.userName = null;
				
				if('Save' == openFrom) {
					saveRow(rowId, rowObj);
				}
				return false;
			}
		}
	});
}

function accountData(listData) {
	this.evaluateCredential = function (userName){
		if(userName && userName != null && userName != '') {
			return 'Account has credential';
		} else {
			return 'None';
		}
	}
	
	this.id = listData['accountId'];
	this.accountName = listData['accountName'];
	this.userId = listData['userId'];
	this.resourceId = listData['resourceId'];
	this.resourceName = listData['resourceName'];
	this.serviceId = listData['serviceId'];
	this.serviceName = listData['serviceName'];
	this.description = listData['description'];
	this.active = listData['active'];
	this.insertDate = listData['insertDate'];
	this.configureAccount = this.evaluateCredential(listData['userName']);
	this.userName = listData['userName'];
	this.userPassword = '';
	this.isCreateKeys = false;
}

function parseAccountResponse(data){
	accountAdminObj.parseResponse(data);
}

$('.addNew').live('click', function(event){
	var newData = {
			accountId: "new_" + accountAdminObj.newRowId,
			accountName: '',
			userId:userId,
			userName: '',
			resourceId: 0,
			resourceName: '',
			serviceId: 0,
			serviceName: '',
			description: '',
			active: 'True',
			insertDate: $.format.date(new Date(),"yyyy-MM-dd HH:mm:ss.SSS")
	}
	
	var dataObj = new accountData(newData);
	
	accountAdminObj.addOperation(dataObj, makeEditableRow, saveRow);
});

$('.delete').live('click', function(event) {
	accountAdminObj.deleteOperation(accountAdminObj);
});

$('.greyRow,.blueRow').live('click',function (event) {
	var input = $('input', event.target);
	var href = $('a', event.target);
	if ((event.target.tagName.toUpperCase() === "INPUT" || input.length > 0) || 
			(event.target.tagName.toUpperCase() === "A" || href.length > 0)) {
        // link exist in the item which is clicked
		return true;
    } else {
    	accountAdminObj.makeEditable(this, makeEditableRow, saveRow);
    }
});

function makeEditableRow(index, tdObj, dataObj) {
	switch(index) {
		case 1:
			name = "accountName_"+dataObj.id;
			id = "accountName_"+dataObj.id;
			value = dataObj.accountName;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 2:
			name = "resurceName_"+dataObj.id;
			id = "resourceName_"+dataObj.id;
			value = dataObj.resourceId;
			var resourceSelect = $('<select id="' + id + '"/>');
			for(var i=0;i<resourceString.length;i++) {
				if(resourceString[i].resourceId == value) {
					$(resourceSelect).append('<option value="' + resourceString[i].resourceId + '" selected>' + resourceString[i].resourceName + '</option>')
					
				} else {
					$(resourceSelect).append('<option value="' + resourceString[i].resourceId + '">' + resourceString[i].resourceName + '</option>')
				}
			}
			$(tdObj).empty();
			$(tdObj).append(resourceSelect);
			var selectedIndex = $('option:selected', '#'+id).index();
			serviceString = resourceString[selectedIndex].services;
			$(resourceSelect).change(function (event){
				var resourceId = $(this).val();
				for(var i=0;i<resourceString.length;i++) {
					if(resourceString[i].resourceId == resourceId) {
						serviceString = resourceString[i].services;
						$('#serviceName_'+dataObj.id).empty();
						createServiceOptions($('#serviceName_'+dataObj.id),serviceString,'');
					}
				}
			});
			break;
		case 3:
			name = "serviceName_"+dataObj.id;
			id = "serviceName_"+dataObj.id;
			value = dataObj.serviceId;
			var serviceSelect = $('<select id="' + id + '"/>');
			createServiceOptions(serviceSelect,serviceString,value);
			$(tdObj).empty();
			$(tdObj).append(serviceSelect);
			break;
		case 4:
			name = "descrtption_"+dataObj.id;
			id = "descrtption_"+dataObj.id;
			value = dataObj.description;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 5:
			$(tdObj).html('<a href="#" onclick="popupAccountCredential(\'' + dataObj.id + '\',this);">Configure PKI/SSH connection</a>');
			break;
	}
}

function saveRow(rowId, rowObj){
	var dataObj = null;
	var method = 'save';
	var accountId = rowId;
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		accountId = rowId.split("_")[1];
	}
	
	var accountName = $('#accountName_'+accountId).val();
	var resourceId = $('#resourceName_'+accountId).val();
	var resourceName = $('#resourceName_' + accountId + ' option:selected').text();
	var serviceId = $('#serviceName_'+accountId).val();
	var serviceName = $('#serviceName_' + accountId + ' option:selected').text();
	var description = $('#descrtption_'+accountId).val();
	
	$('#' + accountAdminObj.activityPane).showLoading();
	
	dataObj = accountAdminObj.dataList[accountId];
	
	if(dataObj.userName == '' && serviceName.toLowerCase() == 'ssh')  {
		var userCredential = document.getElementById('userCredential');
		$(userCredential).attr('rowId',rowId);
		$(userCredential).attr('accountId',accountId);
		$(userCredential).attr('openFrom','Save');
		$("#dialog-modal" ).dialog( "option", "title", "Configure PKI/SSH Passwordless connection to " + resourceName);
		$('#dialog-modal').dialog('open');
		$(accountAdminObj.activityPane).hideLoading();
		return true;
	} else if(dataObj.userName == null) {
		dataObj.userName = '';
	}
	
	var paramData = {
		type: accountAdminObj.typeData,
		method: method,
		parameter:JSON.stringify({
			accountId: accountId,
			accountName:accountName,
			userId:userId,
			userName: dataObj.userName,
			password: dataObj.userPassword,
			isCreateKeys: dataObj.isCreateKeys,
			resourceId:resourceId,
			resourceName:resourceName,
			serviceId:serviceId,
			serviceName:serviceName,
			description:description,
			active:'True'
		})
	};
	
	$.ajax({ url: '/user/forwardRequest', data: paramData, success: function(data) {
		if(data['Error']) {
			$('#'+accountAdminObj.errorConsole).html(data['Error']);
			$('#'+accountAdminObj.errorConsole).removeClass('warningStyle').addClass('errorStyle');
			$('#'+accountAdminObj.errorConsole).show();
			window.setTimeout(function() {
				$('#'+accountAdminObj.errorConsole).hide('slow');
			},5000);
			$('#'+accountAdminObj.activityPane).hideLoading();
			return;
		} else if(data['warning']) {
			$('#'+accountAdminObj.errorConsole).html(data['warning']);
			$('#'+accountAdminObj.errorConsole).removeClass('errorStyle').addClass('warningStyle');
			$('#'+accountAdminObj.errorConsole).show();
			window.setTimeout(function() {
				$('#'+accountAdminObj.errorConsole).hide('slow');
			},5000);
		} else if(data['message']) {
			$('#'+accountAdminObj.errorConsole).html(data['message']);
			$('#'+accountAdminObj.errorConsole).removeClass('errorStyle').removeClass('warningStyle');
			$('#'+accountAdminObj.errorConsole).show();
			window.setTimeout(function() {
				$('#'+accountAdminObj.errorConsole).hide('slow');
			},5000);
		}
		
		if(method == 'add'){
			accountId = data['dataId'];
			//alert("accountId = " + accountId);
			$(rowObj).attr('id',accountAdminObj.tableRowName + accountId);
			var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
			$(checkBox).attr("id",accountAdminObj.checkBoxName + accountId);
			$(checkBox).val(accountId);
			
			var newData = {
					accountId: accountId,
					accountName: accountName,
					userId:userId,
					userName: dataObj.userName,
					resourceId: resourceId,
					resourceName: resourceName,
					serviceId:serviceId,
					serviceName:serviceName,
					description: description,
					active: 'True',
					insertDate: $.format.date(new Date(),"yyyy-MM-dd HH:mm:ss.SSS")
			}
			
			dataObj = new accountData(newData);
			
			accountAdminObj.dataList[accountId] = dataObj;
		} else if(method == 'save'){
			dataObj.accountName = accountName;
			dataObj.resourceId = resourceId;
			dataObj.resourceName = resourceName;
			dataObj.serviceId = serviceId;
			dataObj.serviceName = serviceName;
			dataObj.description = description;
			dataObj.active = 'True';
		}
		
		accountAdminObj.convertToNonEditable(rowObj,dataObj);
		$('#' + accountAdminObj.activityPane).hideLoading();
	},error:function(xhr, textStatus){
		$('#' + activityPane).hideLoading();
		throw "Error occured while saving data. Please try again later.";
	},type: "POST", dataType:"json"});
}

function createServiceOptions(serviceSelect, serviceList, value){
	for(var i=0;i<serviceList.length;i++) {
		if(serviceList[i].serviceId == value) {
			$(serviceSelect).append('<option value="' + serviceList[i].serviceId + '" selected>' + serviceList[i].serviceName + '</option>')
		} else {
			$(serviceSelect).append('<option value="' + serviceList[i].serviceId + '">' + serviceList[i].serviceName + '</option>')
		}
	}
	
	if(serviceList.length == 0){
		$(serviceSelect).append('<option value="" selected>Not available</option>');
	}
}

function popupAccountCredential(accountId, href){
	var serviceName = $('#serviceName_' + accountId + ' option:selected').text();
	var resourceName = $('#resourceName_' + accountId + ' option:selected').text();
	if(serviceName.toLowerCase() == 'ssh')  {
		var userCredential = document.getElementById('userCredential');
		var rowObj = $(href).parent("tr");
		$(userCredential).attr('rowId',rowObj.id);
		$(userCredential).attr('accountId',accountId);
		$(userCredential).attr('openFrom','Hyperlink Click');
		$("#dialog-modal" ).dialog( "option", "title", "Configure PKI/SSH Passwordless connection to " + resourceName);
		$('#dialog-modal').dialog('open');
	} else {
		alert('Credential is only configured with SSH service.');
		return true;
	}
}