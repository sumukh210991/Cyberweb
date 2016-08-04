var messageTypeString = null;
var groupString = null;
var userString = null;

var tabOperationObj = new tabOperation();

var messageTypeAdminObj = new adminData();
messageTypeAdminObj.columnList = new Array('Message Name','Description','is Active');
messageTypeAdminObj.dataKeyNames = new Array('name','description','active');
messageTypeAdminObj.divName = 'messageTypeSearchContent';
messageTypeAdminObj.errorConsole = 'errorConsoleMessageType'; 
messageTypeAdminObj.activityPane = 'activity_pane_messageType';
messageTypeAdminObj.checkBoxName = 'check_messageType_';
messageTypeAdminObj.tableName = 'messageTypeTable'
messageTypeAdminObj.tableRowName = 'messageTypeRow_';
messageTypeAdminObj.typeData = 'messageType';

var messageAdminObj = new adminData();
messageAdminObj.columnList = new Array('Message Name','Message Type','Author','Recipient','is Active','Available From');
messageAdminObj.dataKeyNames = new Array('message','messageType','author','recipient','active','creationDate');
messageAdminObj.divName = 'messageSearchContent';
messageAdminObj.errorConsole = 'errorConsoleMessage'; 
messageAdminObj.activityPane = 'activity_pane_message';
messageAdminObj.checkBoxName = 'check_message_';
messageAdminObj.tableName = 'messageTable'
messageAdminObj.tableRowName = 'messageRow_';
messageAdminObj.typeData = 'message';

function init() {
	tabOperationObj.tabList = new Array(document.getElementById('messageTypeLi'),document.getElementById('messageLi'));
	tabOperationObj.tabDivList = new Array(document.getElementById('messageTypeTab'),document.getElementById('messageTab'));
	tabOperationObj.init();
	tabOperationObj.switchTab(tabOperationObj.tabList[0]);
	
	messageTypeAdminObj.setData(messageTypeData);
	messageTypeAdminObj.setParseResponse(parseMessageTypeResponse);
	messageTypeAdminObj.hideConsole();
	
	messageAdminObj.setData(messageData);
	messageAdminObj.setParseResponse(parseMessageResponse);
	messageAdminObj.hideConsole();
	
	messageTypeAdminObj.getData('/newadmin/forwardRequest','method=view&type=messageType');
}

function messageData(listData) {
	this.id = listData['id'];
	this.message = listData['message'];
	this.messageType = listData['messageType'];
	this.author = listData['author'];
	this.recipient = listData['recipient'];
	this.recipient_type = listData['recipient_type'];
	this.active = listData['active'];
	this.creationDate = listData['creationDate'];
}

function messageTypeData(listData) {
	this.id = listData['id'];
	this.name = listData['name'];
	this.description = listData['description'];
	this.active = listData['active'];
}

function switchTabs(tabObj) {
	tabOperationObj.switchTab(tabObj);
	
	if(tabObj.id == 'messageTypeLi') {
		messageTypeAdminObj.getData('/newadmin/forwardRequest','method=view&type=messageType');
	} else {
		messageAdminObj.getData('/newadmin/forwardRequest','method=view&type=message');
	}
}

function parseMessageTypeResponse(data) {
	messageTypeAdminObj.parseResponse(data);
}

function parseMessageResponse(data){
	messageAdminObj.parseResponse(data);
}

$('.addNew').live('click', function(event){
	switch(tabOperationObj.currentTab) {
		case 'messageTypeLi' :
			addMessageType();
			break;
		case 'messageLi' :
			addMessage();
			break;
	}
});

$('.delete').live('click', function(event) {
	switch(tabOperationObj.currentTab) {
		case 'messageTypeLi' :
			messageTypeAdminObj.deleteOperation(messageTypeAdminObj, messageTypeString);
			break;
		case 'messageLi' :
			messageAdminObj.deleteOperation(messageAdminObj);
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
			case 'messageTypeLi' :
				messageTypeAdminObj.makeEditable(this, makeEditableMessageTypeRow, saveMessageTypeRow);
				break;
			case 'messageLi' :
				messageAdminObj.makeEditable(this, makeEditableMessageRow, saveMessageRow);
				break;
		}
    }
});

