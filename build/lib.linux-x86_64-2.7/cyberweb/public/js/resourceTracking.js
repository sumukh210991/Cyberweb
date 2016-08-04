var resourceList = new Array();
var serviceList = new Array();
var lastResourceURL = '';
var lastServiceURL = '';

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

function switchTabs(tabName) {
	var resoruceTab = document.getElementById('resourceTab');	
	var serviceTab = document.getElementById('servicesTab');
	
	var resoruceLi = document.getElementById('resourceLi');
	var serviceLi = document.getElementById('serviceLi');
	if(tabName == 'Resource') {
		resoruceTab.className = 'visibleTab';
		serviceTab.className = 'hideTab';
		resoruceLi.className = 'selected';
		serviceLi.className = '';
	} else {
		resoruceTab.className = 'hideTab';
		serviceTab.className = 'visibleTab';
		resoruceLi.className = '';
		serviceLi.className = 'selected';
	}
}

function initializeForm() {
	$('#errorConsole').hide();
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
	} else {
		selectedSevice = selectedSevice.substr(0,selectedSevice.length-1);
		url += '?services=' + selectedSevice;
		$('#errorConsole').hide('slow');
	}
	lastServiceURL = url;
	var req = new HttpRequest(url,parseServiceResponse);
	req.send(param);
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

function refereshResource() {
	var resourceDivObj = document.getElementById('resoruceSearchContent');
	resourceDivObj.innerHTML = '';
	$('#errorConsole').hide('slow');
	var selectCombo = document.getElementById("resourceList");
	for(var i=0;i<selectCombo.length;i++) {
		selectCombo.options[i].selected = false;
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