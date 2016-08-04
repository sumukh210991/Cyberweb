

function viz(myform) {
	var dataString = myform.elements[0].name + "=" + myform.elements[0].value;
	for (var i=1; i<myform.length; i++) {
		dataString += "&" + myform.elements[i].name + "=" + myform.elements[i].value;
	}
	$.ajax({
		type: "POST",
		url: "/viz/vizdata",
		data: dataString,
		error: function(msg){
			alert( "Error visualizing data. " + msg);
		},
		success: function(msg){
			$("#viz > .image").html(msg);
		}
	});
}

function checkAll(id,bID){
	var checked = $('#' + id).is(':checked');
	$("#" + bID + " :checkbox").attr('checked', checked);
}

function selectItems(box,bID){
	dataString = "box="+box;
	var files = $("#" + bID + " :checked").each(function(){ dataString += "&file=" + this.name; });
}

function parentdir(box, dir){
	//alert(dir);
	
	parent_path = dir.split('/');
	parent_path[parent_path.length-1] = '';
	parent_path.length = parent_path.length-1;
	new_str = parent_path.join("/");
	if(new_str === ''){
		new_str = '~/';
	}
	//alert(new_str);
	
	select_Host(new_str);	
}

function changedir(box,dir){

	/*if(dir == '..Parent Directory'){
		var folders = $("input#host_path").val().split("/");
		//remove last folder
		folders[folders.length -1] = ''
		host_path = folders.join('/');
		alert('new host path: ' + host_path);
		//host_path = $("input#host_path").val() + '/' + dir;
	}
	else */
	if (dir == '..Parent Directory' || dir == '..Home Directory'){
		host_path = dir;
	}
	else if(dir == '..Refresh Listing'){
		host_path = $("input#host_path").val();
	}
	else{
		host_path = $("input#host_path").val() + '/' + dir;
	}
	
	select_Host(host_path);
	//dataString = "box="+box+"&dir="+dir;
	//$.post("/postjob/changedir", { box:box,dir:dir }, function(){location.href="/postjob"});
	
}


function deletefiles(box,bID){
	dataString = "box="+box;
	$("#" + bID + " :checked").each(function(){ dataString += "&file=" + this.name; });
	$("#" + bID + " :checked").each(function(){ $('#' + this.name).hide(); });

	//return;
	$.ajax({
		type: "POST",
		url: "/viz/delete",
		data: dataString,
		error: function(msg){
			alert( "Error deleting file: " + msg);
		},
		success: function(msg){
			alert( "Success deleting file: " + msg);
			$("#" + bID + " :checked").each(function(){ this.hide() });

			$(".fileList li").removeClass('alternate');
			$(".fileList li:nth-child(odd)").addClass('alternate');
		}
	});
}

