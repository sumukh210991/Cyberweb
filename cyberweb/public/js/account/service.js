var allResources = new Array();
var availableResources = new Array();

function resourceData(id,reName) {
	this.id = id;
	this.resourceName = reName;
	this.serviceList = new Array();
}

function serciveData(seName,seType,protocolName) {
	this.serviceName = seName;
	this.serviceType = seType;
	this.protocolName = protocolName;
}

function parseResourceResponse(data) {
	var resourceDivObj = document.getElementById('resoruceList');
	resourceDivObj.innerHTML = '';
	allResources = new Array();
	availableResources = new Array();
	for (key in data) {
		var objIndividual = data[key];
		var resourceObj = new resourceData(objIndividual['Resource Id'],objIndividual['Resource Name']);
		var count = 0;
		var serciveInnerList = new Array();
		var serviceList = objIndividual['Services'];
		for(key1 in serviceList) {
			var serviceObjJSON = serviceList[key1];
			var serciveObj = new serciveData(serviceObjJSON['serviceName'],serviceObjJSON['serviceType'],serviceObjJSON['protocol']);
			serciveInnerList[count++] = serciveObj;
		}
		resourceObj.serviceList = serciveInnerList;
		if(objIndividual['isResourceAvailable'] == 'true') {
			availableResources[availableResources.length] = resourceObj;
		}
		allResources[allResources.length] = resourceObj;
	}
}

function populateResourceLists(listArray) {
	var resourceDivObj = document.getElementById('resoruceList');
	$(resourceDivObj).empty();
	if(listArray.length > 0) {
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
	} else {
		$(resourceDivObj).html('<p>No Resources are available.</p>')
	}
}

$(document).ready(function () {
	parseResourceResponse(resourceService);
	var value = $('#filterResources').val();
	if(value == 'Available') {
		populateResourceLists(availableResources);
	} else {
		populateResourceLists(allResources);
	}
});

$('#filterResources').live('change',function(){
	var value = $('#filterResources').val();
	if(value == 'Available') {
		populateResourceLists(availableResources);
	} else {
		populateResourceLists(allResources);
	}
});