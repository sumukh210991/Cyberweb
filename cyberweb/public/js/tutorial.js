$(function() {
  $('.error').hide();

  $(".button").click(function() {
		// validate and process form
		// first hide any error messages
    $('.error').hide();
		
		var dataString = 'name=';
		alert (dataString);return false;
		
		$.ajax({
      type: "POST",
      url: "data/getlisting",
      data: dataString,
      success: function() {
        $('#browser').html("<div id='message'></div>");
        $('#message').html("<h2>Contact Form Submitted!</h2>")
        .append("<p>We will be in touch soon.</p>")
        .hide()
        .fadeIn(1500, function() {
          $('#message').append("<img id='checkmark' src='images/check.png' />");
        });
      }
     });
    return false;
	});
});
runOnLoad(function(){
  $("input#submit").select().focus();
});