function transfer(event,ui){
	var sourcepath = ui.sender.attr('path');
	var source = ui.item.attr('file');
	var target = $(this).attr('path');
	var sourcehost = ui.sender.attr('host');
	var targethost = $(this).attr('host');
	var sourcetype = ui.item.attr('type');
	var eventid = ui.item.attr('var') + sourcehost.replace(".","") + targethost.replace(".","");
	dataString = "src="+sourcepath+"/"+source+"&srchost="+sourcehost+"&tgt="+target+"&tgthost="+targethost;

	$(".fileList li").removeClass('alternate');
	$(".fileList li:nth-child(odd)").addClass('alternate');
	progressString = "<div id='"+eventid+"'><div class='progress-icon'><img class='filesprite' src='/images/waitcursor.gif'/></div><div class='progress-name'>"+source+"</div>\n<div class='progress-host'>"+sourcehost+"</div>\n<div class='progress-host'>"+targethost+"</div>\n<div class='progress-status'>Queued</div><div id='progress-timer' class='progress-time'></div></div><br class='clear'/>";
	$("#progress-box").append(progressString);

	// A Stopwatch instance that displays its time nicely formatted.
	var s = new Stopwatch(function(runtime) {
		 // format time as m:ss.d
		 var minutes = Math.floor(runtime / 60000);
		 var seconds = Math.floor(runtime % 60000 / 1000);
		 var decimals = Math.floor(runtime % 1000 / 100);
		 var displayText = minutes + ":" + (seconds < 10 ? "0" : "") + seconds + "." + decimals;
		 $("#"+eventid + " .progress-time").html(displayText);
	});
	s.doDisplay();
	s.startStop();


	$.ajax({
		type: "POST",
		url: "/viz/transfer",
		data: dataString,
		beforeSend: function(){
			$("#"+eventid + " .progress-status").text("In progress");
		},
		error: function(msg){
			alert( "Error transfering: " + msg);
			$("#"+eventid + " .progress-icon").replaceWith("<div class='progress-icon'><img class='filesprite' src='/images/redx.png'/></div>");
			$("#"+eventid + " .progress-status").text("ERROR");
			s.startStop();
		},
		success: function(msg){
			$("#"+ eventid + " .progress-icon").replaceWith("<div class='progress-icon'><img class='filesprite' src='/images/greencheck.png'/></div>");
			$("#"+ eventid + " .progress-status").text("Done");
			s.startStop();
		}
	});

	return;
}


    
$(document).ready(function(){

	
	$("#leftsortable").sortable({
						helper:'clone',
						items:'li',
						connectWith:'#rightsortable',
						receive: transfer,
						dropOnEmpty: true
					});
	$("#rightsortable").sortable({
						helper:'clone',
						items:'li',
						connectWith:'#leftsortable',
						receive: transfer,
						dropOnEmpty: true
					});
	$(".fileList li:nth-child(odd)").addClass('alternate');
	
	/*
	$(".select_job").click(function(event){
		event.preventDefault();
		var dataString = "";
		$('.select_job_form input').each(function(index){
			dataString += $(this).attr('name') + "=" + $(this).val() + "&";
		});
		
		$.ajax({
			type: "POST",
			url: "/postjob/getImageSSH",
			data: dataString,
			error: function(msg){
				alert( "Error visualizing data. " + msg);
			},
			success: function(msg){
				//result = $.base64.encode(msg);
				//result = base64_encode(msg);
				//result = Base64.encode(msg);
				//result2 = (Base64.decode("iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="));
				result = Convert(msg);
				data_uri = "data:image/png;base64," + result;
				//$("#result").html(result);
				$("#myImage").attr("src",data_uri);
			}
		});
	});
	*/
	
	$(".select_job").click(function(event){
		event.preventDefault();
		var dataString = "";
		$('.select_job_form input').each(function(index){
			dataString += $(this).attr('name') + "=" + $(this).val() + "&";
		});
		showLoading();
		$.ajax({
			type: "POST",
			url: "/postjob/selectJobSSH",
			data: dataString,
			error: function(feedback){
				hideLoading();
				alert( "Error visualizing data. " + feedback);
			},
			success: function(feedback){
				json_object = eval('(' + feedback + ')');
				//alert(json_object.error);
				//alert(json_object.message);
				if(json_object.error == 'true'){
					alert(json_object.message);
				}
				else if(json_object.error == 'false'){				
					console.log(json_object.message);
					$("#job_summary").css({'border' : '1px black solid'});
					$("#summary").html(json_object.message);
					$("#check_selected_job").val($("#host_path").val());
					if($("#analysisTypes").val() == 'contour'){
						$("#job_selected").html("Job: " + $("#check_selected_job").val());
						//$('#plot_filename').html("Bathymetry Plot File: " + $("plot_file").val());
					}
				}
				hideLoading();

			}
		});
	});
	
	
	
	$(".create_remote_script").click(function(event){
		event.preventDefault();
		var dataString = "";
		$('.select_job_form input').each(function(index){
			dataString += $(this).attr('name') + "=" + $(this).val() + "&";
		});
		showLoading();
		$.ajax({
			type: "POST",
			url: "/postjob/createRemoteScript",
			data: dataString,
			error: function(msg){
				hideLoading();
				alert( "Error creating remote script. " + msg);
			},
			success: function(msg){
				hideLoading();
				//alert(msg);
				//result = Convert(msg);
				//data_uri = "data:image/png;base64," + result;
				//$("#result").html(result);
				//$("#myImage").attr("src",data_uri);
			}
		});
	});
	
	
	$(".image_submit").click(function(event){
		event.preventDefault();
		var dataString = "";
		$('.select_job_form input').each(function(index){
			dataString += $(this).attr('name') + "=" + $(this).val() + "&";
		});
		
		showLoading();
		$.ajax({
			type: "POST",
			url: "/postjob/selectjob_ssh",
			data: dataString,
			error: function(msg){
				hideLoading();
				alert( "Error visualizing data. " + msg);
			},
			success: function(msg){
				//result = $.base64.encode(msg);
				//result = base64_encode(msg);
				//result = Base64.encode(msg);
				hideLoading();
				//result2 = (Base64.decode("iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="));
				result = Convert(msg);
				data_uri = "data:image/png;base64," + result;
				//$("#result").html(result);
				$("#myImage").attr("src",data_uri);
			}
		});
	});
	
	 $("#analysisTypes").change(function(){
		
		ajaxGetOption(this);
		//$("#plot_type_div").show();
	});
	
	$("#plot_types").change(function(){
		$("#plane_views_div").show();
	
	});
	
	$(".plane_views").click(function(){
		$(".plane_params").hide();
		$(this).parent('td').next().show();
	});
	
	$("#get_listing_button").click(function(event){
		event.preventDefault();
		select_Host('');
	
	});
	
});

