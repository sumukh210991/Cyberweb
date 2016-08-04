var groupString = null;
var userString = null;
var tabOperationObj = new tabOperation();
var userAdminObj = new adminData();
userAdminObj.columnList = new Array('User Name','Name','Email','Institution','is Active','Available From');
userAdminObj.dataKeyNames = new Array('userName','fullName','email','institution','active','created');
userAdminObj.divName = 'userSearchContent';
userAdminObj.errorConsole = 'errorConsoleUsers'; 
userAdminObj.activityPane = 'activity_pane_users';
userAdminObj.checkBoxName = 'check_users_';
userAdminObj.tableName = 'userTable'
userAdminObj.tableRowName = 'usersRow_';
userAdminObj.typeData = 'user';

var groupAdminObj = new adminData();
groupAdminObj.columnList = new Array('Group Name','Description','is Active');
groupAdminObj.dataKeyNames = new Array('name','description','active');
groupAdminObj.divName = 'groupSearchContent';
groupAdminObj.errorConsole = 'errorConsoleGroups'; 
groupAdminObj.activityPane = 'activity_pane_groups';
groupAdminObj.checkBoxName = 'check_groups_';
groupAdminObj.tableName = 'groupTable'
groupAdminObj.tableRowName = 'groupsRow_';
groupAdminObj.typeData = 'group';

var userGroupAdminObj = new adminData();
userGroupAdminObj.columnList = new Array('User Name','Group Name','is Active');
userGroupAdminObj.dataKeyNames = new Array('userName','groupName','active');
userGroupAdminObj.divName = 'userGroupSearchContent';
userGroupAdminObj.errorConsole = 'errorConsoleUsersGroups'; 
userGroupAdminObj.activityPane = 'activity_pane_users_groups';
userGroupAdminObj.checkBoxName = 'check_users_groups_';
userGroupAdminObj.tableName = 'userGroupTable'
userGroupAdminObj.tableRowName = 'usersGroupsRow_';
userGroupAdminObj.typeData = 'userGroup';

function init() {
	$( "#dialog-modal" ).dialog({
		autoOpen: false,
		height: 280,
		width: 460,
		modal: true,
		resizable: false,
		buttons: {
			"Save": function() {
				if($('#password').val() == '') {
					alert("Please specify Password");
					$('#password').focus();
					return false;
				} else if($('#confirmPassword').val() == '') {
					alert("Please specify Confirm password");
					$('#confirmPassword').focus();
					return false;
				} else if($('#confirmPassword').val() != $('#password').val()) {
					alert("Confirm password and password does not match. Please verify");
					$('#confirmPassword').focus();
					return false;
				}
				
				$(this).dialog("close");

				var passwordField = document.getElementById('passwordField');
				var rowId = $(passwordField).attr('rowId');
				var rowObj = document.getElementById(rowId);
				$(passwordField).attr('isPassword','true');
				$(passwordField).attr('password',$('#password').val());
				saveUserRow(rowId, rowObj);
				return true;
			},
			"Cancel": function() {
				$(this).dialog("close");
				
				var passwordField = document.getElementById('passwordField');
				var rowId = $(passwordField).attr('rowId');
				var rowObj = document.getElementById(rowId);
				
				saveUserRow(rowId, rowObj);
				return false;
			}
		}
	});
	
	tabOperationObj.tabList = new Array(document.getElementById('userLi'),document.getElementById('groupLi'),document.getElementById('userGroupLi'));
	tabOperationObj.tabDivList = new Array(document.getElementById('userTab'),document.getElementById('groupTab'),document.getElementById('userGroupTab'));
	tabOperationObj.init();
	tabOperationObj.switchTab(tabOperationObj.tabList[0]);
	
	groupAdminObj.setData(groupsData);
	groupAdminObj.setParseResponse(parseGroupResponse);
	groupAdminObj.hideConsole();
	
	userAdminObj.setData(userData);
	userAdminObj.setParseResponse(parseUserResponse);
	userAdminObj.hideConsole();
	
	userGroupAdminObj.setData(userGroupsData);
	userGroupAdminObj.setParseResponse(parseUserGroupResponse);
	userGroupAdminObj.hideConsole();
	
	userAdminObj.getData('/newadmin/forwardRequest','method=view&type=user');
}

