var tabOperationObj = new tabOperation();
var accountAdminObj = new adminData();
var authKeyAdminObj = new adminData();
var resoruceString = null;
var serviceString = null;
var userString = null;
var newRowId = 1;
var checkBoxCount = 1;
var preClassName = 'greyRow';
var userName = '';

$(document).ready(function () {
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
				var saveObject = $('#' + $(this).attr('saveInfoId'));
				saveObject.attr('isPasswordLessSSH','true');
				saveObject.attr('username',$('#sshUserName').val());
				saveObject.attr('password',$('#sshPassword').val());
				
				saveEdit(null,saveObject);
				return true;
			},
			"Cancel": function() {
				$(this).dialog("close");
				saveEdit(null,$('#' + $(this).attr('saveInfoId')));
				return false;
			}
		}
	});
	
	$('#errorConsoleAccount').hide();
	$('#errorConsoleAuthKey').hide();
});

function userData(userId,userName) {
	this.userId = userId;
	this.userName = userName;
}

function resourceData(resourceId, resourceName) {
	this.resourceId = resourceId;
	this.resourceName = resourceName;
}

function authKeyData(listData) {
	this.id = listData['authKeyId'];
	this.privateKey = listData['private_key'];
	this.publicKey = listData['public_key'];
	this.userName = listData['userName'];
}

function accountsData(listData) {
	this.id = listData['accountId'];
	this.accountName = listData['accountName'];
	this.userName = listData['userName'];
	this.resourceId = listData['resourceId'];
	this.resourceName = listData['resourceName'];
	this.serviceId = listData['serviceId'];
	this.serviceName = listData['serviceName'];
	this.fullName = listData['fullName'];
	this.description = listData['description'];
	this.active = listData['active'];
	this.insertDate = listData['insertDate'];
}

$('.delete').live('click', function(event) {
	switch(tabOperationObj.currentTab) {
		case 'authkeyLi' :
			deleteAuthKey();
			break;
		case 'accountLi' :
			deleteAccount();
			break;
	}
});

$('.addNew').live('click', function(event){
	switch(tabOperationObj.currentTab) {
		case 'authkeyLi' :
			addAuthKey();
			break;
		case 'accountLi' :
			addAccount();
			break;
	}
});

function deleteAuthKey() {
	var deleteData = {
			errorConsole: 'activity_pane_authKey',
			checkBoxName: 'checkAuthKey',
			type: 'authKey',
			tableRowName: 'authKeyRow_'
	};
	
	deleteOperation(deleteData,authKeyAdminObj);
}

function deleteAccount() {
	var deleteData = {
			errorConsole: 'activity_pane_account',
			checkBoxName: 'checkAccount',
			type: 'account',
			tableRowName: 'accountRow_'
	};
	
	deleteOperation(deleteData,accountAdminObj);
}

function deleteOperation(deleteData, adminObj) {
	var checkBoxValue = '';
	$("input:checkbox[name=" + deleteData['checkBoxName'] + "]:checked").each(function()
	{
		if($(this).val().toLowerCase().indexOf("new") == -1) {
			checkBoxValue += $(this).val() + ','; 
		} else {
			rowId = $(this).attr('id').split("_")[1];
			var rowObj = document.getElementById("new_" + rowId);
			var rowIndex = rowObj.rowIndex;
			var table = rowObj.parentNode;
			table.deleteRow(rowIndex-1);
		}
	});
	
	if(checkBoxValue != '') {
		checkBoxValue = checkBoxValue.substr(0,checkBoxValue.length-1);
		deleteRecord(deleteData, adminObj, checkBoxValue)
	}
}