function showLoading(){
$("#loading").show();
}

function hideLoading(){
$("#loading").hide();
}

function ajaxGetOption(element)
{
	//get total columns in table
	var colCount = 0;
    $('.options_table tr:nth-child(1) td').each(function () {
        colCount++;
    });
    //alert(colCount);
    
    //get index of current td
    var current_index = $(element).parent().parent('td').index();
    //alert(current_index);
    
    //remove all columns after current row to remove all selections for previously selected option
    for(i=colCount; i>current_index; i--){
		//$(element).parent().parent('td').find('td').remove();
		 $("#options_table_tr1").find("td:eq("+i+")").remove();
	}
	if(element.value !== ""){
		var name = element.value;
		var label= element.name;
		
		$.getJSON("/postjob/getNextOptions",
				{	"optionName": name,
					"optionLabel": label
				},
				function(data){
					
					if(name =='bathymetry'){
						
						$.getJSON("/postjob/getBathymetryLocation",{},
								function(data){
									//alert(data.path);
									$('#host_path').val(data.path);
									select_Host(data.path);
									//alert("Please select data file to plot bathymetry.");
								});
						$("#job_selected").html('');
						
					}
					else {
						$('#plot_filename').html('');
						//if($("#check_selected_job").val() == ''){
							//alert("Please select job and its respective bathymetry.");	
							//alert("Please select job.");	
						//}
						//text = "Job: " + (($("#check_selected_job").val() == '') ? 'Not Selected' : $("#check_selected_job").val());
						//$("#job_selected").html(text);
						//text = "Bathymetry: " + (($("#plot_file").val() == '') ? 'Not Selected' : $("#plot_file").val());						
						//$('#plot_filename').html(text);
					}
					/*else if(name != 'performance' && name != 'runtime' && name != 'vector'){
						$('#plot_filename').html('');
						$('#plot_file').val(''); 
						$("#check_selected_job").val('');
					}*/
					//alert("Returned");
					if(data.values !== ''){
						addColumnForOption(data.name, data.label, data.subtype, data.values)
					}else{
						showPlotButton();
					}
						
				});
	}
}
function addColumnForOption(name, label, subtype, values){

	var rowCount = $("#options_table").length;
	//alert("rowCount: " + rowCount);
	var tbl_row1 = $("#options_table_tr1"); // table row reference

	tdRow = jQuery('<td/>',{
		id	:	'',
		name:	''
	}).appendTo("#options_table_tr1");

	div = jQuery("<div/>",{
			id: (name+"_div")
	}).appendTo(tdRow);

	h3tag = jQuery("<h3/>",{
			html: subtype
	}).appendTo(div);

	optionSelect = jQuery("<select/>",{
				id:	name,
				name: name			
	}).change(function(){
	
		//$(this).parent().parent('td').next('td').remove();
		var colCount = 0;
	    $('.options_table tr:nth-child(1) td').each(function () {
	        colCount++;
	    });
	    //alert(colCount);
	    
	    //get index of current td
	    var current_index = $(this).parent().parent('td').index();
	    //alert(current_index);
	    
	    //remove all columns after current row to remove all selections for previously selected option
	    for(i=colCount; i>current_index; i--){
			//$(element).parent().parent('td').find('td').remove();
			 $("#options_table_tr1").find("td:eq("+i+")").remove();
		}
		
		if($(this).val() !== ""){
			var name = $(this).val();
			var label= $(this).attr('name');
			
			$.getJSON("/postjob/getNextOptions",
					{	"optionName": name,
						"optionLabel": label
					},
					function(data){
						if(data.values !== ''){
							addColumnForOption(data.name, data.label, data.subtype, data.values)
						}else{
							showPlotButton();
						}
					});
		}
	});

	jQuery("<option/>",{
		value:	"",
		html:	"--Select--"
	}).appendTo(optionSelect);

	for (var i = 0; i < values.length; i++){
		jQuery("<option/>",{
					value: 	values[i].name,
					html:	values[i].label
		}).appendTo(optionSelect);
	}

	optionSelect.appendTo(div);


}

