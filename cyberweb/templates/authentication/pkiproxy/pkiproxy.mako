<%inherit file="./pkiproxy.layout.mako"/>

<%def name="headtags()">
</%def>


<%def name="col2main()">

  <style type="text/css">
    .pki_table, .pki_table tr, .pki_table td {
        border: 1;
        table-layout: fixed;
    }

    .pki_table td {
        vertical-align:top;
    }
   .pki_tdh {
        font-weight:bold;
        vertical-align:top;
    }

    ul.s {list-style-type:square;list-style-position:inside; margin-left:10px;}

</style>

<h2>PKI Credential Management for CyberWeb User: ${c.user}</h2>
<p>
<blockquote>
CyberWeb uses passwordless authentication when performing tasks for CyberWeb Users on resources where they have permission/accounts. The system will create a public/private key pair associated with your CyberWeb account, and then install the public key into the authorized_keys files located on the remote resource under you account. In order for this to occur, you must have an active account, with a valid userID and password.
</blockquote>
<p>
<h3>PKI Enabled Resources for CyberWeb User: ${c.user} </h3>
<table class=pki_table>
   <tr> <td class=pki_tdh>HOSTNAME</td>
        <td class=pki_tdh>KEY#</td> 
        <td class=pki_tdh>ACCOUNT</td> 
        <td class=pki_tdh>PUBKEY</td> 
   </tr>
   % for key in sorted(c.res_pki.iterkeys()):  ## for k in c.res_allata
       <tr><td> ${c.res_pki[key][0]} </td>
           <td style="text-align:center;"> ${c.res_pki[key][3]} </td>
           <td> ${c.res_pki[key][1]} </td>
           <td style="overflow:hidden; vertical-align:top; width:700px;WORD-BREAK:BREAK-ALL">
                ${c.res_pki[key][4]} 
           </td>
       </tr>
   % endfor
</table>
<h3> NON PKI resources (c.res_nonpki)</h3>
<table class=pki_table>
   % for key,v in c.res_nonpki.items():
       <tr><td>${key}</td><td> ${v[0]} </td><td> ${v[1]}  || ${v[2]}   </td></tr>
   % endfor
</table>


% if c.debug:
   <h3> ALL resources (c.res_all) </h3>
   <table>
      % for key,v in c.res_all.items():
          <tr><td>${key}</td><td> ${v[0]} </td><td> ${v[1]} </td></tr>
      % endfor
   </table>

   <p>
   <blockquote>
   <br> c.err: ${c.err}
   <br> c.ssherr: ${c.ssherr}
   <br> c.cmd== ${c.cmd}
   <%
     session = request.environ['beaker.session']
     g = app_globals
   %>
   <p> status: ${c.status}
   % for k,v,admin in g.menu.find_menu('pkiproxy','index',1):
       <li class=current>IDX1  V: "${v}, K=${k}</li>
   % endfor
   <hr>
   % for k,v,admin in g.menu.find_menu('pkiproxy','index',2):
       <li class=current>IDX2  V: "${v}, K=${k}</li>
   % endfor
   <hr>
   % for k,v,admin in g.menu.find_menu('pkiproxy','index',3):
       <li class=current>IDX3  V: "${v}, K=${k}</li>
   % endfor
   <hr>
%endif

</%def>