function deleteRecord(deleteData, adminObj, checkBoxValue) {
	$('#' + deleteData['errorConsole']).showLoading();
	
	var paramData = {
			type: deleteData['type'],
			method: 'delete',
			parameter: JSON.stringify({
				deleteId: checkBoxValue
			})
	};
	
	$.ajax({ url: '/newadmin/forwardRequest', data: paramData,
		beforeSend: function(x) {
            if (x && x.overrideMimeType) {
              x.overrideMimeType("application/j-son;charset=UTF-8");
            }
        },
		success: function(data) {
			
			var rowIds = checkBoxValue.split(',');
			for (var i=0;i<rowIds.length;i++) {
				var rowObj = document.getElementById(deleteData['tableRowName'] + rowIds[i]);
				delete adminObj.dataList[rowIds[i]];
				var rowIndex = rowObj.rowIndex;
				var table = rowObj.parentNode;
				table.deleteRow(rowIndex-1);
			}
			$('#' + deleteData['errorConsole']).hideLoading();
		
		},error:function(xhr, textStatus){
			$('#' + deleteData['errorConsole']).hideLoading();
			alert('error occured while deleting data. please try again later.');
		},type: "POST", dataType:"json"});
}

function addAuthKey() {
	var newAuthKeyData = {
			authKeyId: "new_" + newRowId,
			private_key: '',
			publicKey: '',
			userName: userName,
			userId: -1
	};
	var authKeyObj = new authKeyData(newAuthKeyData);
	
	addOperation(authKeyObj,'authKeyTable');
}

function addAccount() {
	var newAccountData = {
			accountId: "new_" + newRowId,
			accountName: '',
			userName: userName,
			userId: -1,
			resourceId: -1,
			resourceName: '',
			serviceId: -1,
			serviceName: '',
			fullName: '',
			description: '',
			active: 'True',
			insertDate: $.format.date(new Date(),"yyyy-MM-dd HH:mm:ss.SSS")
	};
	var accountObj = new accountsData(newAccountData);
	
	addOperation(accountObj,'accountTable');
}

function addOperation(dataObj,tableName) {
	
	var tableObj = document.getElementById(tableName);
	var tbody = tableObj.getElementsByTagName('tbody')[0];
	var rowObj = tbody.insertRow(-1);
	rowObj.id = "new_" + newRowId;
	$(rowObj).attr("isEditable","true");
	
	createRowColumns(rowObj,dataObj);
	convertToEditable(rowObj,dataObj);
	
	newRowId++;
}

function switchTabs(tabObj) {
	tabOperationObj.switchTab(tabObj);
	
	if(tabObj.id == 'authkeyLi') {
		authKeyAdminObj.getData('/newadmin/forwardRequest','method=view&type=authKey');
	} else {
		accountAdminObj.getData('/newadmin/forwardRequest','method=view&type=account');
	}
}

function populateAuthKeyLists(listArray) {
	var cellcount = 0;
	
	var authKeyDivObj = document.getElementById('authKeySearchContent');
	authKeyDivObj.innerHTML = '';
	
	var divObj = document.createElement('div');
	var tableObj = document.createElement('table');
	tableObj.id = "authKeyTable";
	
	var thead = document.createElement('thead');
	var rowObj = thead.insertRow(-1);
	rowObj.className = "tableHeader";
	
	var cell0 = rowObj.insertCell(cellcount);
	cell0.innerHTML = '';
	
	var cell1 = rowObj.insertCell(++cellcount);
	cell1.innerHTML = 'Private Key';
	var cell2 = rowObj.insertCell(++cellcount);
	cell2.innerHTML = 'Public Key';
	var cell3 = rowObj.insertCell(++cellcount);
	cell3.innerHTML = 'User Name';
	
	var tfoot = document.createElement('tfoot');
	var rowObj = tfoot.insertRow(-1);
	rowObj.className = "tableHeader";
	cellcount = 0;
	
	var cell0 = rowObj.insertCell(cellcount);
	cell0.innerHTML = '';
	
	var cell1 = rowObj.insertCell(++cellcount);
	cell1.innerHTML = 'Private Key';
	var cell2 = rowObj.insertCell(++cellcount);
	cell2.innerHTML = 'Public Key';
	var cell3 = rowObj.insertCell(++cellcount);
	cell3.innerHTML = 'User Name';
	
	var tbody = document.createElement('tbody');
	
	preClassName = 'greyRow';
	for(var i=0;i<listArray.length;i++){
		var authKeyObj = listArray[i];
		if(authKeyObj) {
			var rowObj = tbody.insertRow(-1);
			rowObj.id = "authKeyRow_" + authKeyObj.id;
			$(rowObj).attr("isEditable","false");
			createRowColumns(rowObj,authKeyObj);
		}
	}
	
	tableObj.appendChild(thead);
	tableObj.appendChild(tfoot);
	tableObj.appendChild(tbody);
	divObj.appendChild(tableObj);
	authKeyDivObj.appendChild(divObj);
}

