<%inherit file="/1col.mako"/>

<%def name='col1main()'>

<h3> CyberWeb Project Contact Form</h3>

% if c.state == 'finish' :
  <blockquote>
  <h2>Thanks for your feedback.
      <br>Your input will be sent to the CyberWeb development team::</h2>
  <blockquote>${c.istr}</blockquote>
  <form action='' method='post'>
  <input type='hidden' name='state' value='' >
  <blockquote>
      <input type='submit' value='Sumbit More Feedback' name='form' >
  </blockquote>
   <p>In the event of problems with this form,  <a href='mailto:mthomas@sciences.sdsu.edu'>Mary Thomas</a>

  </form>
  </blockquote>
% else:

<blockquote>
   <h2>Use this form to report things you like or problems, issues you encounter.<br>
       Please Provide copies of error messages if possible.
  </h2>
  <p>
  <form action='' method='post'>
   <table size="500">
      <tr >
         <td size="150">Name:</td>
         <td><input type="text" size="200" name="name" value="${c.info['name']}" /></td>
      </tr>
      <tr>
         <td>CW Account Name<br>(if you have one):</td>
        <td><input type="text" name="cwuser" value="${c.info['cwuser']}" /></td>
      </tr>
      <tr>
         <td>Email:</td>
         <td><input type="text" name="email" value="${c.info['email']}" /></td>
      </tr>
      <tr>
         <td>Comments:</td>
         <td>
           <textarea class="html-text-box" name="comments">${c.info['comments']}</textarea>
           </td>
      </tr>
     <tr>
       <td align=center colspan=2>
       <input type="submit" value="Submit Information/Request" name="form" />
       </td>
     <tr>
       <td align=center colspan=2>
       In the event of problems with this form,  <a href="mailto:mthomas@sciences.sdsu.edu">Mary Thomas</a>
       </td>
     </tr>

   </table>
</blockquote>
<input type="hidden" name="state" value="process" />
</form>
% endif

<hr>
<h3>Output:</h3>

</%def>