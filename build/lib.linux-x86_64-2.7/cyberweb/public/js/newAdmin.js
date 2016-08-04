function tabOperation() {
	this.tabList = new Array();
	this.tabDivList = new Array();
	this.currentTab = null;
	
	this.switchTab = function (selectTab) {
		for(var i=0;i<this.tabList.length;i++) {
			var tabListObj = this.tabList[i];
			var tabObj = this.tabDivList[i];
			if(selectTab && tabListObj.id == selectTab.id) {
				tabListObj.className = 'selected';
				tabObj.className = 'visibleTab classTab';
				this.currentTab = tabListObj.id;
			} else {
				tabListObj.className = '';
				tabObj.className = 'hideTab';
			}
		}
	}
	
	this.init = function () {
		$('#errorConsole').hide();
	}
}

function adminData() {
	/* Object Specific local variable */
	this.dataList = new Array();
	this.preClassName = 'greyRow';
	this.newRowId = 1;
	
	/* Mandatory Initialization While Creating new object*/
	this.errorConsole = 'errorConsole';
	this.activityPane = 'activity_pane';
	this.checkBoxName = 'check_';
	this.tableName = 'table';
	this.tableRowName = 'row_';
	this.typeData = null;
	this.divName = 'searchContent';
	this.dataObj = null;
	this.populateDataObj = null;
	this.parseResponseObj = null;
	this.columnList = new Array();
	this.dataKeyNames = new Array();
	this.sortValue = {};
	this.isEditable = true;
	this.url = '/newadmin/forwardRequest';
}

adminData.prototype.hideConsole = function() {
	$('#'+this.errorConsole).hide();
}

adminData.prototype.setData = function (dataObj) {
	this.dataObj = dataObj;
}

adminData.prototype.setPopulateData = function (populateObj) {
	this.populateDataObj = populateObj;
}

adminData.prototype.setParseResponse = function (parseObj) {
	this.parseResponseObj = parseObj;
}

adminData.prototype.getData = function(url,param) {
	if($('#' + this.activityPane)) {
		$('#' + this.activityPane).showLoading();
	}
	var req = new HttpRequest(url,this.parseResponseObj);
	req.send(param);
}

adminData.prototype.findErrorType = function(data) {
	if(data.indexOf('You must specify a username and password') >= 0) {
		window.location.href = '/signin';
	}
}

adminData.prototype.parseResponse = function(data, callback) {
	var count = 0;
	this.dataList = new Array();
	var myData = null;
	try{
		myData = eval('(' + data + ')');
	} catch(err) {
		alert('err = ' + err);
		myData = null;
		this.findErrorType(data);
	}
	for (key in myData) {
		var objIndividual = myData[key];
		var dataObj = new this.dataObj(objIndividual);
		this.dataList[dataObj.id] = dataObj;
	}
	
	if(this.populateDataObj != null) {
		this.populateDataObj(this.dataList);
	} else if(this.columnList.length > 0 && this.dataKeyNames.length > 0){
		this.populateLists(this.dataList);
	}
	
	if(callback) {
		callback();
	}
	if($('#' + this.activityPane)) {
		$('#' + this.activityPane).hideLoading();
	}
}