function showPlotButton(){
	var rowCount = $("#options_table").length;
	var tbl_row1 = $("#options_table_tr1"); // table row reference
	
	tdRow = jQuery('<td/>',{
		id	:	'',
		name:	''
	}).appendTo("#options_table_tr1");
	
	div = jQuery("<div/>",{
			id: ("plot_div")
	}).appendTo(tdRow);
	
	submitButton = jQuery("<input />",{
		name:	"submit",
		value:	"Submit",
		type:	"submit"
	}).click(function(){
			var error = 'false';
			if($('#analysisTypes').val() === 'bathymetry' && $('#plot_filename').html() === ''){
				$("#job_selected").html('');
				alert("Please select data file to plot bathymetry.");
				hideLoading();
			}
			else if($('#analysisTypes').val() === 'bathymetry'){
				$("#job_selected").html('');
				showLoading();
				var queryString = $('#get_plot_form').formSerialize();
				element = queryString.split('&');				
				var jsonObj = {};
				for (i =0 ; i < element.length ;i++){					
					data = element[i].split("=", 2);
					jsonObj[data[0]] = data[1];				
				}				
				console.log(jsonObj);
				$.getJSON("/postjob/createPlotImage",
						jsonObj,
						function(data){
							if(data.error != 'true'){
								addPlotRow(data.image, data.parameters);
								hideLoading();																
							}
							else{
								alert('Error creating Bathymetry plot: ' + data.message);
							}
							hideLoading();	
						}
					);		
			}
			else{
				$('#plot_filename').html('');
				var dataString = "";
				$('.select_job_form input').each(function(index){
					dataString += $(this).attr('name') + "=" + $(this).val() + "&";
				});
				showLoading();
				$.ajax({
					type: "POST",
					url: "/postjob/selectJobSSH",
					data: dataString,
					error: function(feedback){
						hideLoading();
						alert( "Error visualizing data. " + feedback);
					},
					success: function(feedback){
						
						json_object = eval('(' + feedback + ')');
						if(json_object.error == 'true'){
							alert(json_object.message);
							text = "Job: " + (($("#check_selected_job").val() == '') ? 'Not Selected' : $("#check_selected_job").val());
							$("#job_selected").html(text);
							hideLoading();
						}
						else if(json_object.error == 'false'){				
							console.log(json_object.message);
							$("#job_summary").css({'border' : '1px black solid'});
							$("#summary").html(json_object.message);
							$("#check_selected_job").val($("#host_path").val());
							if($("#analysisTypes").val() == 'contour' || $("#analysisTypes").val() == 'vector'){
								$("#job_selected").html("Job: " + $("#check_selected_job").val());
							}
							
							//hideLoading();
							if(($('#analysisTypes').val() === 'performance' || $('#analysisTypes').val() === 'runtime' || $('#analysisTypes').val() === 'contour' || $('#analysisTypes').val() === 'vector') && $('#check_selected_job').val() == ''){
								alert("Please select Job to create plots.");
								hideLoading();
							}
							else if($('#analysisTypes').val() === 'bathymetry' && $('#plot_filename').html() === ''){
								alert("Please select data file to plot bathymetry.");
								hideLoading();
								
							}
							else{
								var queryString = $('#get_plot_form').formSerialize();
								element = queryString.split('&');				
								var jsonObj = {};
								for (i =0 ; i < element.length ;i++){					
									data = element[i].split("=", 2);
									jsonObj[data[0]] = data[1];				
								}				
								console.log(jsonObj);
								if($('#analysisTypes').val() === 'bathymetry' && $('#plot_file').val() === ''){
									alert("Please select file to plot bathymetry.");
									hideLoading();
								}
								else if($('#analysisTypes').val() === 'contour' && $("#check_selected_job").val() == ''){
								
									if($("#check_selected_job").val() == ''){
										alert("Please select job.");
										hideLoading();
									}
								}			
								else{
									$.getJSON("/postjob/createPlotImage",
										jsonObj,
										function(data){
											if($('#analysisTypes').val() === 'contour' || $('#analysisTypes').val() === 'vector'){
												if(data.output_type == 'contour_image'){	addPlotRow(data.image, data.parameters);	}
												else if(data.output_type == 'contour_movie'){	addMovieRow(data.output_name);}
												else if(data.output_type == 'contour_sequence'){										
													console.log(data);
													addImageSequence(data);
												}
												else{	alert("Something went wrong" + data.message);	}
												hideLoading();
											}
											else if(data.error != 'true'){
												addPlotRow(data.image, data.parameters);
												hideLoading();																
											}
											hideLoading();	
										}
									);		
								}
							}
						}
					}
						
				});
			}
			
			
			//return false;
	}).appendTo(div);

}

