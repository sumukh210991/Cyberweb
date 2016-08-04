<%inherit file="/account/account.layout.mako"/>

<%def name="headtags()">
</%def>

<%def name="col2main()">
<script type="text/javascript">
     function sendMessage(){
         var recipient = document.MessageForm.recipient.value;
         var message = document.MessageForm.message.value;

         var dataString = "recipient=" + recipient + "&message=" + message;
         $.ajax({
               type: "POST",
               url: "/user/send_message",
               data: dataString,
               error: function(msg){
		   var status = eval('(' + msg + ')');
		   if (status.error) {
                       alert("Error: " + status.message);
		   }
               },
               success: function(msg){
		   var status = eval('(' + msg + ')');
		   if (!status.error) {
                       alert(status.message);
		   }
               }
        });
        return;
     };
</script>

<h2>${c.title}</h2>
<h3>CyberWeb Information Services</h3>
<br>
<h3>Received Messages</h3>
  % if len(c.messages):
  <table>
    <tr>
    % for j in c.messageheaders:
        <th>${j}</th>
    % endfor
    </tr>
    % for i in c.messages:
        <tr>
        % for j in c.messageheaders:
          % if i.has_key(j):
            <td>${i[j]}</td>
          % else:
            <td></td>
          % endif
        % endfor
        </tr>
    % endfor
  </table>
  % else:
      You have no messages at this time. <br>
  % endif
<p>&nbsp;
<p>&nbsp;
<hr>
  <form name="MessageForm" action="#" method="POST">
    <div class="sendMessageBox">
    Send
    <select name="recipient">
      % for i in c.recipients:
          <option value="${i['value']}">${i['name']}</option>
      % endfor
    </select>
    a message.<p>
    <textarea name="message" class="html-text-box">Enter your message here... </textarea>
      <p><input type="button" value="Send Message" onClick="sendMessage()"/>
      <p><a onClick="sendMessage()">Send Message</a>
    </div>
  </form>
  <br>
  <p>
</%def>