adminData.prototype.populateLists = function(listArray) {
	var divObjResult = document.getElementById(this.divName);
	divObjResult.innerHTML = '';
	
	var divObj = document.createElement('div');
	/*var h4Obj = document.createElement('h2');
	h4Obj.innerHTML = this.tableHeader;*/
	var tableObj = document.createElement('table');
	tableObj.id = this.tableName; 
		
	var thead = document.createElement('thead');
	var rowObj = thead.insertRow(-1);
	rowObj.className = "tableHeader";
	
	var cell0 = rowObj.insertCell(0);
	cell0.innerHTML = '';
	var adminObj = this;
	
	for (var i=0;i<this.columnList.length;i++) {
		var cell = rowObj.insertCell(i+1);
		cell.innerHTML = this.columnList[i];
		
		$(cell).click(function(event){
			//alert('cell Index = ' + this.cellIndex + " Sort Order = " + adminObj.sortValue[this.cellIndex]);
			var keyIndex = this.cellIndex - 1;
			function SortByASC(a, b){
			  var aName = eval("a."+adminObj.dataKeyNames[keyIndex]).toLowerCase();
			  var bName = eval("b."+adminObj.dataKeyNames[keyIndex]).toLowerCase(); 
			  return ((aName < bName) ? -1 : ((aName > bName) ? 1 : 0));
			}
			
			function SortByDSC(a, b){
			  var aName = eval("a."+adminObj.dataKeyNames[keyIndex]).toLowerCase();
			  var bName = eval("b."+adminObj.dataKeyNames[keyIndex]).toLowerCase(); 
			  return ((aName > bName) ? -1 : ((aName < bName) ? 1 : 0));
			}
			
			if(adminObj.sortValue[this.cellIndex] == 'dsc') {
				adminObj.sortValue[this.cellIndex] = 'asc';
				adminObj.dataList.sort(SortByDSC);
			} else {
				adminObj.sortValue[this.cellIndex] = 'dsc';
				adminObj.dataList.sort(SortByASC);
			}
			adminObj.populateLists(adminObj.dataList);
		});
		
		$(cell).mouseover(function (event){
			$(this).addClass('cursorHand');
		});
		
		$(cell).mouseout(function (event){
			$(this).removeClass('cursorHand');
		});
	}
	
	var tfoot = document.createElement('tfoot');
	var rowObj = tfoot.insertRow(-1);
	rowObj.className = "tableHeader";
	
	var cell0 = rowObj.insertCell(0);
	cell0.innerHTML = '';
	
	for (var i=0;i<this.columnList.length;i++) {
		var cell = rowObj.insertCell(i+1);
		cell.innerHTML = this.columnList[i];
		
		$(cell).click(function(event){
			//alert('cell Index = ' + this.cellIndex + " Sort Order = " + adminObj.sortValue[this.cellIndex]);
			var keyIndex = this.cellIndex - 1;
			function SortByASC(a, b){
			  var aName = eval("a."+adminObj.dataKeyNames[keyIndex]).toLowerCase();
			  var bName = eval("b."+adminObj.dataKeyNames[keyIndex]).toLowerCase(); 
			  return ((aName < bName) ? -1 : ((aName > bName) ? 1 : 0));
			}
			
			function SortByDSC(a, b){
			  var aName = eval("a."+adminObj.dataKeyNames[keyIndex]).toLowerCase();
			  var bName = eval("b."+adminObj.dataKeyNames[keyIndex]).toLowerCase(); 
			  return ((aName > bName) ? -1 : ((aName < bName) ? 1 : 0));
			}
			
			if(adminObj.sortValue[this.cellIndex] == 'dsc') {
				adminObj.sortValue[this.cellIndex] = 'asc';
				adminObj.dataList.sort(SortByDSC);
			} else {
				adminObj.sortValue[this.cellIndex] = 'dsc';
				adminObj.dataList.sort(SortByASC);
			}
			adminObj.populateLists(adminObj.dataList);
		});
		
		$(cell).mouseover(function (event){
			$(this).addClass('cursorHand');
		});
		
		$(cell).mouseout(function (event){
			$(this).removeClass('cursorHand');
		});
	}
	
	var tbody = document.createElement('tbody');
	this.preClassName = 'greyRow';
	for(var i=0;i<listArray.length;i++){
		var dataObj = listArray[i];
		if(dataObj) {
			var rowObj = tbody.insertRow(-1);
			if(this.tableRowName != null) {
				rowObj.id = this.tableRowName + dataObj.id;
			} else {
				rowObj.id = dataObj.id;
			}
			$(rowObj).attr("isEditable","false");
			this.createRow(rowObj,dataObj);
		}
	}
	
	tableObj.appendChild(thead);
	tableObj.appendChild(tfoot);
	tableObj.appendChild(tbody);
	//divObj.appendChild(h4Obj);
	divObj.appendChild(tableObj);
	divObjResult.appendChild(divObj);
}