$(document).ready(function () {
	
	$('#errorConsoleAccount').hide();
	$('#errorConsoleAuthKey').hide();
});

function userData(listData) {
	this.id = listData['id'];
	this.userName = listData['userName'];
	this.fullName = listData['fullName'];
	this.email = listData['email'];
	this.institution = listData['institution'];
	this.active = listData['active'];
	this.created = listData['created'];
}

function groupsData(listData) {
	this.id = listData['id'];
	this.name = listData['name'];
	this.description = listData['description'];
	this.active = listData['active'];
}

function userGroupsData(listData) {
	this.id = listData['id'];
	this.userName = listData['userName'];
	this.groupName = listData['groupName'];
	this.active = listData['active'];
}

function switchTabs(tabObj) {
	tabOperationObj.switchTab(tabObj);
	
	if(tabObj.id == 'userLi') {
		userAdminObj.getData('/newadmin/forwardRequest','method=view&type=user');
	} else if(tabObj.id == 'groupLi'){
		groupAdminObj.getData('/newadmin/forwardRequest','method=view&type=group');
	} else {
		userGroupAdminObj.getData('/newadmin/forwardRequest','method=view&type=userGroup');
	}
}

function parseUserResponse(data) {
	userAdminObj.parseResponse(data);
}

function parseGroupResponse(data){
	groupAdminObj.parseResponse(data);
}

function parseUserGroupResponse(data){
	userGroupAdminObj.parseResponse(data);
}