function addMovieRow(movie_name){

	$('#movie_holder').show();
	$("#plot_table").hide();
	
	/*
	player = jwplayer("movie_holder").setup({
        file: movie_name,
        width: 670,
        height: 377
    });
    */
    $('#movie_holder').html('');
	$('#movie_holder').html('\
    							<video id="myVideoTag" width="670" height="377" autoplay="true" controls="controls">\
									<source src="' + movie_name + '" type="video/mp4">\
								</video>\
							');
							

    
    //video_tag = $('<video />')
    //player = $('#movie_holder');
    
	//player.load(movie_name);
	
	//$('#myVideoTag').attr('src', movie_name);

}

function addImageSequence(data){
	$('#movie_holder').html('');
	$('#movie_holder').hide();
	$("#plot_table").show();
	plotTable = $("#plot_table");
	$("#plot_table").html('');
	
	//row id using random number generator
	var randomnumber = Math.floor(Math.random()*101)
	row_id = "row_" + randomnumber;
	
	//new row for new image plot
	trNew = jQuery("<tr/>", { "id": row_id }).appendTo(plotTable);
	
	//new td in tr
	tdRow = jQuery('<td/>',{
		id	:	'',
		name:	''
	}).appendTo(trNew);
	
	//new div in td
	div = jQuery("<div/>",{
			id: ""
	}).appendTo(tdRow);		
	
	//new image and options for that plot in div
	
	for(i=0; i<data.output_name.length; i++){
		//result = ;
		result = Convert(data.image_data[i]);
		data_uri = "data:image/png;base64," + result;
		
		atag_id = "image_atag_" + randomnumber;
		onclick_atag = $("<a />").attr({ href : data_uri, class : "highslide", "id" : atag_id})
								.click(function(event){
										event.preventDefault();
										return hs.expand(this,{ 
																wrapperClassName: 'borderless floating-caption', 
																dimmingOpacity: 0.75, 
																align: 'center'
															   }
														);
													  }
								).appendTo(div);
		
		image_tag = "image_id_" + randomnumber;
		imageEle = jQuery("<img/>",{
			name:	"",
			src	:	data_uri,
			alt	:	"plot_image",
			/*width:	"500px",
			height:	"450px",*/
			width:	"200px",
			height:	"180px",
			"id" : image_tag
		}).appendTo(onclick_atag);
		
		//parameters display
	
		
	}
}