adminData.prototype.createRow = function(rowObj,dataObj) {
	
	var cell0 = rowObj.insertCell(0);
	cell0.innerHTML = '<input type="checkbox" id="'+ this.checkBoxName + rowObj.id.split("_")[1] +'" name="' + this.checkBoxName + '" value="' + dataObj.id + '"/>';
	cell0.className = 'checkCell';
	cell0.tagName = "checkBox";
	
	for (var j=0;j<this.dataKeyNames.length;j++) {
		var cell1 = rowObj.insertCell(j+1);
		cell1.innerHTML = eval("dataObj."+this.dataKeyNames[j]);
	}
	
	if(this.preClassName == 'blueRow') {
		rowObj.className='greyRow';
		this.preClassName = 'greyRow';
	} else {
		rowObj.className='blueRow';
		this.preClassName = 'blueRow';
	}
}

adminData.prototype.cancelEdit = function(event,cancelButton, adminObj) {
	var rowId = $(cancelButton).attr('rowId');
	var rowObj = document.getElementById(rowId);
	var dataId = rowId.split("_")[1];
	var dataObj = adminObj.dataList[dataId];
	
	if(rowId.split("_")[0] == 'new') {
		var rowObj = document.getElementById("new_" + dataId);
		var rowIndex = rowObj.rowIndex;
		var table = rowObj.parentNode;
		table.deleteRow(rowIndex-1);
		return;
	}
	
	adminObj.convertToNonEditable(rowObj,dataObj);
	$(rowObj).attr("isEditable","false");
}

adminData.prototype.makeEditable = function(rowObj, callBack, callBackSaveEdit) {
	var dataId = $(rowObj).attr('id');
	dataId = dataId.split("_")[1];
	var dataObj = null;
	//alert("rowObj.isEditable = " + $(rowObj).attr("isEditable"));
	if($(rowObj).attr("isEditable") == "false") {
		$(rowObj).attr("isEditable","true");
		this.convertToEditable(rowObj,this.dataList[dataId],callBack,callBackSaveEdit);
	}
}