function populateAccountLists(listArray) {
	var accountDivObj = document.getElementById('accountSearchContent');
	accountDivObj.innerHTML = '';
	
	var divObj = document.createElement('div');
	var tableObj = document.createElement('table');
	tableObj.id = "accountTable";
	
	var thead = document.createElement('thead');
	var rowObj = thead.insertRow(-1);
	rowObj.className = "tableHeader";
	var cellcount = 0;
	
	var cell0 = rowObj.insertCell(cellcount);
	cell0.innerHTML = '';
	
	var cell1 = rowObj.insertCell(++cellcount);
	cell1.innerHTML = 'Account ID';
	var cell2 = rowObj.insertCell(++cellcount);
	cell2.innerHTML = 'User Id';
	var cell3 = rowObj.insertCell(++cellcount);
	cell3.innerHTML = 'Resource Name';
	var cell7 = rowObj.insertCell(++cellcount);
	cell7.innerHTML = 'Service Name';
	var cell4 = rowObj.insertCell(++cellcount);
	cell4.innerHTML = 'Description';
	var cell5 = rowObj.insertCell(++cellcount);
	cell5.innerHTML = 'is Active';
	var cell6 = rowObj.insertCell(++cellcount);
	cell6.innerHTML = 'Available From';
	
	var tfoot = document.createElement('tfoot');
	var rowObj = tfoot.insertRow(-1);
	rowObj.className = "tableHeader";
	cellcount = 0;
	
	var cell0 = rowObj.insertCell(cellcount);
	cell0.innerHTML = '';
	
	var cell1 = rowObj.insertCell(++cellcount);
	cell1.innerHTML = 'Account Name';
	var cell2 = rowObj.insertCell(++cellcount);
	cell2.innerHTML = 'User Id';
	var cell3 = rowObj.insertCell(++cellcount);
	cell3.innerHTML = 'Resource Name';
	var cell7 = rowObj.insertCell(++cellcount);
	cell7.innerHTML = 'Service Name';
	var cell4 = rowObj.insertCell(++cellcount);
	cell4.innerHTML = 'Description';
	var cell5 = rowObj.insertCell(++cellcount);
	cell5.innerHTML = 'is Active';
	var cell6 = rowObj.insertCell(++cellcount);
	cell6.innerHTML = 'Available From';
	
	var tbody = document.createElement('tbody');
	
	preClassName = 'greyRow';
	for(var i=0;i<listArray.length;i++){
		var accountObj = listArray[i];
		if(accountObj) {
			var rowObj = tbody.insertRow(-1);
			rowObj.id = "accountRow_" + accountObj.id;
			$(rowObj).attr("isEditable","false");
			createRowColumns(rowObj,accountObj);
		}
	}
	
	tableObj.appendChild(thead);
	tableObj.appendChild(tfoot);
	tableObj.appendChild(tbody);
	divObj.appendChild(tableObj);
	accountDivObj.appendChild(divObj);
}

function parseAuthKeyResponse(data) {
	authKeyAdminObj.parseResponse(data);
}

function parseAccountResponse(data){
	accountAdminObj.parseResponse(data);
}

$('.greyRow').live('click',function (event) {
	var input = $('input', event.target);
	if (event.target.tagName.toUpperCase() === "INPUT" || input.length > 0) {
        // link exist in the item which is clicked
		return true;
    } else {
    	makeEditable(this);
    }
});

$('.blueRow').live('click',function (event) {
	var input = $('input', event.target);
	if (event.target.tagName.toUpperCase() === "INPUT" || input.length > 0) {
        // link exist in the item which is clicked
		return true;
    } else {
    	makeEditable(this);
    }
});