function addPlotRow(plot_image, parameters){
	$('#movie_holder').hide();
	$("#plot_table").show();
	plotTable = $("#plot_table");
	$("#plot_table").html('');
	
	//row id using random number generator
	var randomnumber = Math.floor(Math.random()*101)
	row_id = "row_" + randomnumber;
	
	//new row for new image plot
	trNew = jQuery("<tr/>", { "id": row_id }).appendTo(plotTable);
	
	//new td in tr
	tdRow = jQuery('<td/>',{
		id	:	'',
		name:	''
	}).appendTo(trNew);
	
	//new div in td
	div = jQuery("<div/>",{
			id: ""
	}).appendTo(tdRow);		
	
	//new image and options for that plot in div
	result = Convert(plot_image);
	data_uri = "data:image/png;base64," + result;
	
	atag_id = "image_atag_" + randomnumber;
	onclick_atag = $("<a />").attr({ href : data_uri, class : "highslide", "id" : atag_id})
							.click(function(event){
									event.preventDefault();
									return hs.expand(this,{ 
															wrapperClassName: 'borderless floating-caption', 
															dimmingOpacity: 0.75, 
															align: 'center'
														   }
													);
												  }
							).appendTo(div);
	
	image_tag = "image_id_" + randomnumber;
	imageEle = jQuery("<img/>",{
		name:	"",
		src	:	data_uri,
		alt	:	"plot_image",
		/*width:	"350px",
		height:	"350px",*/
		width:	"500px",
		height:	"450px",
		"id" : image_tag
	}).appendTo(onclick_atag);
	
	//parameters display

	//new td in tr
	tdRow2 = jQuery('<td/>',{
		id	:	'',
		name:	''
	}).appendTo(trNew);
	
	//new div in td
	div2 = jQuery("<div/>",{
			id: ""
	}).appendTo(tdRow2);
	
	form_id = "form_" + randomnumber;
	plot_form = jQuery('<form />', { "id" : form_id , "class" : "param_form"}).appendTo(div2);
	
	param_table_id = 'param_table_id_' + randomnumber;
	param_table = jQuery('<table />',{ "id" : param_table_id, "class" : "form_table" }).appendTo(plot_form);
	if(parameters.length > 0){
		for(i=0; i < parameters.length; i++){
		
			//new row for new image plot
			param_trNew = jQuery("<tr/>", { "id": row_id}).appendTo(param_table);
		
			
			switch(parameters[i].type){
				case "int":
							//Label
							param_tdRow1 = jQuery('<td/>',{
															id	:	'',
															name:	''
														}).appendTo(param_trNew);
		
							label_element = jQuery('<label />', {
																"text" : parameters[i].title
																}).appendTo(param_tdRow1);
														
							//Input Value
							param_tdRow2 = jQuery('<td/>',{
															id	:	'',
															name:	''
														}).appendTo(param_trNew);
							input_element = jQuery('<input />',{
																"name" :  parameters[i].name,
																"value":  parameters[i].value,
																"type" : "text",
																"class": parameters[i].type
																}).appendTo(param_tdRow2);
																
							//new_line = jQuery('<br />').appendTo(plot_form);
							//alert("Integer parameter with name " + parameters[i].name);
							break;
							
				case "hidden":
							//Input Value
							param_tdRow1 = jQuery('<td/>',{
															id	:	'',
															name:	''
														}).appendTo(param_trNew);
														
							input_element = jQuery('<input />',{
																"name" :  parameters[i].name,
																"value":  parameters[i].value,
																"type" : "hidden",
																"class": parameters[i].type
																}).appendTo(param_tdRow1);
							break;
			}	
	
		
		
		}
		
		//check rebuild	
		rebuild_class = "rebuild_" + randomnumber;											
		input_element = jQuery('<input />',{
											"name" :  'check_rebuild',
											"value":  0,
											"type" : "hidden",
											"class": rebuild_class
											}).appendTo(param_tdRow1);	
		
		//Submit Button			
		submit_id = "submit_" + randomnumber;
		input_element = jQuery('<input />',{
											"value":  "Submit",
											"type" : "button",
											"class": "param_form_submit",
											"id"   : submit_id
											})
											.click(function(event){
												showLoading();
												rebuild_clicked($(this));
												hideLoading();
												/*
												//alert("Submit clicked.");
												submit_id = $(this).attr('id');
												values = submit_id.split('submit_');
												row_id = values[1];
												plot_id = "#form_" + row_id;
												var queryString = $(plot_id).formSerialize();
												element = queryString.split('&');
												var jsonObj = {};
												
												//form json oblect with values
												for (i =0 ; i < element.length ;i++){
													data = element[i].split("=", 2);
													jsonObj[data[0]] = data[1];
												}
												console.log(jsonObj);
												showLoading();
												
												$.getJSON("/postjob/rebuildPlotImage",
													jsonObj,
													function(data){
														if(data.error != 'true'){
															//alert("Success");
															result = Convert(data.image);
															data_uri = "data:image/png;base64," + result;
															
															atag_id = "#image_atag_" + row_id;
															console.log("tag_id: " + atag_id);
															$(atag_id).attr({"href" : data_uri});
															
															image_id = "#image_id_" + row_id;
															console.log("image_id: " + image_id);
															$(image_id).attr({"src" : data_uri});
															
															
															//addPlotRow(data.image, data.parameters);
															//plot_table							
														}
														hideLoading();
													}
												);
												
											*/
											
											})
											.appendTo(plot_form);
	
		//Rebuild Default Plot	
		rebuild_id = "default_plot_" + randomnumber;
		input_element = jQuery('<input />',{
											"value":  "Plot Default",
											"type" : "button",
											"class": "param_form_submit",
											"id"   : rebuild_id
											})
											.click(function(event){
												showLoading();
												submit_id = $(this).attr('id');
												values = submit_id.split('default_plot_');
												row_id = values[1];
												rebuild_class = ".rebuild_" + randomnumber;	
												$(rebuild_class).attr({"value" : 1});
												
												//rebuild_clicked($(this));
												
												
												//alert("Submit clicked.");
												submit_id = $(this).attr('id');
												values = submit_id.split('default_plot_');
												row_id = values[1];
												plot_id = "#form_" + row_id;
												var queryString = $(plot_id).formSerialize();
												element = queryString.split('&');
												var jsonObj = {};
												
												//form json oblect with values
												for (i =0 ; i < element.length ;i++){
													data = element[i].split("=", 2);
													jsonObj[data[0]] = data[1];
												}
												console.log(jsonObj);
												showLoading();
												
												$.getJSON("/postjob/rebuildPlotImage",
													jsonObj,
													function(data){
														if(data.error != 'true'){
															//alert("Success");
															result = Convert(data.image);
															data_uri = "data:image/png;base64," + result;
															
															atag_id = "#image_atag_" + row_id;
															console.log("tag_id: " + atag_id);
															$(atag_id).attr({"href" : data_uri});
															
															image_id = "#image_id_" + row_id;
															console.log("image_id: " + image_id);
															$(image_id).attr({"src" : data_uri});
															
															
															//addPlotRow(data.image, data.parameters);
															//plot_table							
														}
														hideLoading();
													}
												);
												//hideLoading();	
											
											
											})
											.appendTo(plot_form);
	
	}
	hideLoading();
}