function addMessageType() {
	var newData = {
			id: "new_" + messageTypeAdminObj.newRowId,
			name: '',
			description: '',
			active: 'True'
	}
	
	var dataObj = new messageTypeData(newData);
	
	messageTypeAdminObj.addOperation(dataObj, makeEditableMessageTypeRow, saveMessageTypeRow);
}

function addMessage() {
	var newData = {
			id: "new_" + messageAdminObj.newRowId,
			message: '',
			messageType: '',
			author: '',
			recipient: '',
			recipient_type: 'None',
			active: 'True',
			creationDate: $.format.date(new Date(),"yyyy-MM-dd HH:mm:ss.SSS")
	}
	
	var dataObj = new messageData(newData);
	
	messageAdminObj.addOperation(dataObj, makeEditableMessageRow, saveMessageRow);
}

function makeEditableMessageTypeRow(index, tdObj, dataObj) {
	switch(index) {
		case 1:
			name = "messageTypeName_"+dataObj.id;
			id = "messageTypeName_"+dataObj.id;
			value = dataObj.name;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 2:
			name = "messageTypeDescription_"+dataObj.id;
			id = "messageTypeDescription_"+dataObj.id;
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

function makeEditableMessageRow(index, tdObj, dataObj) {
	switch(index) {
		case 1:
			name = "messageName_"+dataObj.id;
			id = "messageName_"+dataObj.id;
			value = dataObj.message;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 2:
			name = "messageType_"+dataObj.id;
			id = "messageType_"+dataObj.id;
			value = dataObj.messageType;
			var messageTypeSelect = $('<select id="' + id + '"/>');
			for(var i=0;i<messageTypeString.length;i++) {
				if(messageTypeString[i]) {
					if(messageTypeString[i].messageTypeName == value) {
						$(messageTypeSelect).append('<option value="' + messageTypeString[i].id + '" selected>' + messageTypeString[i].messageTypeName + '</option>')
					} else {
						$(messageTypeSelect).append('<option value="' + messageTypeString[i].id + '">' + messageTypeString[i].messageTypeName + '</option>')
					}
				}
			}
			$(tdObj).empty();
			$(tdObj).append(messageTypeSelect);
			break;
		case 3:
			name = "author_"+dataObj.id;
			id = "author_"+dataObj.id;
			value = dataObj.author;
			var userSelect = $('<select id="' + id + '"/>');
			for(var i=0;i<userString.length;i++) {
				if(userString[i].userName == value) {
					$(userSelect).append('<option value="' + userString[i].id + '" selected>' + userString[i].userName + '</option>')
				} else {
					$(userSelect).append('<option value="' + userString[i].id + '">' + userString[i].userName + '</option>')
				}
			}
			$(tdObj).empty();
			$(tdObj).append(userSelect);
			break;
		case 4:
			name = "recipient_"+dataObj.id;
			id = "recipient_"+dataObj.id;
			value = dataObj.recipient;
			var type = dataObj.recipient_type 
			var userSelect = $('<select id="' + id + '"/>');
			$(userSelect).append('<option value="None">None</option>');
			var optUser = $("<optgroup label='Users'></optgroup>");
			
			for(var i=0;i<userString.length;i++) {
				if(userString[i].userName == value && type == 'User') {
					$(optUser).append('<option value="' + userString[i].id + '" type="User" selected>' + userString[i].userName + '</option>')
				} else {
					$(optUser).append('<option value="' + userString[i].id + '" type="User">' + userString[i].userName + '</option>')
				}
			}
			
			var optGroup = $("<optgroup label='Groups'></optgroup>");
			
			for(var i=0;i<groupString.length;i++) {
				if(groupString[i].groupName == value  && type == 'Group') {
					$(optGroup).append('<option value="' + groupString[i].id + '" type="Group" selected>' + groupString[i].groupName + '</option>')
				} else {
					$(optGroup).append('<option value="' + groupString[i].id + '" type="Group">' + groupString[i].groupName + '</option>')
				}
			}
			$(userSelect).append(optUser);
			$(userSelect).append(optGroup);
			$(tdObj).empty();
			$(tdObj).append(userSelect);
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

function saveMessageTypeRow(rowId, rowObj){
	var dataObj = null;
	var method = 'save';
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		rowId = rowId.split("_")[1];
	}
	
	var messageTypeName = $('#messageTypeName_'+rowId).val();
	var messageTypeDescription = $('#messageTypeDescription_'+rowId).val();
	var active = $('input:radio[name=isActive_'+rowId+']:checked').val();
	
	dataObj = messageTypeAdminObj.dataList[rowId];
	
	var paramData = {
		type: messageTypeAdminObj.typeData,
		method: method,
		parameter:JSON.stringify({
			messageTypeId: rowId,
			name: messageTypeName,
			description: messageTypeDescription,
			active:active
		})
	};
	
	$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
		if(method == 'add'){
			rowId = data['dataId'];
			//alert("rowId = " + rowId);
			$(rowObj).attr('id',messageTypeAdminObj.tableRowName + rowId);
			var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
			$(checkBox).attr("id",messageTypeAdminObj.checkBoxName + rowId);
			$(checkBox).val(rowId);
			
			var newData = {
					id: rowId,
					name: messageTypeName,
					description: messageTypeDescription,
					active:active
			}
			
			dataObj = new messageTypeData(newData);
			
			messageTypeAdminObj.dataList[rowId] = dataObj;
			
			if(messageTypeString != null) {
				messageTypeString.push({
					id: rowId,
					messageTypeName: messageTypeName
				});
			}
		} else if(method == 'save'){
			dataObj.name = messageTypeName;
			dataObj.description = messageTypeDescription;
			dataObj.active = active;
		}
		
		messageTypeAdminObj.convertToNonEditable(rowObj,dataObj);
		
	},error:function(xhr, textStatus){
		throw "Error occured while saving data. Please try again later.";
	},type: "POST", dataType:"json"});
}