function makeEditable(rowObj) {
	var dataId = $(rowObj).attr('id');
	dataId = dataId.split("_")[1];
	var dataObj = null;
	if($(rowObj).attr("isEditable") == "false") {
		$(rowObj).attr("isEditable","true");
		switch(tabOperationObj.currentTab) {
			case 'authkeyLi' :
				dataObj = authKeyAdminObj.dataList[dataId];
				break;
			case 'accountLi' :
				dataObj = accountAdminObj.dataList[dataId];
				break;
		}
		convertToEditable(rowObj,dataObj);
	}
}

function convertToEditable(rowObj,dataObj) {
	var tds = $(rowObj).find('td');
	var values = '';
	var hrefType = '';
	$.each(tds, function(index, item) {
		var name = null;
		var id = null;
		var value = null;
		
		switch(tabOperationObj.currentTab) {
			case 'authkeyLi' :
				hrefType = 'authKeyTab';
				switch(index) {
					case 1:
						name = "privateKey_"+dataObj.id;
						id = "privateKey_"+dataObj.id;
						value = dataObj.privateKey;
						$(item).html('<textarea rows="2" cols="20" name="' + name + '" id="' + id + '">' + value + '</textarea>');
						break;
					case 2:
						name = "publicKey_"+dataObj.id;
						id = "publicKey_"+dataObj.id;
						value = dataObj.publicKey;
						$(item).html('<textarea rows="2" cols="20" name="' + name + '" id="' + id + '">' + value + '</textarea>');
						break;
					case 3:
						name = "userName_"+dataObj.id;
						id = "userName_"+dataObj.id;
						value = dataObj.userName;
						var userSelect = $('<select id="' + id + '"/>');
						for(var i=0;i<userString.length;i++) {
							if(userString[i].userName == value) {
								$(userSelect).append('<option value="' + userString[i].userId + '" selected>' + userString[i].userName + '</option>')
							} else {
								$(userSelect).append('<option value="' + userString[i].userId + '">' + userString[i].userName + '</option>')
							}
						}
						$(item).empty();
						$(item).append(userSelect);
						break;
				}
				break;
			case 'accountLi' :
				hrefType = 'accountTab';
				switch(index) {
					case 1:
						name = "accountName_"+dataObj.id;
						id = "accountName_"+dataObj.id;
						value = dataObj.accountName;
						$(item).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
						break;
					case 2:
						name = "userName_"+dataObj.id;
						id = "userName_"+dataObj.id;
						value = dataObj.userName;
						var userSelect = $('<select id="' + id + '"/>');
						for(var i=0;i<userString.length;i++) {
							if(userString[i].userName == value) {
								$(userSelect).append('<option value="' + userString[i].userId + '" selected>' + userString[i].userName + '</option>')
							} else {
								$(userSelect).append('<option value="' + userString[i].userId + '">' + userString[i].userName + '</option>')
							}
						}
						$(item).empty();
						$(item).append(userSelect);
						break;
					case 3:
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
						$(item).empty();
						$(item).append(resourceSelect);
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
					case 4:
						name = "serviceName_"+dataObj.id;
						id = "serviceName_"+dataObj.id;
						value = dataObj.serviceId;
						var serviceSelect = $('<select id="' + id + '"/>');
						createServiceOptions(serviceSelect,serviceString,value);
						$(item).empty();
						$(item).append(serviceSelect);
						break;
					case 5:
						name = "descrtption_"+dataObj.id;
						id = "descrtption_"+dataObj.id;
						value = dataObj.description;
						$(item).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
						break;
					case 6:
						name = "isActive_"+dataObj.id;
						id = "isActive_"+dataObj.id;
						value = (dataObj.active.toLowerCase() === 'true');
						$(item).html('<input type="radio" name="' + name + '" value="True"/> True <input type="radio" name="' + name + '" value="False"/> False ');
						if(value) {
							$("input:radio[name=" + name + "]:nth(0)").attr('checked', true);
						} else {
							$("input:radio[name=" + name + "]:nth(1)").attr('checked', true);
						}
						break;
				}
				break;
		}
    });
	
	var cellCount = rowObj.cells.length;
	var cellObj = rowObj.cells[0];
	$(cellObj).removeClass('checkCell').addClass('iconsStyle');
	cellObj.innerHTML = '';
	cellObj.style.width = "60px";
	cellObj.width = "60px";
	
	var outterDiv = $('<div />');
	var innerDiv1 = $('<div />');
	var innerDiv2 = $('<div />');
	
	var saveButton = $('<a/>');
	$(saveButton).attr('id','save_'+dataObj.id);
	$(saveButton).attr('href','#'+hrefType);
	$(saveButton).addClass('imageHyperLink');
	$(saveButton).html('<img src="../images/save-as-icon_small.png" width="24" height="24" alt="Save" title="Save" />');
	$(saveButton).attr('rowId',$(rowObj).attr('id'));
	$(saveButton).click(function (event) {
		
		switch(tabOperationObj.currentTab) {
			case 'authkeyLi' :
				saveEdit(event,this);
				break;
			case 'accountLi' :
				var rowId = $(this).attr('rowId');
				var method = 'save';
				if(rowId.split("_")[0] == 'new') {
					method = 'add'
				} else {
					rowId = rowId.split("_")[1];
				}
				var serviceName = $('#serviceName_' + rowId + ' option:selected').text();
				var resourceName = $('#resourceName_' + rowId + ' option:selected').text();
				//$('#resourceId').empty();
				if(serviceName.toLowerCase() == 'ssh' && method == 'add') {
					//$('#resourceId').html(resourceName);
					$("#dialog-modal" ).dialog( "option", "title", "Configure PKI/SSH Passwordless connection to " + resourceName);
					$('#dialog-modal')
						.attr('saveInfoId', this.id)
						.dialog('open');
				} else {
					saveEdit(event,this);
				}
				break;
		}
	});
	
	var cancelButton = $('<a/>');
	$(cancelButton).attr('id','cancel_'+dataObj.id);
	$(cancelButton).attr('href','#'+hrefType);
	$(cancelButton).addClass('imageHyperLink');
	$(cancelButton).html('<img src="../images/Button-Delete-icon.png" width="24" height="24" alt="Cancel" title="Cancel" />');
	$(cancelButton).attr('rowId',$(rowObj).attr('id'));
	$(cancelButton).click(function(event) {
		cancelEdit(event,this);
	});
	
	$(innerDiv1).append(saveButton);
	$(innerDiv1).append(cancelButton);
	
	var copyButton = $('<a/>');
	$(copyButton).attr('id','copy_'+dataObj.id);
	$(copyButton).attr('href','#');
	$(copyButton).addClass('imageHyperLinkLessMargin');
	$(copyButton).html('<img src="../images/copy.png" style="width: 20px; height: 20px;" alt="Copy" title="Copy" />');
	$(copyButton).attr('rowId',$(rowObj).attr('id'));
	var activityPane = this.activityPane;
	$(copyButton).click(function (event) {
		
	});
	
	
	var deleteButton = $('<a/>');
	$(deleteButton).attr('id','delete_'+dataObj.id);
	$(deleteButton).attr('href','#');
	$(deleteButton).addClass('imageHyperLinkLessMargin');
	$(deleteButton).html('<img src="../images/delete_trash.png" style="width: 20px; height: 20px;" alt="Delete" title="Delete" />');
	$(deleteButton).attr('dataId',dataObj.id);
	var adminObj = this;
	$(deleteButton).click(function(event) {
		var dataId = $(this).attr('dataId');
		if(dataId.toLowerCase().indexOf("new") == -1) {
			switch(tabOperationObj.currentTab) {
				case 'authkeyLi' :
					var deleteData = {
						errorConsole: 'activity_pane_authKey',
						checkBoxName: 'checkAuthKey',
						type: 'authKey',
						tableRowName: 'authKeyRow_'
					};
					
					deleteRecord(deleteData,authKeyAdminObj, dataId);
					break;
				case 'accountLi' :
					var deleteData = {
						errorConsole: 'activity_pane_account',
						checkBoxName: 'checkAccount',
						type: 'account',
						tableRowName: 'accountRow_'
					};
					
					deleteRecord(deleteData,accountAdminObj, dataId);
					break;
			}
		} else {
			rowId = dataId.split("_")[1];
			var rowObj = document.getElementById("new_" + rowId);
			var rowIndex = rowObj.rowIndex;
			var table = rowObj.parentNode;
			table.deleteRow(rowIndex-1);
		}
	});
	
	$(innerDiv2).append(copyButton);
	$(innerDiv2).append(deleteButton);
	
	$(outterDiv).append(innerDiv1);
	$(outterDiv).append(innerDiv2);
	
	$(cellObj).append(outterDiv);
	$("#accountName_"+dataObj.id).focus();
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

function saveEdit(event,saveButton) {
	var rowId = $(saveButton).attr('rowId');
	var rowObj = document.getElementById(rowId);
	var dataObj = null;
	var method = 'save';
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		rowId = rowId.split("_")[1];
	}
	
	switch(tabOperationObj.currentTab) {
		case 'authkeyLi' :
			$('#activity_pane_authKey').showLoading();
			var privateKey = $('#privateKey_'+rowId).val();
			var publicKey = $('#publicKey_'+rowId).val();
			var userId = $('#userName_'+rowId).val();
			var userName = $('#userName_' + rowId + ' option:selected').text();
			
			dataObj = authKeyAdminObj.dataList[rowId];
			
			var paramData = {
					type: 'authKey',
					method: method,
					parameter:JSON.stringify({
						authKeyId: rowId,
						private_key:privateKey,
						userId:userId,
						userName:userName,
						public_key:publicKey
					})
			};
			
			$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
				if(method == 'add'){
					rowId = data['dataId'];
					$(rowObj).attr('id',"authKeyRow_"+rowId);
					var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
					$(checkBox).attr("id","check_"+rowId);
					$(checkBox).val(rowId);
					
					var newAuthKeyData = {
							authKeyId: rowId,
							private_key:privateKey,
							userId:userId,
							userName:userName,
							public_key:publicKey
					};
					dataObj = new authKeyData(newAuthKeyData);
					
					accountAdminObj.dataList[rowId] = dataObj;
				} else if(method == 'save'){
					dataObj.privateKey = privateKey;
					dataObj.userName = userName;
					dataObj.publicKey = publicKey;
				}
				
				convertToNonEditable(rowObj,dataObj);
				
				$('#activity_pane_authKey').hideLoading();
				$(rowObj).attr("isEditable","false");
			},error:function(xhr, textStatus){
				$('#activity_pane_authKey').hideLoading();
				alert('error occured while saving data. please try again later.');
			},type: "POST", dataType:"json"});
			
			break;
		case 'accountLi' :
			var accountName = $('#accountName_'+rowId).val();
			var userId = $('#userName_'+rowId).val();
			var userNameDisplay = $('#userName_' + rowId + ' option:selected').text();
			var resourceId = $('#resourceName_'+rowId).val();
			var resourceName = $('#resourceName_' + rowId + ' option:selected').text();
			var serviceId = $('#serviceName_'+rowId).val();
			var serviceName = $('#serviceName_' + rowId + ' option:selected').text();
			var description = $('#descrtption_'+rowId).val();
			var active = $('input:radio[name=isActive_'+rowId+']:checked').val();
			
			if(serviceId == '') {
				$('#errorConsoleAccount').html('No Service is Configured for the resource. Please <a href="/newadmin/resourceServiceLinkDetails" title="Configure Services">Click here</a> to configure the Service.');
				$('#errorConsoleAccount').removeClass('warningStyle').addClass('errorStyle');
				$('#errorConsoleAccount').show();
				$('#errorConsoleAccount').focus();
				window.setTimeout(function() {
					$('#errorConsoleAccount').hide('slow');
				},50000);
				return false;
			}
			$('#activity_pane_account').showLoading();
			dataObj = accountAdminObj.dataList[rowId];
			var paramData = {
					type: 'account',
					method: method,
					parameter:{
						accountId: rowId,
						accountName:accountName,
						userId:userId,
						resourceId:resourceId,
						resourceName:resourceName,
						serviceId:serviceId,
						serviceName:serviceName,
						description:description,
						active:active
					}
			};
			
			if($(saveButton).attr('isPasswordLessSSH')) {
				paramData['parameter']['isCreateKeys'] = true;
				paramData['parameter']['userName'] = $(saveButton).attr('username');
				paramData['parameter']['password'] = $(saveButton).attr('password');
			}
			
			paramData['parameter'] = JSON.stringify(paramData['parameter']);

			$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
				
				if(data['Error']) {
					$('#errorConsoleAccount').html(data['Error']);
					$('#errorConsoleAccount').removeClass('warningStyle').addClass('errorStyle');
					$('#errorConsoleAccount').show();
					window.setTimeout(function() {
						$('#errorConsoleAccount').hide('slow');
					},5000);
					$('#activity_pane_account').hideLoading();
					return;
				} else if(data['warning']) {
					$('#errorConsoleAccount').html(data['warning']);
					$('#errorConsoleAccount').removeClass('errorStyle').addClass('warningStyle');
					$('#errorConsoleAccount').show();
					window.setTimeout(function() {
						$('#errorConsoleAccount').hide('slow');
					},5000);
				} else if(data['message']) {
					$('#errorConsoleAccount').html(data['message']);
					$('#errorConsoleAccount').removeClass('errorStyle').removeClass('warningStyle');
					$('#errorConsoleAccount').show();
					window.setTimeout(function() {
						$('#errorConsoleAccount').hide('slow');
					},5000);
				}
				
				if(method == 'add'){
					//var dataValues = eval('('+data+')');
					rowId = data['dataId'];
					//alert("rowId = " + rowId);
					$(rowObj).attr('id',"accountRow_"+rowId);
					var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
					$(checkBox).attr("id","check_"+rowId);
					$(checkBox).val(rowId);
					
					var newAccountData = {
							accountId: rowId,
							accountName: accountName,
							userName: userNameDisplay,
							resourceId: resourceId,
							resourceName: resourceName,
							serviceId:serviceId,
							serviceName:serviceName,
							fullName: '',
							description: description,
							active: active,
							insertDate: $.format.date(new Date(),"yyyy-MM-dd HH:mm:ss.SSS")
					};
					dataObj = new accountsData(newAccountData);
					
					accountAdminObj.dataList[rowId] = dataObj;
				} else if(method == 'save'){
					//alert("dataObj = " + dataObj);
					dataObj.accountName = accountName;
					dataObj.userName = userNameDisplay;
					dataObj.resourceId = resourceId;
					dataObj.resourceName = resourceName;
					dataObj.serviceId = serviceId;
					dataObj.serviceName = serviceName;
					dataObj.description = description;
					dataObj.active = active;
				}
				
				convertToNonEditable(rowObj,dataObj);
				
				$(rowObj).attr("isEditable","false");
				$('#activity_pane_account').hideLoading();
			},error:function(xhr, status, error){
				$('#activity_pane_account').hideLoading();
				var err = eval("(" + xhr.responseText + ")");
				$('#errorConsoleAccount').html(err.Message);
			},type: "POST", dataType:"json"});
			
			break;
	}
}

