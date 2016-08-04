<%inherit file="/1col.mako"/>

<%def name="col1main()">

  <form action="/exec/interact_action" method="post">
<table border=0 width=98%>
  <tr><td>&nbsp;  </td></tr>
  <tr><td>
      <h3> Cyberweb Execution Services: Batch Script Job Builder</h3>
  </td></tr>
  <tr><td>&nbsp;  </td></tr>
  <tr>
  <td align=left valign =top width=200>
    <table border=1 width=100%>
      <tr>
         <td width=150 align=right>Select Host:</td>
         <td>
            <select name="hostname">
              <option value value="tg-login.ncsa.teragrid.org" checked>tg-login.ncsa.teragrid.org<br>
              <option value value="pipeline3.acel.sdsu.edu">pipeline3.acel.sdsu.edu<br>
              <option value value="anthill.sdsu.edu">anthill.sdsu.edu<br>
              <option value value="dolphin.sdsu.edu">dolphin.sdsu.edu<br>
              <option value value="tbd">tbd<br>
            </select>
         </td>
      </tr>
      <tr>
         <td width=150 align=right>Port:</td>
         <td>2122</td>
      </tr>
      <tr>
         <td width=150 align=right>Executable:</td>
         <td>xxx</td>
      </tr>
      <tr>
         <td width=150 align=right>Arguments:</td>
         <td>xxx</td>
      </tr>
      <tr>
         <td width=150 align=right>Standard Output:</td>
         <td>xxx</td>
      </tr>
      <tr>
         <td width=150 align=right>Standard Error:</td>
         <td>xxx</td>
      </tr>
      <tr>
         <td width=150 align=right>Directory:</td>
         <td>xxx</td>
      </tr>
      <tr>
         <td width=150 align=right>CPU Count:</td>
         <td>xxx</td>
      </tr>
      <tr>
         <td width=150 align=right>Wall Clock Time<br>(min):</td>
         <td>xxx</td>
      </tr>
      <tr> <td colspan=2</td> &nbsp; </tr>
      <tr><td align=right>
           <input type="submit" name="interact_form" value="Submit Job" />
      </td></tr>
    </table>
  </td>
  </table>

</%def>