function saveMessageRow(rowId, rowObj){
	var dataObj = null;
	var method = 'save';
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		rowId = rowId.split("_")[1];
	}
	var message = $('#messageName_'+rowId).val();
	var messageTypeNameId = $('#messageType_'+rowId).val();
	var messageTypeName = $('#messageType_' + rowId + ' option:selected').text();
	var authorId = $('#author_'+rowId).val();
	var authorName = $('#author_' + rowId + ' option:selected').text();
	var receiptId = $('#recipient_'+rowId).val();
	var receiptName = $('#recipient_' + rowId + ' option:selected').text();
	var recipientType = $('#recipient_' + rowId + ' option:selected').attr('type') || 'None';
	var active = $('input:radio[name=isActive_'+rowId+']:checked').val();
	
	dataObj = messageAdminObj.dataList[rowId];
	
	var paramData = {
		type: messageAdminObj.typeData,
		method: method,
		parameter:JSON.stringify({
			messageId: rowId,
			message: message,
			messageTypeId: messageTypeNameId,
			authorId: authorId,
			recipientId: receiptId,
			recipientType: recipientType,
			active:active
		})
	};
	
	$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
		if(method == 'add'){
			rowId = data['dataId'];
			//alert("rowId = " + rowId);
			$(rowObj).attr('id',messageAdminObj.tableRowName + rowId);
			var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
			$(checkBox).attr("id",messageAdminObj.checkBoxName + rowId);
			$(checkBox).val(rowId);
			
			var newData = {
					id: rowId,
					message: message,
					messageType: messageTypeName,
					author:authorName,
					recipient:receiptName,
					recipient_type:recipientType,
					active:active,
					creationDate: $.format.date(new Date(),"yyyy-MM-dd HH:mm:ss.SSS")
			}
			
			dataObj = new messageTypeData(newData);
			
			messageAdminObj.dataList[rowId] = dataObj;
			
			if(messageTypeString != null) {
				messageTypeString.push({
					messageTypeId: rowId,
					messageTypeName: messageTypeName
				});
			}
		} else if(method == 'save'){
			dataObj.message = message;
			dataObj.messageType = messageTypeName;
			dataObj.author = authorName;
			dataObj.recipient = receiptName;
			dataObj.recipient_type = recipientType;
			dataObj.active = active;
		}
		
		messageAdminObj.convertToNonEditable(rowObj,dataObj);
		
	},error:function(xhr, textStatus){
		throw "Error occured while saving data. Please try again later.";
	},type: "POST", dataType:"json"});
}