function rebuild_clicked(element){
											
		//alert("Submit clicked.");
		submit_id = $(element).attr('id');
		values = submit_id.split('submit_');
		row_id = values[1];
		plot_id = "#form_" + row_id;
		var queryString = $(plot_id).formSerialize();
		element = queryString.split('&');
		var jsonObj = {};
		
		//form json oblect with values
		for (i =0 ; i < element.length ;i++){
			data = element[i].split("=", 2);
			jsonObj[data[0]] = data[1];
		}
		console.log(jsonObj);
		//showLoading();
		
		$.getJSON("/postjob/rebuildPlotImage",
			jsonObj,
			function(data){
				if(data.error != 'true'){
					//alert("Success");
					result = Convert(data.image);
					data_uri = "data:image/png;base64," + result;
					
					atag_id = "#image_atag_" + row_id;
					console.log("tag_id: " + atag_id);
					$(atag_id).attr({"href" : data_uri});
					
					image_id = "#image_id_" + row_id;
					console.log("image_id: " + image_id);
					$(image_id).attr({"src" : data_uri});
				}
			});										



}

function clean_hex(input, remove_0x) {
	input = input.toUpperCase();
	
	if (remove_0x) {
	  input = input.replace(/0x/gi, "");        
	}
	
	var orig_input = input;
	input = input.replace(/[^A-Fa-f0-9]/g, "");
	//if (orig_input != input)
	//    alert ("Warning! Non-hex characters in input string ignored.");
	return input;    
}

var base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
function binary_to_base64(input) {
var ret = new Array();
var i = 0;
var j = 0;
var char_array_3 = new Array(3);
var char_array_4 = new Array(4);
var in_len = input.length;
var pos = 0;

while (in_len--)
{
  char_array_3[i++] = input[pos++];
  if (i == 3)
  {
	  char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
	  char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
	  char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
	  char_array_4[3] = char_array_3[2] & 0x3f;

	  for (i = 0; (i <4) ; i++)
		  ret += base64_chars.charAt(char_array_4[i]);
	  i = 0;
  }
}

if (i)
{
  for (j = i; j < 3; j++)
	  char_array_3[j] = 0;

  char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
  char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
  char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
  char_array_4[3] = char_array_3[2] & 0x3f;

  for (j = 0; (j < i + 1); j++)
	  ret += base64_chars.charAt(char_array_4[j]);

  while ((i++ < 3))
	  ret += '=';

}

return ret;
}

function Convert(msg) {
var cleaned_hex = clean_hex(msg, 1);
//document.frmConvert.cleaned_hex.value = cleaned_hex;
if (cleaned_hex.length % 2) {
//alert ("Error: cleaned hex string length is odd.");
//document.frmConvert.base64.value = "";        
return;
}
var binary = new Array();
for (var i=0; i<cleaned_hex.length/2; i++) {
var h = cleaned_hex.substr(i*2, 2);
binary[i] = parseInt(h,16);        
}
return binary_to_base64(binary);
} 


function setFileName(filename) {

	$("#file_name").val(filename.innerHTML);	
	if($('#analysisTypes').val() == 'bathymetry'){
		title = "Bathymetry Plot File: " + filename.innerHTML;
		$('#plot_filename').html(title);
		$('#plot_file').val(filename.innerHTML); 
	}/*
	else if($('#analysisTypes').val() == 'contour'){
		title = "Bathymetry Plot File: " + filename.innerHTML;
		$('#plot_filename').html(title);
		value = $('#host_path').val() + '/' + filename.innerHTML;
		$('#plot_file').val(value); 	
	}*/
	else{
		$('#plot_filename').html('');
		$('#plot_file').val(''); 	
	}
	
	//$(".select_job").click();
}

function selectAnalysisType(selectedType){
	if(selectedType == "Data Type")
	{
		$("#data_type").show();
		$("#plot_type_div").hide();
		
	}
	else
	{
		$("#data_type").hide();
		$("#plot_type_div").show();
	}
	$("#plane_views_div").hide();
}