function makeEditableUserRow(index, tdObj, dataObj) {
	switch(index) {
		case 1:
			name = "userName_"+dataObj.id;
			id = "userName_"+dataObj.id;
			value = dataObj.userName;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 2:
			name = "userFullName_"+dataObj.id;
			id = "userFullName_"+dataObj.id;
			value = dataObj.fullName;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 3:
			name = "userEmail_"+dataObj.id;
			id = "userEmail_"+dataObj.id;
			value = dataObj.email;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 4:
			name = "userInstitution_"+dataObj.id;
			id = "userInstitution_"+dataObj.id;
			value = dataObj.institution;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 5:
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

function makeEditableGroupRow(index, tdObj, dataObj) {
	switch(index) {
		case 1:
			name = "groupName_"+dataObj.id;
			id = "groupName_"+dataObj.id;
			value = dataObj.name;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 2:
			name = "groupDescription_"+dataObj.id;
			id = "groupDescription_"+dataObj.id;
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

function makeEditableUserGroupRow(index, tdObj, dataObj) {
	switch(index) {
		case 1:
			name = "userName_"+dataObj.id;
			id = "userName_"+dataObj.id;
			value = dataObj.userName;
			var userSelect = $('<select id="' + id + '"/>');
			for(var i=0;i<userString.length;i++) {
				if(userString[i]) {
					if(userString[i].userName == value) {
						$(userSelect).append('<option value="' + userString[i].id + '" selected>' + userString[i].userName + '</option>')
					} else {
						$(userSelect).append('<option value="' + userString[i].id + '">' + userString[i].userName + '</option>')
					}
				}
			}
			$(tdObj).empty();
			$(tdObj).append(userSelect);
			break;
		case 2:
			name = "groupName_"+dataObj.id;
			id = "groupName_"+dataObj.id;
			value = dataObj.groupName;
			var groupSelect = $('<select id="' + id + '"/>');
			for(var i=0;i<groupString.length;i++) {
				if(groupString[i]) {
					if(groupString[i].groupName == value) {
						$(groupSelect).append('<option value="' + groupString[i].id + '" selected>' + groupString[i].groupName + '</option>')
					} else {
						$(groupSelect).append('<option value="' + groupString[i].id + '">' + groupString[i].groupName + '</option>')
					}
				}
			}
			$(tdObj).empty();
			$(tdObj).append(groupSelect);
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

function passwordDialog(rowId, rowObj) {
	var passwordField = document.getElementById('passwordField'); 
	$(passwordField).attr('isPassword','');
	$(passwordField).attr('password','');
	$(passwordField).attr('rowId',rowId);
	$('#dialog-modal').dialog('open');
}

function saveUserRow(rowId, rowObj){
	var dataObj = null;
	var method = 'save';
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		rowId = rowId.split("_")[1];
	}
	var passwordField = document.getElementById('passwordField');
	
	var userName = $('#userName_'+rowId).val();
	var userFullName = $('#userFullName_'+rowId).val();
	var userEmail = $('#userEmail_'+rowId).val();
	var userInstitution = $('#userInstitution_' + rowId).val();
	var active = $('input:radio[name=isActive_'+rowId+']:checked').val();
	var parameter = {};
	
	if($(passwordField).attr('isPassword')) {
		parameter = {
				userId: rowId,
				username:userName,
				password:$(passwordField).attr('password'),
				name:userFullName,
				email:userEmail,
				institution:userInstitution,
				active:active
			}
	} else {
		parameter = {
				userId: rowId,
				username:userName,
				name:userFullName,
				email:userEmail,
				institution:userInstitution,
				active:active
			}
	}
	
	dataObj = userAdminObj.dataList[rowId];
	
	var paramData = {
		type: userAdminObj.typeData,
		method: method,
		parameter:JSON.stringify(parameter)
	};
	
	
	
	$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
		if(method == 'add'){
			rowId = data['dataId'];
			//alert("rowId = " + rowId);
			$(rowObj).attr('id',userAdminObj.tableRowName + rowId);
			var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
			$(checkBox).attr("id",userAdminObj.checkBoxName + rowId);
			$(checkBox).val(rowId);
			
			var newUserData = {
					id: rowId,
					userName: userName,
					fullName: userFullName,
					email: userEmail,
					institution: userInstitution,
					active:active,
					created: $.format.date(new Date(),"yyyy-MM-dd HH:mm:ss.SSS")
			}
			
			dataObj = new userData(newUserData);
			
			userAdminObj.dataList[rowId] = dataObj;
			
			if(userString != null) {
				userString.push({
					id: rowId,
					userName: userName
				});
			}
		} else if(method == 'save'){
			dataObj.userName = userName;
			dataObj.fullName = userFullName;
			dataObj.email = userEmail;
			dataObj.institution = userInstitution;
			dataObj.active = active;
		}
		
		userAdminObj.convertToNonEditable(rowObj,dataObj);
		
	},error:function(xhr, textStatus){
		throw "Error occured while saving data. Please try again later.";
	},type: "POST", dataType:"json"});
}

function saveGroupRow(rowId, rowObj){
	var dataObj = null;
	var method = 'save';
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		rowId = rowId.split("_")[1];
	}
	
	var groupName = $('#groupName_'+rowId).val();
	var groupDescription = $('#groupDescription_'+rowId).val();
	var active = $('input:radio[name=isActive_'+rowId+']:checked').val();
	
	dataObj = groupAdminObj.dataList[rowId];
	
	var paramData = {
		type: groupAdminObj.typeData,
		method: method,
		parameter:JSON.stringify({
			groupId: rowId,
			name: groupName,
			description: groupDescription,
			active:active
		})
	};
	
	$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
		if(method == 'add'){
			rowId = data['dataId'];
			//alert("rowId = " + rowId);
			$(rowObj).attr('id',groupAdminObj.tableRowName + rowId);
			var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
			$(checkBox).attr("id",groupAdminObj.checkBoxName + rowId);
			$(checkBox).val(rowId);
			
			var newData = {
					id: rowId,
					name: groupName,
					description: groupDescription,
					active:active
			}
			
			dataObj = new groupsData(newData);
			
			groupAdminObj.dataList[rowId] = dataObj;
			
			if(groupString != null) {
				groupString.push({
					id: rowId,
					groupName: groupName
				});
			}
		} else if(method == 'save'){
			dataObj.name = groupName;
			dataObj.description = groupDescription;
			dataObj.active = active;
		}
		
		groupAdminObj.convertToNonEditable(rowObj,dataObj);
		
	},error:function(xhr, textStatus){
		throw "Error occured while saving data. Please try again later.";
	},type: "POST", dataType:"json"});
}

