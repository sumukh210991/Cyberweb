<%inherit file="/layout.mako"/>

<%def name="headtags()">
    <script type="text/javascript">
		$(document).ready(function() {

			//Execute the slideShow
			slideShow();

		});

		function slideShow() {

			//Set the opacity of all images to 0
			$('#gallery a').css({opacity: 0.0});

			//Get the first image and display it (set it to full opacity)
			$('#gallery a:first').css({opacity: 1.0});

			//Set the caption background to semi-transparent
			$('#gallery .caption').css({opacity: 0.7});

			//Resize the width of the caption according to the image width
			$('#gallery .caption').css({width: $('#gallery a').find('img').css('width')});

			//Get the caption of the first image from REL attribute and display it
			$('#gallery .content').html($('#gallery a:first').find('img').attr('rel'))
			.animate({opacity: 0.7}, 400);

			//Call the gallery function to run the slideshow, 6000 = change to next image after 6 seconds
			setInterval('gallery()',6000);

		}

		function gallery() {

			//if no IMGs have the show class, grab the first image
			var current = ($('#gallery a.show')?  $('#gallery a.show') : $('#gallery a:first'));

			//Get next image, if it reached the end of the slideshow, rotate it back to the first image
			var next = ((current.next().length) ? ((current.next().hasClass('caption'))? $('#gallery a:first') :current.next()) : $('#gallery a:first'));

			//Get next image caption
			var caption = next.find('img').attr('rel');

			//Set the fade in effect for the next image, show class has higher z-index
			next.css({opacity: 0.0})
			.addClass('show')
			.animate({opacity: 1.0}, 1000);

			//Hide the current image
			current.animate({opacity: 0.0}, 1000)
			.removeClass('show');

			//Display the content
			$('#gallery .content').html(caption);

		}
    </script>
</%def>

<%def name="footer()">
</%def>

<!--#BEGIN col2-main1-->
<div class="col2-main1">
  <div id="newsandmessages">
    <h3>News and Messages</h3>
<%
    cnt=0
    context.write('<table class="d0">')
    for m in c.messages:
       if ( (cnt % 2) == 0 ):
          context.write('<tr class="d0">')
          context.write('<td width=100><mfd0>' + m["date"] + ': </mfd1> </td><td> </mfd0><mf0>' + m["message"] + '</mf0</td>' )
          context.write('</tr>')
       else:
          context.write('<tr class="d1">')
          context.write('<td width=100><mfd1>' + m["date"] + ': </mfd1> </td><td> <mf1>' + m["message"] + '</mf1></td>' )
          context.write('</tr>')
       endif
       cnt=cnt+1
    endfor
    context.write("</table>")
%>

  </div>
  <div class="resourcesandservices">
     <h3>Resources</h3>
     % for i in c.resources:
	<div class="res_entry">${i.name}</div>
     % endfor
  </div>
  <div class="resourcesandservices">
     <h3>Services</h3>
     % for i in c.service_names:
	<div class="srv_entry">${i.name}</div>
     % endfor
  </div>
</div>
<!--#End col2-main1-->

<!--#BEGIN col2-main2-->
<div class="col2-main2">
  <div id="gallery">
      <a href="#" class="show"><img src="${c.images[0]}" rel="${c.captions[c.images[0]]}" alt="" /></a>
    % for i in c.images[1:]:
      <a href="#"><img src="${i}" alt="" rel="${c.captions[i]}"/></a>
    % endfor
	<div class="caption"><div class="content"></div></div>
  </div>
  <div class="clear"></div>
</div>
 <div id="calendar">
<iframe src="http://www.google.com/calendar/embed?height=600&amp;wkst=1&amp;bgcolor=%23FFFFFF&amp;src=gbkea1jbsuei2klp6cj9ek5ge4%40group.calendar.google.com&amp;color=%231B887A&amp;ctz=Europe%2FParis" style=" border-width:0 " width="280" height="260" frameborder="0" scrolling="yes"></iframe>
 </div>

