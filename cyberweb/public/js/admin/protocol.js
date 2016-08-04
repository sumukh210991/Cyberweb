var tabOperationObj = new tabOperation();

var protocolAdminObj = new adminData();
protocolAdminObj.columnList = new Array('protocol Name','Description','is Active');
protocolAdminObj.dataKeyNames = new Array('name','description','active');
protocolAdminObj.divName = 'protocolSearchContent'; //Specify the div name to load the content dynamically
protocolAdminObj.errorConsole = 'errorConsoleProtocol';  //Specify error handling div to dislay messages, warning or errors from server
protocolAdminObj.activityPane = 'activity_pane_protocol'; //This gives the loading notification to user
protocolAdminObj.checkBoxName = 'check_protocol_'; //Specify the checkbox name
protocolAdminObj.tableName = 'protocolTable'; //Specify the table Name of the grid
protocolAdminObj.tableRowName = 'protocolRow_'; //Name will be appended to each row of the table
protocolAdminObj.typeData = 'protocol'; //Specify the key name which needs to pass to server for request routing

function init() {
	tabOperationObj.init(); //Initializing tabs
	protocolAdminObj.setData(protocolData); //Setting data function to admin object
	protocolAdminObj.setParseResponse(parseProtocolResponse); //setting ajax response function to handle data manipulation
	protocolAdminObj.hideConsole();
	
	protocolAdminObj.getData('/newadmin/forwardRequest','method=view&type=protocol'); //loading first tab data
}

function protocolData(listData) {
	this.id = listData['id']; //Id is a primary key of the record. This is mandatory for each entity
	this.name = listData['name'];
	this.description = listData['description'];
	this.active = listData['active'];
}

function parseProtocolResponse(data){
	//If you wan to manage or update data of the server
	protocolAdminObj.parseResponse(data);
}

/* This method getting called for each column. */
function makeEditableRow(index, tdObj, dataObj) {
	switch(index) {
		case 1:
			name = "protocolName_"+dataObj.id;
			id = "protocolName_"+dataObj.id;
			value = dataObj.name;
			$(tdObj).html('<input type="text" size="20" name="' + name + '" value="' + value + '" id="' + id + '"/>');
			break;
		case 2:
			name = "protocolDescription_"+dataObj.id;
			id = "protocolDescription_"+dataObj.id;
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

function saveRow(rowId, rowObj){
	var dataObj = null;
	var method = 'save';
	if(rowId.split("_")[0] == 'new') {
		method = 'add'
	} else {
		rowId = rowId.split("_")[1];
	}
	
	var protocolName = $('#protocolName_'+rowId).val();
	var protocolDescription = $('#protocolDescription_'+rowId).val();
	var active = $('input:radio[name=isActive_'+rowId+']:checked').val();
	
	dataObj = protocolAdminObj.dataList[rowId];
	
	var paramData = {	//Need to create a JOSN object of parameters to pass to server
		type: protocolAdminObj.typeData,
		method: method,
		parameter:JSON.stringify({
			protocolId: rowId,
			name: protocolName,
			description: protocolDescription,
			active:active
		})
	};
	
	$.ajax({ url: '/newadmin/forwardRequest', data: paramData, success: function(data) {
		if(method == 'add'){
			rowId = data['dataId'];
			//alert("rowId = " + rowId);
			$(rowObj).attr('id',protocolAdminObj.tableRowName + rowId);
			var checkBox = $('#'+ $(rowObj).attr("id") + " input:checkbox")[0];
			$(checkBox).attr("id",protocolAdminObj.checkBoxName + rowId);
			$(checkBox).val(rowId);
			
			var newData = {
					id: rowId,
					name: protocolName,
					description: protocolDescription,
					active:active
			}
			
			dataObj = new protocolData(newData);
			
			protocolAdminObj.dataList[rowId] = dataObj;
		} else if(method == 'save'){
			dataObj.name = protocolName;
			dataObj.description = protocolDescription;
			dataObj.active = active;
		}
		
		protocolAdminObj.convertToNonEditable(rowObj,dataObj);
		
	},error:function(xhr, textStatus){
		throw "Error occured while saving data. Please try again later.";
	},type: "POST", dataType:"json"});
}

//handler for adding record
$('.addNew').live('click', function(event){
	var newData = {
			id: "new_" + protocolAdminObj.newRowId,
			name: '',
			description: '',
			active: 'True'
	}
	
	var dataObj = new protocolData(newData);
	
	protocolAdminObj.addOperation(dataObj, makeEditableRow, saveRow);
});

//handler for deleting record
$('.delete').live('click', function(event) {
	protocolAdminObj.deleteOperation(protocolAdminObj);
});

//handler for editing record
$('.greyRow,.blueRow').live('click',function (event) {
	var input = $('input', event.target);
	if (event.target.tagName.toUpperCase() === "INPUT" || input.length > 0) {
        // link exist in the item which is clicked
		return true;
    } else {
    	protocolAdminObj.makeEditable(this, makeEditableRow, saveRow);
    }
});