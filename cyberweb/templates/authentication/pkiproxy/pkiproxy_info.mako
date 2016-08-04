<%inherit file="./pkiproxy.layout.mako"/>

<%def name="headtags()">
	<style>
		.errorStyle{
			margin: 0;
			padding: 1em;
			color: red;
			font-weight: bold;
		}
		
		.formStyle th, .formStyle td{
			border: 0;
		}
		
		.label {
			text-align: right;
		}
	</style>
</%def>

<%def name="col2main()">
  <style type="text/css">
    .prefbutton {
      margin:0 10px 0 10px;
      display:inline;
    }
    .prefbuttons {
      width: 190px;
      margin: 0 auto;
      text-align: center;
    }
    .prefheader {
      float:left;
      width: 130px;
      text-align: right;
      color: grey;
      font-weight: bold;
      margin: 5px 0 5px 0;
    }
    .prefvalue {
      float:left;
      padding-left:15px;
      width: 323px;
      margin: 5px 0 5px 0;
    }
    .prefbar {
      background:#cccccc;
      padding-left:15px;
      margin-bottom:7px;
    }

    .pki_table, .pki_table tr, .pki_table td {
        border: 1;
        table-layout: fixed;
    }
	
    .pki_table td {
        vertical-align:top;
    }

    ul.b {list-style-type:square;list-style-position:inside; margin-left:10px;}

  </style>

  <div style="width:700px;">
	    <div class="prefbar">PKI Credential Information</div>
            <table class="pki_table">
               <tr><td style="width:100px;"> Resources</td>  <td style="vertical-align:top;">Key</td> </tr>
	       % for k in c.current_keys:
                  <tr>
                     <td>
                        <ul class="b"> 
	                   % for r in c.pkires:
                             <li> ${c.pkires[r]}</li> 
	                   % endfor
                        </ul> 
                     </td>
                     <td style="overflow:hidden; vertical-align:top; width:500px;WORD-BREAK:BREAK-ALL">
                         ${k.public_key}
                     </td>
                  </tr>
	       % endfor
            </table>



</div>
</%def>