function cancelEdit(event,cancelButton) {
	var rowId = $(cancelButton).attr('rowId');
	var rowObj = document.getElementById(rowId);
	var dataObj = null;
	var dataId = rowId.split("_")[1];
	
	if(rowId.split("_")[0] == 'new') {
		var rowObj = document.getElementById("new_" + dataId);
		var rowIndex = rowObj.rowIndex;
		var table = rowObj.parentNode;
		table.deleteRow(rowIndex-1);
		
		if(preClassName == 'blueRow') {
			preClassName = 'greyRow';
		} else {
			preClassName = 'blueRow';
		}
		return;
	}
	
	switch(tabOperationObj.currentTab) {
		case 'authkeyLi' :
			dataObj = authKeyAdminObj.dataList[dataId];
			break;
		case 'accountLi' :
			dataObj = accountAdminObj.dataList[dataId];
			break;
	}
	convertToNonEditable(rowObj,dataObj);
	$(rowObj).attr("isEditable","false");
}

function convertToNonEditable(rowObj, dataObj) {
	var cellCount = rowObj.cells.length;
	var tds = $(rowObj).find('td');
	var checkBoxName = '';
	$.each(tds, function(index, item) {
		switch(tabOperationObj.currentTab) {
			case 'authkeyLi' :
				checkBoxName = 'checkAuthKey';
				switch(index) {
					case 1:
						$(item).empty();
						$(item).html(dataObj.privateKey);
						break;
					case 2:
						$(item).empty();
						$(item).html(dataObj.publicKey);
						break;
					case 3:
						$(item).html(dataObj.userName);
						break;
				}
				break;
			case 'accountLi' :
				checkBoxName = 'checkAccount';
				switch(index) {
					case 1:
						$(item).html(dataObj.accountName);
						break;
					case 2:
						$(item).html(dataObj.userName);
						break;
					case 3:
						$(item).html(dataObj.resourceName);
						break;
					case 4:
						$(item).html(dataObj.serviceName);
						break;
					case 5:
						$(item).html(dataObj.description);
						break;
					case 6:
						$(item).html(dataObj.active);
						break;
				}
				break;
		}
	});
	
	var cellObj = rowObj.cells[0];
	cellObj.innerHTML = '<input type="checkbox" id="check_'+ rowObj.id.split("_")[1] +'" name="' + checkBoxName + '" value="' + dataObj.id + '"/>';
	$(cellObj).removeClass('iconsStyle').addClass('checkCell');
	cellObj.tagName = "checkBox";
	cellObj.style.width = "15px";
	cellObj.width = "15px";
}

