<%inherit file="/account/account.layout.mako"/>

<%def name="headtags()">
	<link rel="stylesheet" type="text/css" href="/css/admin.css" media="screen">
	<link rel="stylesheet" type="text/css" href="/css/services.css" media="screen">
	
	<script type="text/javascript" src="/js/account/service.js"></script>
</%def>

<%def name="col2main()">
<script type="text/javascript">
    function connect(service){
        dataString = "service="+service;

        $.ajax({
            type: "POST",
            url: "/user/jodis_connect",
            data: dataString,
            error: function(){
                window.location.reload()
            },
            success: function(){
                window.location.reload()
            }
        });

        return;
    };
</script>

<div class="mainContent">
	<h2 class="mainHeading">CyberWeb Information Services</h2> &nbsp;&nbsp;
	
	<h3>Filter Result:</h3>
	<table class="noBorder">
		<tr>
			<td>Resources:</td>
			<td><select id="filterResources">
					<option value="Available">Available</option>
					<option value="All">All</option>
				</select>
			</td>
		</tr>
	</table>
	<br>
	<div id="resoruceList">
	</div>
	<div style="margin-bottom:40px"></div>
	<script>
		var decodedResourceString = $("<div/>").html('${c.resourceServiceJson}').text();
		var resourceService = eval('(' + decodedResourceString + ')');
	</script>
</div>
</%def>