function saveUserGroupRow(rowId, rowObj){
	var dataObj = null;
	var method = 'save';
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		rowId = rowId.split("_")[1];
	}
	
	var groupId = $('#groupName_'+rowId).val();
	var groupName = $('#groupName_' + rowId + ' option:selected').text();
	var userId = $('#userName_'+rowId).val();
	var userName = $('#userName_' + rowId + ' option:selected').text();
	var active = $('input:radio[name=isActive_'+rowId+']:checked').val();
	
	dataObj = userGroupAdminObj.dataList[rowId];
	
	var paramData = {
		type: userGroupAdminObj.typeData,
		method: method,
		parameter:JSON.stringify({
			userGroupId: rowId,
			user_id: userId,
			group_id: groupId,
			active:active
		})
	};
	
	$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
		if(method == 'add'){
			rowId = data['dataId'];
			//alert("rowId = " + rowId);
			$(rowObj).attr('id',userGroupAdminObj.tableRowName + rowId);
			var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
			$(checkBox).attr("id",userGroupAdminObj.checkBoxName + rowId);
			$(checkBox).val(rowId);
			
			var newData = {
					id: rowId,
					userName: userName,
					groupName: groupName,
					active:active
			}
			
			dataObj = new userGroupsData(newData);
			
			userGroupAdminObj.dataList[rowId] = dataObj;
		} else if(method == 'save'){
			dataObj.userName = userName;
			dataObj.groupName = groupName;
			dataObj.active = active;
		}
		
		userGroupAdminObj.convertToNonEditable(rowObj,dataObj);
	},error:function(xhr, textStatus){
		throw "Error occured while saving data. Please try again later.";
	},type: "POST", dataType:"json"});
}

$('.addNew').live('click', function(event){
	switch(tabOperationObj.currentTab) {
		case 'userLi' :
			addUsers();
			break;
		case 'groupLi' :
			addGroups();
			break;
		case 'userGroupLi' :
			addUsersGroups();
			break;
	}
});

$('.delete').live('click', function(event) {
	switch(tabOperationObj.currentTab) {
		case 'userLi' :
			userAdminObj.deleteOperation(userAdminObj, userString);
			break;
		case 'groupLi' :
			groupAdminObj.deleteOperation(groupAdminObj, groupString);
			break;
		case 'userGroupLi' :
			userGroupAdminObj.deleteOperation(userGroupAdminObj);
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
			case 'userLi' :
				userAdminObj.makeEditable(this, makeEditableUserRow, passwordDialog);
				break;
			case 'groupLi' :
				groupAdminObj.makeEditable(this, makeEditableGroupRow, saveGroupRow);
				break;
			case 'userGroupLi' :
				userGroupAdminObj.makeEditable(this, makeEditableUserGroupRow, saveUserGroupRow);
				break;
		}
    }
});

function addUsers() {
	var newUserData = {
			id: "new_" + userAdminObj.newRowId,
			userName: '',
			fullName: '',
			email: '',
			institution: '',
			active: 'True',
			created: $.format.date(new Date(),"yyyy-MM-dd HH:mm:ss.SSS")
	}
	
	var userDataObj = new userData(newUserData);
	
	userAdminObj.addOperation(userDataObj, makeEditableUserRow, passwordDialog);
}

function addGroups() {
	var newGroupData = {
			id: "new_" + groupAdminObj.newRowId,
			name: '',
			description: '',
			active: 'True'
	}
	
	var groupDataObj = new groupsData(newGroupData);
	
	groupAdminObj.addOperation(groupDataObj, makeEditableGroupRow, saveGroupRow);
}

function addUsersGroups(){
	var newUserGroupData = {
			id: "new_" + userGroupAdminObj.newRowId,
			userName: '',
			groupName: '',
			active: 'True'
	}
	
	var userGroupDataObj = new userGroupsData(newUserGroupData);
	
	userGroupAdminObj.addOperation(userGroupDataObj, makeEditableUserGroupRow, saveUserGroupRow);
}