adminData.prototype.convertToEditable = function(rowObj, dataObj, callBack, callBackSaveEdit) {
	if(!callBack) {
		console.log('No CallBack function is defined for makeEditable');
	}
	
	if(!callBackSaveEdit) {
		console.err('No CallBack function is defined to save record');
	}
	var tds = $(rowObj).find('td');
	$.each(tds, function(index, tdObj) {
		if(callBack) {
			callBack(index,tdObj,dataObj);
		}
	});
	
	var cellCount = rowObj.cells.length;
	//var cellObj = rowObj.insertCell(cellCount);
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
	$(saveButton).attr('href','#');
	$(saveButton).addClass('imageHyperLink');
	$(saveButton).html('<img src="../images/save-as-icon_small.png" width="24" height="24" alt="Save" title="Save" />');
	$(saveButton).attr('rowId',$(rowObj).attr('id'));
	var activityPane = this.activityPane;
	$(saveButton).click(function (event) {
		if($('#' + activityPane)) {
			$('#' + activityPane).showLoading();
		}
		if(callBackSaveEdit) {
			try{
				var rowId = $(this).attr('rowId');
				var rowObj = document.getElementById(rowId);
				callBackSaveEdit(rowId,rowObj);
			} catch(err) {
				if($('#' + activityPane)) {
					$('#' + activityPane).hideLoading();
				}
				alert('Error occured while saving data. Please try again later.');
			}
		}
		if($('#' + activityPane)) {
			$('#' + activityPane).hideLoading();
		}
	});
	
	
	var cancelButton = $('<a/>');
	$(cancelButton).attr('id','cancel_'+dataObj.id);
	$(cancelButton).attr('href','#');
	$(cancelButton).addClass('imageHyperLink');
	$(cancelButton).html('<img src="../images/Button-Delete-icon.png" width="24" height="24" alt="Cancel" title="Cancel" />');
	$(cancelButton).attr('rowId',$(rowObj).attr('id'));
	var adminObj = this;
	$(cancelButton).click(function(event) {
		adminObj.cancelEdit(event,this,adminObj);
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
			adminObj.deleteRecord(adminObj, dataId);
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
}

adminData.prototype.convertToNonEditable = function(rowObj, dataObj) {
	var cellCount = rowObj.cells.length;
	var tds = $(rowObj).find('td');
	var dataKeyNames = this.dataKeyNames;
	$.each(tds, function(index, item) {
		if(index > 0){
			$(item).empty();
			var value = eval("dataObj."+dataKeyNames[index-1]);
			$(item).html(value);
		}
	});
	
	var cellCount = rowObj.cells.length;
	var cellObj = rowObj.cells[0];
	cellObj.innerHTML = '<input type="checkbox" id="'+ this.checkBoxName + rowObj.id.split("_")[1] +'" name="' + this.checkBoxName + '" value="' + dataObj.id + '"/>';
	$(cellObj).removeClass('iconsStyle').addClass('checkCell');
	cellObj.tagName = "checkBox";
	cellObj.style.width = "15px";
	cellObj.width = "15px";
	//rowObj.deleteCell(--cellCount);
	
	$(rowObj).attr("isEditable","false");
}

adminData.prototype.addOperation = function(dataObj, callBack, callBackSaveEdit) {
	
	var tableObj = document.getElementById(this.tableName);
	var tbody = tableObj.getElementsByTagName('tbody')[0];
	var rowObj = tbody.insertRow(-1);
	rowObj.id = "new_" + this.newRowId;
	$(rowObj).attr("isEditable","true");
	
	this.createRow(rowObj,dataObj);
	this.convertToEditable(rowObj, dataObj, callBack, callBackSaveEdit);
	this.dataList[dataObj.id] = dataObj;
	this.newRowId++;
}

adminData.prototype.deleteOperation = function(adminObj, clearFromList) {
	var checkBoxValue = '';
	$("input:checkbox[name=" + this.checkBoxName + "]:checked").each(function()
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
		this.deleteRecord(adminObj, checkBoxValue, clearFromList);
	}
}

adminData.prototype.deleteRecord = function (adminObj, checkBoxValue, clearFromList){
	$('#' + adminObj.activityPane).showLoading();
	var paramData = {
			type: this.typeData,
			method: 'delete',
			parameter: JSON.stringify({
				deleteId: checkBoxValue
			})
	};
	
	$.ajax({ url: adminObj.url, data: paramData,
		beforeSend: function(x) {
            if (x && x.overrideMimeType) {
              x.overrideMimeType("application/j-son;charset=UTF-8");
            }
        },
		success: function(data) {
			
			var rowIds = checkBoxValue.split(',');
			for (var i=0;i<rowIds.length;i++) {
				var rowObj = document.getElementById(adminObj.tableRowName + rowIds[i]);
				if(clearFromList) {
					for(var i=0;i<clearFromList.length;i++) {
						if(clearFromList[i].id == rowObj.id.split("_")[1]) {
							delete clearFromList[i];
						}
					}
				}
				delete adminObj.dataList[rowObj.id.split("_")[1]];
				var rowIndex = rowObj.rowIndex;
				var table = rowObj.parentNode;
				table.deleteRow(rowIndex-1);
			}
			$('#' + adminObj.activityPane).hideLoading();
		
		},error:function(xhr, textStatus){
			$('#' + adminObj.activityPane).hideLoading();
			alert('Error occured while deleting data. Please try again later.');
		},type: "POST", dataType:"json"});
}