function createRowColumns(rowObj,dataObj) {
	cellcount = 0;
	
	switch(tabOperationObj.currentTab) {
		case 'authkeyLi' :
			var cell0 = rowObj.insertCell(cellcount);
			cell0.innerHTML = '<input type="checkbox" id="check_'+ rowObj.id.split("_")[1] +'" name="checkAuthKey" value="' + dataObj.id + '"/>';
			cell0.className = 'checkCell';
			cell0.tagName = "checkBox";
			
			var cell1 = rowObj.insertCell(++cellcount);
			cell1.innerHTML = dataObj.privateKey;
			$(cell1).addClass("maxWidth");
			var cell2 = rowObj.insertCell(++cellcount);
			cell2.innerHTML = dataObj.publicKey;
			$(cell2).addClass("maxWidth");
			var cell3 = rowObj.insertCell(++cellcount);
			cell3.innerHTML = dataObj.userName;
			$(cell3).addClass("maxWidth");
			break;
		case 'accountLi' :
			var cell0 = rowObj.insertCell(cellcount);
			cell0.innerHTML = '<input type="checkbox" id="check_'+ rowObj.id.split("_")[1] +'" name="checkAccount" value="' + dataObj.id + '"/>';
			cell0.className = 'checkCell';
			cell0.tagName = "checkBox";
			
			var cell1 = rowObj.insertCell(++cellcount);
			cell1.innerHTML = dataObj.accountName;
			var cell2 = rowObj.insertCell(++cellcount);
			cell2.innerHTML = dataObj.userName;
			var cell3 = rowObj.insertCell(++cellcount);
			cell3.innerHTML = dataObj.resourceName;
			var cell7 = rowObj.insertCell(++cellcount);
			cell7.innerHTML = dataObj.serviceName;
			var cell4 = rowObj.insertCell(++cellcount);
			cell4.innerHTML = dataObj.description;
			var cell5 = rowObj.insertCell(++cellcount);
			cell5.innerHTML = dataObj.active;
			var cell6 = rowObj.insertCell(++cellcount);
			cell6.innerHTML = dataObj.insertDate;
			break;
	}
	
	if(preClassName == 'blueRow') {
		rowObj.className='greyRow';
		preClassName = 'greyRow';
	} else {
		rowObj.className='blueRow';
		preClassName = 'blueRow';
	}
}