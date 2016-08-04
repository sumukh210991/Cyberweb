<%inherit file="/gcem/gcem.layout.2col.mako"/>

<%def name="col2main()">
% if "error" in c.jobstate  :
   MSG: ${c.jobmsg}<p>
   model_key: ${c.model_key}<p>
   mode: ${c.mode}<p>
   jobstate: ${c.jobstate}<p>
   jobname: ${c.jobname}<p>
% elif c.jobstate == 'build' :
   <h3> ${c.title}</h3>
   <h3 style="color:red">${c.error_flash}</h3>
   <form action='/gccom/app_jobs_action' method='post'>
   <input type='submit' name='app_jobs_action' value='Exec GCEM Job' >
   <table width=100% border=0 bordercolor='white'>
     <tr width=100% align=left  valign=top>
               <td width=250 valign=top align=left bgcolor='#9999cc' >
                 <h3>Job Information:</h3>
               </td>
               <td valign=top align=left bgcolor='#9999cc'>
                     Note: Parameters can only be modified for Test cases, and requires a GCEM account.
               </td> 
            </tr>
            <tr align=left valign=top>
               <td width=250 valign=top align=left >
                   <h3>Job Name: </h3>
                   You can create a unique name
               </td>
               <td valign=top align=left >
                   DATE_TIME_CyberWebJobID_<input type='text' name='jobname' value='${c.jobname}'>
                   <br>The system will include the DATE+TIME+JobID to the jobname after submission.
               </td>
            </tr>
            <tr align=left valign=top>
               <td width=200 valign=top align=left >
                   <h3>Job Decription:</h3> Include custom description or comments: </h3>
               </td>
               <td valign=top align=left >
                   <textarea name="jobdescription" class="html-text-box">GCEM ${c.model_key} ${c.mode}  Case: fixed parameters.  </textarea>
               </td>
            </tr>
            <tr>
               <td valign=top align=left >
                   <h3>Select Host:<h3>
               </td>
               <%
               cnt=0
               %>
               <td valign=top align=left >
		  % if  len(c.resources.items()) == 0: 
 		 	You currently have SSH connected resources.<br>
         		To add compute resource accounts, see MyCyberWeb-->Authentication.
		  % else:
                      % for r_id, r in c.resources.items():
                          <% checked = "checked" if cnt == 0 else "" %>
                          <input type='radio' name='hostname' value='${r_id}' ${checked}>&nbsp;&nbsp;&nbsp;${r['hostname']}<br>
			  <%
			     cnt=cnt+1
			  %>
                       % endfor
		   %endif
      </td>
   </tr>
            <tr align=left valign=top>
               <td width=200 valign=top align=left >
                   <h3>Job Details: </h3>
               </td>
               <td valign=top align=left >
                  <b>Grid Name: </b> ${c.grid_name} <br>
                  <b>Grid Dimensions:</b> [IMax,JMax,KMax] = [${c.grid_imax}, ${c.grid_jmax},${c.grid_kmax}] 
               </td>
            </tr>
   <tr> 
      <td colspan=2 align=left valign=top >
         <table width=100% align=center>
           <tr bgcolor='#9999cc'>
               <td colspan=3 >
                   <h3>Parameter List:</h3> Note: All parameters can be modified for the Test cases.
               </td> 
            </tr>
            <%
                p = c.model_params
             %>
            % if len(p):
           <tr bgcolor='#ffffcc'>
           % for i in c.model_param_hdrs:
               <th>${i}</th>
           % endfor
           % for r in p:
               <tr>
                 <th>${r[0]}</th>
                 <td>${r[1]}</td>
                 <td> <input type="text" readonly="readonly" name="${r[0]}.paramval" value="${r[2]}"></td>
               </tr>
           % endfor
            </td>
            </tr>
          </table>
       <tr>
       <td colspan=3  align=center><p>
            <input type="submit" name="app_jobs_action" value="Exec GCEM Job" />
       </td>
       </tr>
   </table>
       <input type="hidden" name="mode"         value="${c.mode}" >
       <input type="hidden" name="model_key"    value="${c.model_key}" >
       <input type="hidden" name="model_params" value="${c.model_params}" >
       <input type="hidden" name="model_desc"   value="${c.model_desc}" >
       <input type="hidden" name="jobstate"     value="submit" >
   </form>
       % else:
           No Application Available.<br>
       % endif
% elif c.jobstate == 'submitted' :
<h3>jobstate: ${c.jobstate}</h3>
   <h3>GCEM Job Submission Successful for ${c.model_desc} ${c.mode} Case:</h3>
   <table>
     <tr align="left" valign="top" ><td width="100"><b>GCEM User:</b> </td><td> ${c.cwuser} </td></tr>
     <tr><td> <b>GCEM Job Title</b>   </td><td> ${c.title}  </td></tr>
     <tr><td> <b>GCEM User: </b>      </td><td> ${c.cwuser}  </td></tr>
     <tr><td> <b>GCEM Job Name: </b>  </td><td> ${c.jobname}  </td></tr>
     <tr><td> <b>Grid Name: </b>      </td><td> ${c.grid_name} </td></tr>
     <tr><td> <b>Grid Dimensions:</b> </td>
         <td> [IMax,JMax,KMax] = [${c.grid_imax}, ${c.grid_jmax},${c.grid_kmax}] </td></tr>
     <tr><td> <b>Remote Host:</b>     </td><td> ${c.hostname}  </td></tr>
     <tr><td><b>JobId:</b>   </td><td>${c.jobid} </td></tr>
     <tr><td><b>Mode:</b>  </td><td> ${c.mode} </td></tr>
   </table>
    </td></tr>
    <table>
        <tr>
           % for i in c.model_param_hdrs:
               <th>${i}</th>
           % endfor
         </tr>
           % for r in c.model_params:
         <tr>
                   % for k in r:
                       <td>${k}</td>
                   % endfor
         </tr>
    	   % endfor
   </table>
   <form action="/gccom/jobmonitor" method="post">
       <input type="hidden" name="mode"        value="${c.mode}" >
       <input type="hidden" name="jobid"        value="${c.jobid}" >
       <input type="hidden" name="jobname"      value="${c.jobname}" >
       <input type="hidden" name="model_key"    value="${c.model_key}" >
       <input type="hidden" name="model_params" value="${c.model_params}" >
       <input type="hidden" name="jobstate"     value="monitor" >
       <input type="submit" name="app_jobs_action" value="Monitor Jobs" />
   </form>

% else:
   <h3>Problem with Run: %{c.title}</h3>
   model_key: ${c.model_key}<p>
   mode: ${c.mode}<p>
   jobstate: ${c.jobstate}<p>
   jobname: ${c.jobname}<p>
% endif

</%def>