function select_Host(host_path){

	host_id = $("select#host").val();
	host_name = $("#host option:selected").text();
	if(host_path == '')
		host_path = $("input#host_path").val();
	
	if(host_id != ''){
		showLoading();
		$.getJSON("/postjob/selectHost", 
				{ 
					"host_id"	: host_id,
					"host_name"	: host_name,
					"host_path"	: host_path 
				}, 
				function(data){
					
					//alert(data['right'].listing);
					
					$("#host_path").val(data['right'].path);
					$("#job_path").val(data['right'].path);
					
					$('#rightdatabox').html('	\
							<!--<div style="position: relative;padding: 3px 0 5px 0;border-bottom:dotted 1px grey">	\
								<div class="detail-check">	\
									<input type="checkbox" id="rightcheckall" onClick="checkAll(this.id, \'rightsortable\')"/>	\
								</div>	\
								<div style="margin-left:7px;width:7px;border:solid white;float:left"></div>	\
								<div class="detail-name"><h3>Name</h3></div>	\
								<br class="clear"/>	\
							</div>-->	\
							<li>	\
								<div id="">	\
									<div style="position: relative;">	\
										<div style="width:12px;border:solid white;float:left"></div>	\
										<div class="detail-icon"><img class="filesprite" src="/images/uparrow.gif"/></div>	\
										<div class="detail-name"><a href="#" onClick=\'parentdir("right", "'+data['right'].path+'")\'>Parent Directory..</a></div>	\
										<br class="clear"/>	\
									</div>	\
								</div>	\
							</li>	\
						');

					rightsortable = $('<div />').attr({ 
														id :	'rightsortable',
														class : 'sortable', 
														'host' : data['right'].host , 
														'path' : data['right'].path})
												.appendTo("#rightdatabox");
	
					if (data['right'].listing.length === 0) {
						//alert("listing is empty");
						$('#rightsortable').html('');
					}
					else{
						
													
						filelist = $("<ul />").attr({ class : 'fileList'})
											.appendTo('#rightsortable');
						
						for( i=0; i < data['right'].listing.length ; i++){
							row = data['right'].listing[i];
							if(row[0] == 'directory'){	//if the curent element is directory
								//outer_li = $("<li />").attr()
								$(".fileList").append("	\
														<li var='"+row[1]+"' file='"+row[1]+"' host='"+data['right'].host+"' type='directory'>		\
															<div class='rightdrag'>	\
																<div style='position: relative;'>	\
																	<div class='detail-check'><!--<input type='checkbox' name='"+row[1]+"' />--></div>	\
																	<div class='detail-icon'><img class='filesprite' src='/images/folder.gif'/></div>	\
																	<div class='detail-name'><a href='#' onClick=\"changedir('right','"+row[1]+"')\">"+row[1]+"</a></div>	\
																	<br class='clear'/>		\
																</div>		\
															</div>		\
														</li>		\
													  ");
								
							}
							else if(row[0] == 'file'){		//if the curent element is file
								$(".fileList").append('	\
														<li var="'+row[1]+'" file="'+row[1]+'" host="'+data['right'].host+'" type="file">	\
															<div class="rightdrag">	\
																<div style="position: relative;">	\
																	<div class="detail-check"><!--<input type="checkbox" name="'+row[1]+'" />--></div>	\
																	<div class="detail-icon"><img class="filesprite" src="/images/text.gif"/></div>	\
																	<div class="detail-name" onClick="javascript: return setFileName(this)">'+row[1]+'</div>	\
																	<br class="clear"/>	\
																</div>	\
															</div>	\
														</li>');
							}
						
						}
						/*
						% for a in listarr[box]:
							% if dirvar[box][a] == 1:
								<li var="${listvar[box][a]}" file="${a}" host="${host[box]}" type="directory">
									<div class="${box}drag">
										<div style="position: relative;">
											<div class="detail-check"><input type="checkbox" name="${listvar[box][a]}" /></div>
											<div class="detail-icon"><img class="filesprite" src="/images/folder.gif"/></div>
											<div class="detail-name"><a href="#" onClick="changedir('${box}','${a}')">${a}</a></div>
											<br class="clear"/>
										</div>
									</div>
								</li>
							% else:
								<li var="${listvar[box][a]}" file="${listing[box][a][1]}" host="${host[box]}" type="file">
									<div class="${box}drag">
										<div style="position: relative;">
											<div class="detail-check"><input type="checkbox" name="${listing[box][a][1]}" /></div>
											<div class="detail-icon"><img class="filesprite" src="/images/text.gif"/></div>
											<div class="detail-name" onClick="javascript: return setFileName(this)">${listing[box][a][1]}</div>
											<!--<div class="detail-size">${listing[box][a][3]}</div>
											<div class="detail-modified">${listing[box][a][2]}</div>-->
											<br class="clear"/>
										</div>
									</div>
								</li>
							% endif
						  % endfor
						
						*/
						
						//alert("Total listings: " + data['right'].listing.length);
						
					}
					hideLoading();

				}
		);	
	
	
	}
	else{
		alert("Please select host to access it.");
	}


}







